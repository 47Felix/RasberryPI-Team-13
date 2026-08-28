"""
Pi-Dashboard fuer den Digitalen Tresor (Kurzprojekt).

Track G: liest Events vom Arduino ueber Serial (USB), autodetect + Reconnect.
Track H: loggt jedes Event mit Zeitstempel in SQLite.
Track I: zeigt Verlauf + Live-Status auf einer Weboberflaeche.
Track J: Formular zum Aendern des Tresor-Codes (eigenes Admin-Passwort,
         nicht zu verwechseln mit dem Tresor-Code selbst).
Stretch: Discord-Alarm-Meldung, Live-Ampel + Versuchszaehler.

Siehe ObsidianGehirn/01 Projekt/Erweiterung - Raspberry Pi Dashboard.md
"""
import json
import os
import sqlite3
import threading
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import serial
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

BASE_DIR = Path(__file__).parent
DB_PATH = Path(os.environ.get("DASHBOARD_DB_PATH", BASE_DIR / "tresor.db"))
ADMIN_PASSWORD = os.environ.get("DASHBOARD_ADMIN_PASSWORD")
SECRET_KEY = os.environ.get("DASHBOARD_SECRET_KEY") or os.urandom(24).hex()
SERIAL_CANDIDATES = ["/dev/ttyACM0", "/dev/ttyACM1", "/dev/ttyUSB0", "/dev/ttyUSB1"]
# Fuer Tests ohne angeschlossenen Arduino: z.B. per socat einen virtuellen
# Seriell-Port bauen (siehe Erweiterung - Raspberry Pi Dashboard.md) und hier reinreichen.
_mock_port = os.environ.get("DASHBOARD_MOCK_SERIAL_PORT")
if _mock_port:
    SERIAL_CANDIDATES = [_mock_port] + SERIAL_CANDIDATES
SERIAL_BAUD = 9600
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_ALARM_CHANNEL_ID = os.environ.get("DISCORD_ALARM_CHANNEL_ID")

app = Flask(__name__)
app.secret_key = SECRET_KEY

serial_lock = threading.Lock()
serial_conn = {"port": None, "obj": None}
live_status = {"state": "unbekannt", "failed_attempts": 0, "last_event_at": None}


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            event TEXT NOT NULL,
            detail TEXT
        )"""
    )
    conn.commit()
    conn.close()


def log_event(event, detail=None):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO events (ts, event, detail) VALUES (?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), event, detail),
    )
    conn.commit()
    conn.close()


def notify_discord(message):
    if not DISCORD_BOT_TOKEN or not DISCORD_ALARM_CHANNEL_ID:
        print("[discord] Kein Token/Channel konfiguriert, Meldung wird nicht gesendet.")
        return
    try:
        req = urllib.request.Request(
            f"https://discord.com/api/v10/channels/{DISCORD_ALARM_CHANNEL_ID}/messages",
            data=json.dumps({"content": message}).encode(),
            headers={
                "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
                "Content-Type": "application/json",
                # Discord/Cloudflare blockt den generischen Python-urllib User-Agent (403) -
                # eigener User-Agent laut Discord-API-Doku empfohlen.
                "User-Agent": "TresorDashboardBot (https://github.com/47Felix/RasberryPI-Team-13, 1.0)",
            },
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[discord] Fehler beim Senden: {e}")


def handle_line(line):
    line = line.strip()
    if not line:
        return
    print(f"[arduino] {line}")
    now = datetime.now(timezone.utc).isoformat()
    if line == "EVENT:GRANTED":
        live_status.update(state="offen", failed_attempts=0, last_event_at=now)
        log_event("granted")
    elif line.startswith("EVENT:DENIED:"):
        attempt = line.split(":")[-1]
        live_status["state"] = "verschlossen"
        live_status["last_event_at"] = now
        try:
            live_status["failed_attempts"] = int(attempt)
        except ValueError:
            pass
        log_event("denied", detail=f"Versuch {attempt}")
    elif line == "EVENT:ALARM":
        live_status.update(state="alarm", last_event_at=now)
        log_event("alarm")
        notify_discord("🚨 **Tresor-Alarm ausgeloest!** Zu viele falsche Codes eingegeben.")
    elif line == "EVENT:LOCKED":
        live_status.update(state="verschlossen", last_event_at=now)
        log_event("locked", detail="Automatisch nach Zugang wieder verriegelt")
    elif line == "EVENT:READY":
        live_status.update(state="verschlossen", failed_attempts=0, last_event_at=now)
        log_event("ready", detail="Arduino gestartet/verbunden")
    elif line == "EVENT:CODE_UPDATED":
        log_event("code_updated", detail="vom Arduino bestaetigt")


def serial_reader_loop():
    while True:
        port = next((c for c in SERIAL_CANDIDATES if os.path.exists(c)), None)
        if not port:
            serial_conn["port"] = None
            serial_conn["obj"] = None
            time.sleep(5)
            continue
        try:
            with serial.Serial(port, SERIAL_BAUD, timeout=2) as ser:
                with serial_lock:
                    serial_conn["port"] = port
                    serial_conn["obj"] = ser
                print(f"[serial] verbunden auf {port}")
                while True:
                    raw = ser.readline()
                    if not raw:
                        continue
                    try:
                        handle_line(raw.decode("utf-8", errors="replace"))
                    except Exception as e:
                        print(f"[serial] Parse-Fehler: {e}")
        except serial.SerialException as e:
            print(f"[serial] Verbindungsfehler auf {port}: {e}")
            with serial_lock:
                serial_conn["port"] = None
                serial_conn["obj"] = None
            time.sleep(5)


def send_new_code(new_code):
    with serial_lock:
        ser = serial_conn.get("obj")
        if not ser:
            return False, "Arduino nicht verbunden"
        try:
            ser.write(f"SETCODE:{new_code}\n".encode())
            return True, None
        except Exception as e:
            return False, str(e)


@app.route("/api/status")
def api_status():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM events ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify(
        status=live_status,
        events=[dict(r) for r in rows],
        arduino_connected=serial_conn["obj"] is not None,
    )


@app.route("/")
def dashboard():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM events ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    return render_template(
        "dashboard.html",
        status=live_status,
        events=rows,
        arduino_connected=serial_conn["obj"] is not None,
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not ADMIN_PASSWORD:
        return "DASHBOARD_ADMIN_PASSWORD ist nicht gesetzt - Admin-Bereich deaktiviert.", 503

    if not session.get("admin_ok"):
        if request.method == "POST" and request.form.get("admin_password") == ADMIN_PASSWORD:
            session["admin_ok"] = True
            return redirect(url_for("admin"))
        error = "Falsches Passwort." if request.method == "POST" else None
        return render_template("admin_login.html", error=error)

    message = None
    if request.method == "POST" and "new_code" in request.form:
        new_code = request.form.get("new_code", "").strip()
        if not new_code.isdigit() or not (4 <= len(new_code) <= 8):
            message = ("error", "Code muss 4-8 Ziffern lang sein.")
        else:
            ok, err = send_new_code(new_code)
            message = ("success", f"Neuer Code gesendet: {new_code}") if ok else ("error", f"Fehler: {err}")

    return render_template(
        "admin.html", message=message, arduino_connected=serial_conn["obj"] is not None
    )


@app.route("/logout")
def logout():
    session.pop("admin_ok", None)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    init_db()
    threading.Thread(target=serial_reader_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
