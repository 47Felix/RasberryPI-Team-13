# Challenge III – Ice Truck in der Cloud (Azure IoT Hub)

Die Temperaturdaten aus Challenge I (`challenge_i.db` auf dem Pi) werden
automatisch in die Azure-Cloud übertragen, dort revisionssicher archiviert und
ausgewertet. Warum Azure IoT Hub und nicht AWS, Arduino Cloud oder ein eigener
Server, steht in [`ENTSCHEIDUNG.md`](ENTSCHEIDUNG.md), zusammen mit der Begründung
der fünf NIST-Merkmale.

## Architektur

```
 Truck (Edge)                                   Azure (EU-Region)
┌──────────────────────────────┐            ┌───────────────────────────────────────────┐
│ Arduino ─I2C─> app.py        │            │  IoT Hub (F1, PaaS)                       │
│                  │ SQLite    │  MQTT/TLS  │   ├─ Route "to-archive" ─> Blob Storage   │
│          challenge_i.db ─────┼──8883/443──┼─> │     (JSON, nach Datum, Nachweis ≥1 Jahr)│
│                  │ (Puffer)  │            │   └─ Route "to-builtin" ─> Event-Endpunkt │
│          cloud-bridge/       │            │                              │            │
│          bridge.py           │            │  Azure Data Explorer  <──────┘            │
│  (Cursor, Batches, Flags)    │            │   (KQL, Dashboard, Anomalie-Erkennung)    │
└──────────────────────────────┘            └───────────────────────────────────────────┘
```

- **Edge:** `cloud-bridge/bridge.py` liest nur lesend aus der bestehenden DB. Der
  Challenge-I-Regelkreis bleibt unverändert, der Truck regelt also auch ohne Netz weiter.
- **Store & Forward:** Die DB ist gleichzeitig der Puffer. Der Cursor
  (`bridge_state.json`) rückt erst nach erfolgreichem Senden weiter. Ist das Netz weg
  (Tunnel, Funkloch), holt die Bridge den Rückstand danach nach
  (`MAX_MESSAGES_PER_CYCLE` Batches pro Minute).
- **Vorauswertung am Edge:** Jeder Batch trägt `flags` (`temp_high`,
  `sensor_mismatch`, `sensor_stuck`) als Body-Feld und als Application Property
  `alarm=true/false`. Damit kann der IoT Hub Alarme ohne Parsen routen, etwa an eine
  Logic App, die eine E-Mail an die Werkstatt schickt.

## Nachrichtenformat

Ein Batch ≈ 1 Minute Messungen im Spaltenformat (spart Kontingent, siehe unten):

```json
{"schema":"icetruck-v1","truck_id":"icetruck-team13-1",
 "first_ts":"2026-09-30T08:00:00+00:00","last_ts":"2026-09-30T08:00:55+00:00",
 "min_temp_c":6.4,"max_temp_c":7.1,"flags":[],
 "cols":["id","timestamp_utc","sensor_board_raw","sensor_board_temp_c","sensor_board_digital",
         "actor_board_raw","actor_board_temp_c","fan_pwm","valve_angle"],
 "rows":[[4711,"2026-09-30T08:00:00+00:00",190,6.8,0,188,7.1,0,0], ...]}
```

## Kontingent (Tarif F1 = 0 €)

F1 erlaubt 8.000 Nachrichten pro Tag, abgerechnet in 0,5-KB-Blöcken.
`app.py` misst alle 5 s, das sind 17.280 Messungen pro Tag.

| Variante | Blöcke/Tag | passt in F1? |
|---|---|---|
| jede Messung einzeln als JSON-Objekt (~250 B) | 17.280 | ❌ |
| Batch/Minute als Objekt-Liste (~12×200 B) | ~7.200 | knapp |
| **Batch/Minute im Spaltenformat (~12×70 B)** | **~2.900** | ✅ Luft für Nachholen nach Funkloch |

Wird es trotzdem eng (mehrere Trucks), lohnt der Wechsel auf S1 (≈ 25 $/Monat,
400.000 Nachrichten/Tag) oder den Basic-Tarif B1. Der Code muss dafür nicht
geändert werden, das ist mit **Rapid Elasticity** gemeint.

## Einrichtung

### 1. Azure (einmalig, ca. 10 min)

Im Portal die **Cloud Shell** (Bash) öffnen, das Repo-Skript hochladen oder den Inhalt einfügen:

