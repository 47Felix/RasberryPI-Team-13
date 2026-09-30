"""Challenge III: Cloud-Bridge Pi -> Azure IoT Hub (Plan B: ThingSpeak).

Liest neue Zeilen aus der `readings`-Tabelle von Challenge I
(`Challenge-I-Ice-Truck/Code/pi-backend/challenge_i.db`, geschrieben von
app.py) und schickt sie gebuendelt per MQTT (TLS, Port 8883 - oder MQTT
ueber WebSockets auf 443, falls das Netz 8883 blockt) an den Azure IoT Hub.

Store & Forward: Die lokale SQLite-DB ist gleichzeitig der Puffer. Der
Cursor (`last_sent_id` in STATE_PATH) wird erst NACH erfolgreichem Senden
weitergeschoben - faellt unterwegs das Mobilfunknetz aus, wird der
Rueckstand beim naechsten erfolgreichen Verbindungsaufbau nachgeliefert.
Weil zwischen erfolgreichem Senden und Speichern des Cursors theoretisch
ein Absturz liegen kann (at-least-once), traegt jede Zeile ihre lokale
`id` mit, damit die Cloud Duplikate herausfiltern kann.

Kompaktes Spaltenformat (`cols` + `rows` statt eines Objekts pro Messung),
weil der kostenlose IoT-Hub-Tarif F1 nur 8.000 Nachrichten a 0,5 KB pro Tag
erlaubt - siehe README.md, Abschnitt "Kontingent".
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Protocol

SCHEMA_VERSION = "icetruck-v1"

COLUMNS = [
    "id",
    "timestamp_utc",
    "sensor_board_raw",
    "sensor_board_temp_c",
    "sensor_board_digital",
    "actor_board_raw",
    "actor_board_temp_c",
    "fan_pwm",
    "valve_angle",
]

_HERE = Path(__file__).resolve().parent
_DEFAULT_DB_PATH = _HERE.parent.parent.parent / "Challenge-I-Ice-Truck" / "Code" / "pi-backend" / "challenge_i.db"


def _env_float(name: str, default: float) -> float:
    value = os.environ.get(name)
    return default if value is None else float(value)


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name)
    return default if value is None else int(value)


DB_PATH = os.environ.get("DB_PATH", str(_DEFAULT_DB_PATH))
STATE_PATH = os.environ.get("STATE_PATH", str(_HERE / "bridge_state.json"))
TRUCK_ID = os.environ.get("TRUCK_ID", "icetruck-team13-1")
SEND_INTERVAL_SECONDS = _env_int("SEND_INTERVAL_SECONDS", 60)
MAX_ROWS_PER_MESSAGE = _env_int("MAX_ROWS_PER_MESSAGE", 60)
MAX_MESSAGES_PER_CYCLE = _env_int("MAX_MESSAGES_PER_CYCLE", 5)
# "now" = beim allerersten Start nur neue Messungen schicken (alter Bestand
# wuerde das F1-Tageskontingent sprengen), "all" = kompletten Bestand nachladen.
START_FROM = os.environ.get("START_FROM", "now")
ALARM_TEMP_C = _env_float("ALARM_TEMP_C", 28.0)
SENSOR_MISMATCH_C = _env_float("SENSOR_MISMATCH_C", 3.0)


class Sender(Protocol):
    def send(self, body: str, properties: dict[str, str]) -> None: ...


def open_db(db_path: str) -> sqlite3.Connection:
    # Nur lesend oeffnen - geschrieben wird ausschliesslich von app.py.
    return sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)


def load_state(state_path: str) -> dict | None:
    try:
        with open(state_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def save_state(state_path: str, state: dict) -> None:
    # Atomar schreiben, damit ein Stromausfall keinen halben Cursor hinterlaesst.
    tmp_path = f"{state_path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(state, f)
    os.replace(tmp_path, state_path)


def initial_cursor(conn: sqlite3.Connection, start_from: str) -> int:
    if start_from == "all":
        return 0
    (max_id,) = conn.execute("SELECT COALESCE(MAX(id), 0) FROM readings").fetchone()
    return max_id


def fetch_batch(conn: sqlite3.Connection, after_id: int, limit: int) -> list[tuple]:
    return conn.execute(
        f"SELECT {', '.join(COLUMNS)} FROM readings WHERE id > ? ORDER BY id LIMIT ?",
        (after_id, limit),
    ).fetchall()


def health_flags(rows: list[tuple], alarm_temp_c: float, mismatch_c: float) -> list[str]:
    """Einfache Vorab-Auswertung am Edge fuer Alarm-Routing / Predictive Maintenance.

    - temp_high: Mittelwert beider Boards ueber der Alarmschwelle
    - sensor_mismatch: beide Boards weichen deutlich voneinander ab (typisch
      fuer Wackelkontakt/defekten Sensor, siehe Offene Punkte zum KY-028)
    - sensor_stuck: Rohwert eines Boards ueber einen ganzen Batch exakt
      konstant (eingefrorener Sensor/haengender I2C-Bus)
    """
    idx = {name: i for i, name in enumerate(COLUMNS)}
    flags = []
    averages = [(r[idx["sensor_board_temp_c"]] + r[idx["actor_board_temp_c"]]) / 2 for r in rows]
    if max(averages) > alarm_temp_c:
        flags.append("temp_high")
    deltas = [abs(r[idx["sensor_board_temp_c"]] - r[idx["actor_board_temp_c"]]) for r in rows]
    if max(deltas) > mismatch_c:
        flags.append("sensor_mismatch")
    if len(rows) >= 12:
        for board in ("sensor_board_raw", "actor_board_raw"):
            if len({r[idx[board]] for r in rows}) == 1:
                flags.append("sensor_stuck")
                break
    return flags


def build_message(
    rows: list[tuple], truck_id: str, alarm_temp_c: float, mismatch_c: float
) -> tuple[str, dict[str, str]]:
    idx = {name: i for i, name in enumerate(COLUMNS)}
    temps = [t for r in rows for t in (r[idx["sensor_board_temp_c"]], r[idx["actor_board_temp_c"]])]
    flags = health_flags(rows, alarm_temp_c, mismatch_c)
    body = {
        "schema": SCHEMA_VERSION,
        "truck_id": truck_id,
        "first_ts": rows[0][idx["timestamp_utc"]],
        "last_ts": rows[-1][idx["timestamp_utc"]],
        "min_temp_c": min(temps),
        "max_temp_c": max(temps),
        "flags": flags,
        "cols": COLUMNS,
        "rows": [list(r) for r in rows],
    }
    # Application Properties: im IoT Hub per Routing-Query auswertbar, ohne
    # den Body zu parsen (z.B. Route "alarm = 'true'" -> E-Mail/Logic App).
    properties = {
        "schema": SCHEMA_VERSION,
        "truck_id": truck_id,
        "alarm": "true" if flags else "false",
        "flags": ",".join(flags),
    }
    return json.dumps(body, separators=(",", ":")), properties


def send_pending(
    conn: sqlite3.Connection,
    sender: Sender,
    state_path: str,
    truck_id: str = TRUCK_ID,
    max_rows: int = MAX_ROWS_PER_MESSAGE,
    max_messages: int = MAX_MESSAGES_PER_CYCLE,
    start_from: str = START_FROM,
    alarm_temp_c: float = ALARM_TEMP_C,
    mismatch_c: float = SENSOR_MISMATCH_C,
) -> int:
    """Schickt bis zu max_messages Batches. Gibt die Anzahl gesendeter Zeilen zurueck.

    Wirft die Exception des Senders weiter, der Cursor bleibt dann auf dem
    letzten erfolgreich gesendeten Batch stehen.
    """
    state = load_state(state_path)
    if state is None:
        state = {"last_sent_id": initial_cursor(conn, start_from)}
        save_state(state_path, state)

    sent = 0
    for _ in range(max_messages):
        rows = fetch_batch(conn, state["last_sent_id"], max_rows)
        if not rows:
            break
        body, properties = build_message(rows, truck_id, alarm_temp_c, mismatch_c)
        sender.send(body, properties)
        state["last_sent_id"] = rows[-1][0]
        save_state(state_path, state)
        sent += len(rows)
    return sent


class ThingSpeakSender:
    """Plan B ohne Azure: ThingSpeak (MathWorks), per HTTPS-Bulk-Update.

    Nimmt denselben Batch-Body wie der Azure-Sender entgegen, damit
    send_pending (Cursor, Store & Forward, Health-Flags) unveraendert bleibt.

    Einschraenkungen des kostenlosen Tarifs:
    - hoechstens 1 Request alle 15 s -> hier per MIN_REQUEST_SPACING erzwungen
    - ca. 3 Mio. Nachrichten/Jahr (~8.200/Tag), jeder Eintrag im Bulk-Update
      zaehlt einzeln -> nur jede DOWNSAMPLE-te Messung wird hochgeladen
      (5 s * 3 = 15-s-Raster, 5.760/Tag). Lokal bleiben alle Messungen in der DB.
    - bis zu 960 Eintraege pro Bulk-Update

    Feldbelegung des Kanals (so in ThingSpeak benennen, siehe README):
      field1 sensor_board_temp_c   field5 valve_angle
      field2 actor_board_temp_c    field6 sensor_board_raw
      field3 avg_temp_c            field7 actor_board_raw
      field4 fan_pwm               field8 sensor_board_digital
      status  "id=<lokale id>" + ggf. Health-Flags des Batches
    """

    URL = "https://api.thingspeak.com/channels/{channel_id}/bulk_update.json"
    MIN_REQUEST_SPACING = 15.5
    MAX_ENTRIES = 960

    def __init__(self, channel_id: str, write_api_key: str, downsample: int = 3, opener=None) -> None:
        self._url = self.URL.format(channel_id=channel_id)
        self._write_api_key = write_api_key
        self._downsample = max(1, downsample)
        self._opener = opener or urllib.request.urlopen
        self._last_request = None

    def build_updates(self, body: dict) -> list[dict]:
        idx = {name: i for i, name in enumerate(body["cols"])}
        rows = [r for r in body["rows"] if r[idx["id"]] % self._downsample == 0]
        # Alarme duerfen durchs Ausduennen nicht verloren gehen: letzte Zeile des
        # Batches immer mitnehmen, die Flags stehen dort im status-Feld.
        if body["rows"] and (not rows or rows[-1] is not body["rows"][-1]):
            rows.append(body["rows"][-1])
        updates = []
        for r in rows:
            sensor_c, actor_c = r[idx["sensor_board_temp_c"]], r[idx["actor_board_temp_c"]]
            updates.append({
                "created_at": r[idx["timestamp_utc"]],
                "field1": sensor_c,
                "field2": actor_c,
                "field3": round((sensor_c + actor_c) / 2, 2),
                "field4": r[idx["fan_pwm"]],
                "field5": r[idx["valve_angle"]],
                "field6": r[idx["sensor_board_raw"]],
                "field7": r[idx["actor_board_raw"]],
                "field8": r[idx["sensor_board_digital"]],
                "status": f"id={r[idx['id']]}",
            })
        if body["flags"]:
            updates[-1]["status"] += " flags=" + ",".join(body["flags"])
        return updates

    def send(self, body: str, properties: dict[str, str]) -> None:
        updates = self.build_updates(json.loads(body))
        if len(updates) > self.MAX_ENTRIES:
            raise ValueError(
                f"{len(updates)} Eintraege > {self.MAX_ENTRIES}: MAX_ROWS_PER_MESSAGE verkleinern"
            )
        if self._last_request is not None:
            wait = self.MIN_REQUEST_SPACING - (time.monotonic() - self._last_request)
            if wait > 0:
                time.sleep(wait)
        data = json.dumps({"write_api_key": self._write_api_key, "updates": updates}).encode()
        request = urllib.request.Request(
            self._url, data=data, headers={"Content-Type": "application/json"}, method="POST"
        )
        self._last_request = time.monotonic()
        with self._opener(request, timeout=30) as response:
            result = json.loads(response.read() or b"{}")
        # ThingSpeak antwortet mit {"success": true}; Fehler (401 falscher Key,
        # 429 zu schnell) wirft urlopen bereits als HTTPError -> Cursor bleibt stehen.
        if not result.get("success", False):
            raise RuntimeError(f"ThingSpeak hat den Batch abgelehnt: {result}")

    def shutdown(self) -> None:
        pass


class AzureIoTHubSender:
    """Sendet per azure-iot-device SDK (MQTT 3.1.1 ueber TLS) an den IoT Hub."""

    def __init__(self, connection_string: str, websockets: bool = False) -> None:
        from azure.iot.device import IoTHubDeviceClient

        self._client = IoTHubDeviceClient.create_from_connection_string(
            connection_string, websockets=websockets
        )

    def send(self, body: str, properties: dict[str, str]) -> None:
        from azure.iot.device import Message

        message = Message(body)
        # Ohne contentType/-Encoding kann das IoT-Hub-Routing den Body nicht
        # als JSON lesen und der Blob-Export speichert ihn Base64-kodiert.
        message.content_type = "application/json"
        message.content_encoding = "utf-8"
        message.custom_properties.update(properties)
        if not self._client.connected:
            self._client.connect()
        self._client.send_message(message)

    def shutdown(self) -> None:
        self._client.shutdown()


def create_sender():
    backend = os.environ.get("CLOUD_BACKEND", "azure")
    if backend == "thingspeak":
        return ThingSpeakSender(
            os.environ["THINGSPEAK_CHANNEL_ID"],
            os.environ["THINGSPEAK_WRITE_API_KEY"],
            downsample=_env_int("THINGSPEAK_DOWNSAMPLE", 3),
        )
    if backend == "azure":
        websockets = os.environ.get("IOTHUB_WEBSOCKETS", "0") == "1"
        return AzureIoTHubSender(os.environ["IOTHUB_DEVICE_CONNECTION_STRING"], websockets=websockets)
    raise ValueError(f"Unbekanntes CLOUD_BACKEND: {backend!r} (azure oder thingspeak)")


def main() -> None:
    sender = create_sender()
    print(
        f"cloud-bridge: backend={os.environ.get('CLOUD_BACKEND', 'azure')} truck_id={TRUCK_ID} "
        f"db={DB_PATH} interval={SEND_INTERVAL_SECONDS}s",
        flush=True,
    )
    try:
        while True:
            try:
                conn = open_db(DB_PATH)
                try:
                    sent = send_pending(conn, sender, STATE_PATH)
                finally:
                    conn.close()
                if sent:
                    print(f"cloud-bridge: {sent} Messungen gesendet", flush=True)
            except Exception as exc:  # Netz weg, DB gesperrt, ... -> naechster Zyklus
                print(f"cloud-bridge: Fehler, neuer Versuch im naechsten Zyklus: {exc!r}", flush=True)
            time.sleep(SEND_INTERVAL_SECONDS)
    finally:
        sender.shutdown()


if __name__ == "__main__":
    main()