```bash
SUFFIX=team13x1 LOCATION=germanywestcentral bash setup.sh
```

Das Skript legt die Ressourcengruppe, den IoT Hub (F1), das Device, den Storage-Container
und beide Routen an und gibt am Ende den **Device-Connection-String** aus.

<details><summary>Falls die CLI-Befehle scheitern: dasselbe im Portal</summary>

1. *IoT Hub erstellen*: Tarif **Free (F1)**, Region Germany West Central / West Europe.
2. IoT Hub → *Geräte* → *Gerät hinzufügen*, ID `icetruck-team13-1`, Authentifizierung
   „Symmetrischer Schlüssel“ → primäre Verbindungszeichenfolge kopieren.
3. *Speicherkonto erstellen* (Standard LRS), Container `telemetry` anlegen (privat).
4. IoT Hub → *Nachrichtenrouting* → Route `to-archive`: Endpunkt „Storage“, Container
   `telemetry`, **Codierung JSON**, Quelle „Gerätetelemetrienachrichten“.
5. Zweite Route `to-builtin` auf den integrierten Endpunkt `events`. Ohne diese Route
   landet nach Schritt 4 nichts mehr am eingebauten Endpunkt.
</details>

### 2. Pi

```bash
cd ~/RasberryPI-Team-13 && git pull
cd Challenge-III-Ice-Truck-Cloud/Code/cloud-bridge
python3 -m venv venv && venv/bin/pip install -r requirements.txt
cp .env.example .env && chmod 600 .env
nano .env        # IOTHUB_DEVICE_CONNECTION_STRING eintragen
sudo cp cloud-bridge.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now cloud-bridge
journalctl -u cloud-bridge -f     # "... Messungen gesendet"
```

Blockt ein Netz Port 8883 (manche Schul-/Firmennetze), `IOTHUB_WEBSOCKETS=1` setzen.
Die Verbindung läuft dann als MQTT über WebSockets auf Port 443.

### 3. Prüfen, ob Daten ankommen

```bash
az iot hub monitor-events -n iothub-icetruck-team13x1 -d icetruck-team13-1 --properties app
```

Im Portal: Speicherkonto → Container `telemetry`. Nach ≤ 5 min liegen dort JSON-Dateien
unter `<hub>/<partition>/JJJJ/MM/TT/HH/mm`.

### 4. Visualisierung (Azure Data Explorer)

1. Kostenlosen Cluster anlegen: <https://dataexplorer.azure.com/freecluster>, Datenbank `icetruck`.
2. Tabelle, Mapping und Funktion aus [`azure/adx.kql`](azure/adx.kql) ausführen (Abschnitte 1 + 2).
3. *Get data*: Quelle **Event Hub / IoT Hub** (integrierter Endpunkt, Mapping
   `IceTruckMapping`) für Live-Daten. Alternativ **Azure Storage** → Container
   `telemetry` (Mapping `IceTruckBlobMapping`) für das Archiv.
   Welche Quellen der Free Cluster anbietet, beim Anlegen prüfen. Die Blob-Variante
   funktioniert in jedem Fall.
4. *Dashboards* → neue Kacheln mit den Abfragen aus Abschnitt 3 der `adx.kql`
   (Temperaturverlauf, Aktoren, Alarme, Sensor-Drift, Anomalien, Tagesnachweis).

## Tests

```bash
cd cloud-bridge && python3 -m venv venv && venv/bin/pip install -r requirements.txt -r requirements-dev.txt
venv/bin/python -m pytest -q tests
```

Die Tests laufen ohne Azure, mit einem Fake-Sender gegen eine echte SQLite-DB aus
`pi-backend/db.py`. Abgedeckt sind: erster Start, Nachholen im Batch, Limit pro Zyklus,
Cursor bleibt bei Sendefehler stehen, Health-Flags und dass die DB nur lesend geöffnet wird.

## Was noch fehlt / nur auf dem Pi prüfbar

- [ ] `setup.sh` im echten Azure-for-Students-Abo ausführen (Region-Policy der Schule prüfen)
- [ ] Bridge auf dem Pi installieren, Ende-zu-Ende gegen den echten Hub testen
- [ ] Offline-Test: WLAN am Pi trennen, 5 min warten, wieder verbinden. Der Rückstand muss nachkommen.
- [ ] ADX-Dashboard einrichten, Screenshots für die Präsentation
- [ ] Optional: Alarm-Route `alarm = 'true'` → Logic App → E-Mail an die Werkstatt
