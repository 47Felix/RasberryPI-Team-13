#!/usr/bin/env python3
import importlib.util
spec = importlib.util.spec_from_file_location("bp", "build_pptx.py")
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

from pptx.util import Inches
from pptx.enum.text import PP_ALIGN

N = 0
def nxt():
    global N
    N += 1
    return N

# ---------- Slide 1: Title ----------
bp.lead_slide(nxt(), "team", "The Ice Truck Problem(s)",
              "Team 13 – Technisches Fachgespräch Challenge I + II",
              extra="Anton · Felix · Dogan · Erik · Smart Systems (BH4ab)")

# ---------- Slide 2: Worum geht's heute ----------
bp.content_slide(nxt(), "team", None, "Überblick", "Worum geht's heute",
    bullets=[
        "**Ein** Kühl-Truck-Szenario, zwei Challenges nacheinander gebaut:",
        ("**Challenge I** – Signale & Bus-Systeme (Sensoren, LEDs, I2C, Aktorik)", 1),
        ("**Challenge II** – Kommunikation & Entwicklungswerkzeuge (MQTT, Node-RED, Handy)", 1),
        "Roter Faden: Sensor → Arduino → I2C → Pi (Regellogik + SQL) → Aktor, danach zusätzlich → MQTT → Node-RED → Handy",
        "Wir gehen den Datenfluss entlang – jede:r erklärt den Abschnitt, an dem er/sie am tiefsten drin war",
    ])

# ---------- Slide 3: Team & Aufteilung ----------
s = bp.add_slide(); bp.set_bg(s, bp.WHITE)
body_y = bp.content_header(s, "team", nxt(), None, "Überblick", "Team & Aufteilung")
rows = [
    ["Block", "Thema", "Wer"],
    ["1", "Hardware & Sensorik (Ch I)", "Anton"],
    ["2", "Datenübertragung & Speicherung (Ch I)", "Felix"],
    ["3", "Regellogik & Aktorik (Ch I)", "Dogan"],
    ["4", "MQTT & Topics (Ch II)", "Erik"],
    ["5", "Node-RED & Fernsteuerung (Ch II)", "Anton"],
    ["6", "Mobiles Endgerät & Status (Ch II)", "Felix"],
    ["7", "Fazit", "Dogan"],
]
bp.simple_table(s, 0.75, body_y + 0.15, 9.5, rows, [0.9, 6.3, 2.3], "team", row_h=0.5)
bp.add_text(s, 0.75, body_y + 0.15 + 0.5 * len(rows) + 0.25, 11.5, 0.4,
            "Gesamtdauer: ca. 15 Minuten Vortrag, danach Rückfragen · 5 Folien pro Person",
            size=13, color=bp.MUTED, italic=True)

# ---------- Slide 4: Block 1 divider ----------
bp.lead_slide(nxt(), "anton", "Block 1: Hardware & Sensorik", "Anton", eyebrow="Challenge I")

# ---------- Slide 5: Systemarchitektur (diagram) ----------
s = bp.add_slide(); bp.set_bg(s, bp.WHITE)
body_y = bp.content_header(s, "anton", nxt(), "Challenge I", "Hardware & Sensorik", "Systemarchitektur Challenge I")
y0 = body_y + 0.2
bp.diagram_box(s, 0.75, y0, 5.2, 1.5, "Sensor-Board · I2C 0x08",
                ["KY-028 Temperatursensor → A0", "Status-LED (PWM) → D9"], "anton")
bp.diagram_box(s, 7.38, y0, 5.2, 1.5, "Aktor-Board · I2C 0x09",
                ["KY-028 Temperatursensor → A0", "Status-LED (PWM) → D5",
                 "Lüfter (Software-PWM) → D4", "Servo/Ventil → D6"], "anton")
bus_y = y0 + 1.8
bp.add_line(s, 3.35, y0 + 1.5, 3.35, bus_y, bp.PEOPLE["anton"]["p"], 1.5)
bp.add_line(s, 9.98, y0 + 1.5, 9.98, bus_y, bp.PEOPLE["anton"]["p"], 1.5)
bp.add_line(s, 3.35, bus_y, 9.98, bus_y, bp.PEOPLE["anton"]["p"], 1.5)
bp.add_text(s, 3.35, bus_y - 0.32, 6.63, 0.26, "I2C · SDA/SCL · Pull-ups auf 3,3V",
            size=11, color=bp.PEOPLE["anton"]["dark"], align=PP_ALIGN.CENTER, bold=True)
bp.diagram_arrow_v(s, 6.665, bus_y, bus_y + 0.35, bp.PEOPLE["anton"]["p"])
pi_y = bus_y + 0.35
bp.diagram_box(s, 4.9, pi_y, 3.55, 0.85, "Raspberry Pi — pi-backend/app.py",
                ["liest beide Boards · rechnet & regelt · loggt in SQLite"], "anton", filled=True)
bp.add_text(s, 0.75, pi_y + 1.05, 11.5, 0.4, "Zwei Arduino Unos, ein gemeinsamer I2C-Bus, ein Pi als Gehirn.",
            size=13, color=bp.FG)

# ---------- Slide 6: Sensorik ----------
bp.content_slide(nxt(), "anton", "Challenge I", "Hardware & Sensorik · Bewertung: Sensor funktionstüchtig (5 Pkt)",
    "Sensorik: von DHT22 zu 2× KY-028",
    bullets=[
        "Ursprünglich geplant: DHT22 (Temp/Feuchte) auf dem Aktor-Board",
        "**Problem:** `readTemperature()`/`readHumidity()` lieferten ab dem ersten Aufruf nach jedem Reset nur `NaN` – per Serial direkt verifiziert, Verkabelung mehrfach gegengeprüft",
        "**Entscheidung:** DHT22 raus, stattdessen ein zweites KY-028 – beide Boards messen jetzt nach demselben Prinzip",
        "Beide Sensoren einzeln mit einem Referenzthermometer kalibriert (2 Punkte je Board)",
    ])

# ---------- Slide 7: LED ----------
bp.content_slide(nxt(), "anton", "Challenge I", "Hardware & Sensorik · Bewertung: LED + Helligkeit folgt Sensor (4 + 6 Pkt)",
    "LED zeigt den Messwert", badge=True,
    bullets=[
        "Jedes Board hat eine eigene PWM-LED, die **lokal auf dem Arduino** aus dem Rohwert berechnet wird – kein I2C-Umweg nötig",
        "Kalibrierte Eckwerte pro Board (z.B. Aktor-Board: `RAW_AT_LED_FULL=129`, `RAW_AT_LED_OFF=385`), dazwischen linear interpoliert",
        "LED voll hell ab ~30°C, aus ab ~-10°C",
        "Wir zeigen das jetzt kurz live: Finger auf den Sensor, Helligkeit ändert sich in Echtzeit",
    ])

# ---------- Slide 8: Block 2 divider ----------
bp.lead_slide(nxt(), "felix", "Block 2: Datenübertragung & Speicherung", "Felix", eyebrow="Challenge I")

# ---------- Slide 9: I2C-Kommunikation ----------
bp.content_slide(nxt(), "felix", "Challenge I", "Datenübertragung · Bewertung: Kommunikation mehrerer Arduinos mit dem Pi (5 Pkt)",
    "I2C-Kommunikation Pi ↔ beide Arduinos",
    bullets=[
        "Pi liest beide Boards per I2C aus (`smbus2`, `/dev/i2c-1`), Adressen `0x08` / `0x09`",
        "**Bug, den wir gefunden haben:** `smbus2`s `write_i2c_block_data()`/`read_i2c_block_data()` sprechen die SMBus-Block-Konvention (ein Register-Byte vorab, erstes Byte = Längenangabe) – unsere Sketches senden aber rohe Bytes ohne Präfix",
        "Symptom: Lüfter- und Ventil-Sollwerte vertauscht, Sensorwerte um ein Byte verschoben",
        "**Fix:** `smbus2.i2c_msg.read()`/`.write()` statt der Block-Funktionen – exakte Byte-Anzahl, kein Präfix",
    ])

# ---------- Slide 10: Datenformate (table) ----------
bp.content_slide(nxt(), "felix", "Challenge I", "Datenübertragung · Bewertung: Datenformate dargestellt (5 Pkt)",
    "Datenformate der Sensoren",
    table=[["Board", "23°C → Rohwert", "30°C → Rohwert"],
           ["Sensor-Board", "212", "160"],
           ["Aktor-Board", "174", "126 (bei 30,5°C)"]],
    table_widths=[4.5, 3.7, 3.6],
    bullets=[
        "Jedes Board sendet **2 rohe Bytes** (KY-028-Analogwert) über I2C – keine Umrechnung in der Firmware",
        "Umrechnung passiert komplett im Pi-Backend (`calibration.py`): 2-Punkt-lineare Interpolation, **pro Board eigene Kurve**",
    ])

# ---------- Slide 11: SQLite ----------
bp.content_slide(nxt(), "felix", "Challenge I", "Datenübertragung · Bewertung: Messdaten in SQL-DB protokolliert (4 Pkt)",
    "Messdaten in SQLite protokolliert",
    bullets=[
        "Tabelle `readings` (`db.py`), eine Zeile je Poll-Zyklus (alle 5s)",
        "Felder: `timestamp`, `sensor_board_raw`, `sensor_board_temp_c`, `actor_board_raw`, `actor_board_temp_c`, `fan_pwm`, `valve_angle`",
        "Läuft als systemd-Service (`challenge-i-backend.service`) – startet automatisch bei jedem Boot",
        "Rohwert **und** kalibrierter Wert werden geloggt – falls die Kalibrierung später nachjustiert wird, bleiben die Rohdaten auswertbar",
    ])

# ---------- Slide 12: Block 3 divider ----------
bp.lead_slide(nxt(), "dogan", "Block 3: Regellogik & Aktorik", "Dogan", eyebrow="Challenge I")

# ---------- Slide 13: Regellogik (code) ----------
bp.content_slide(nxt(), "dogan", "Challenge I", "Regellogik & Aktorik", "Regellogik: zwei Kühlstufen",
    code=("# rules.py – vereinfacht\n"
          "if temp < 25°C:         fan = 0,         valve = 0\n"
          "if 25°C <= temp < 28°C: fan = 40..255,   valve = 0     # Stufe 1\n"
          "if temp >= 28°C:         fan = 255,       valve = 30..180  # Stufe 2", 1.35),
    bullets=[
        "Berechnungsgrundlage: **Mittelwert** beider kalibrierter Temperaturen",
        "Schwellwerte sind aktuell Tischtest-Platzhalter, nicht die echten Betriebswerte aus der Moodle-Aufgabenstellung – offener Punkt",
    ])

# ---------- Slide 14: Lüfter ----------
bp.content_slide(nxt(), "dogan", "Challenge I", "Regellogik & Aktorik · Bewertung: Lüfter über Transistor vom Pi gesteuert (8 Pkt)",
    "Lüfter: Ansteuerung über Transistor", badge=True,
    bullets=[
        "DC-Lüfter hängt über einen Transistor/H-Brücke am Arduino, der Pi liefert den PWM-Sollwert per I2C",
        "**Die Odyssee dahin:** D9 (Timer1) kollidierte mit der Servo-Bibliothek → auf D3 (Timer2) umverkabelt → Timer2 lief auf diesem Board generell nicht (vermutlich LGT8F328P-Klon-Chip statt echtem ATmega328P) → **Software-PWM auf D4**, per `digitalWrite()` und `millis()`",
        "Danach drehte der Lüfter erst **rückwärts** (schneller bei Kälte) – Board schaltet active-low, Logik invertiert, jetzt korrekt",
    ])

# ---------- Slide 15: Servo ----------
bp.content_slide(nxt(), "dogan", "Challenge I", "Regellogik & Aktorik · Bewertung: Servomotor vom Pi gesteuert (3 Pkt)",
    "Ventil: Servo-Ansteuerung", badge=True,
    bullets=[
        "Servo am Ventil, Signal auf D6, Standard-Arduino-`Servo`-Bibliothek",
        "Winkel 0–180° direkt aus `rules.py`, vom Pi per I2C an den Aktor-Arduino geschrieben",
        "Genau diese Bibliothek belegt intern Timer1 – **das** war die Ursache für den Lüfter-Konflikt auf D9/D10 (siehe vorherige Folie)",
    ])

# ---------- Slide 16: Szenario erweitert ----------
bp.content_slide(nxt(), "dogan", "Challenge I", "Regellogik & Aktorik · Bewertung: Szenario sinnvoll erweitert (5 Pkt)",
    "Szenario sinnvoll erweitert",
    bullets=[
        "Zwei physische Boards statt nur des geforderten Minimums (Sensor + Platzhalter-Slave) – echte 2-Sensor-Redundanz",
        "Kalibrierung nicht geschätzt, sondern mit Referenzthermometer gemessen",
        "Automatischer Systemd-Start, kein manuelles Hochfahren nötig",
        "`control_state.py`/`set_control.py`: manueller Override-Kanal – die Brücke zu Challenge II",
    ])

# ---------- Slide 17: Block 4 divider ----------
bp.lead_slide(nxt(), "erik", "Block 4: MQTT & Topics", "Erik", eyebrow="Challenge II")

# ---------- Slide 18: Von Challenge I zu II (diagram) ----------
s = bp.add_slide(); bp.set_bg(s, bp.WHITE)
body_y = bp.content_header(s, "erik", nxt(), "Challenge II", "MQTT & Topics", "Von Challenge I zu Challenge II")
y0 = body_y + 0.15
bw, bh, gap = 2.55, 0.82, 0.55
xs = [0.75]
for _ in range(3):
    xs.append(xs[-1] + bw + gap)
bp.diagram_box(s, xs[0], y0, bw, bh, "SQLite", ["challenge_i.db"], "erik")
bp.diagram_box(s, xs[1], y0, bw, bh, "Node-RED", ["Flow"], "erik")
bp.diagram_box(s, xs[2], y0, bw, bh, "MQTT-Broker", ["Mosquitto (Pi)"], "erik")
bp.diagram_box(s, xs[3], y0, bw, bh, "Handy", ["MQTT Dash / Explorer"], "erik", filled=True)
mid_y = y0 + bh / 2
bp.diagram_arrow_h(s, xs[0] + bw, xs[1], mid_y, bp.PEOPLE["erik"]["p"], "alle 5s")
bp.diagram_arrow_h(s, xs[1] + bw, xs[2], mid_y, bp.PEOPLE["erik"]["p"], "publish")
bp.diagram_arrow_h(s, xs[2] + bw, xs[3], mid_y, bp.PEOPLE["erik"]["p"], "MQTT")
ret_y = y0 + bh + 0.95
node_cx = xs[1] + bw / 2
handy_cx = xs[3] + bw / 2
bp.add_line(s, handy_cx, y0 + bh, handy_cx, ret_y, bp.PEOPLE["erik"]["p"], 1.5)
bp.add_line(s, node_cx, ret_y, handy_cx, ret_y, bp.PEOPLE["erik"]["p"], 1.5)
bp.add_text(s, node_cx, ret_y - 0.32, handy_cx - node_cx, 0.26, "control/* (Fernsteuerung)",
            size=10.5, color=bp.PEOPLE["erik"]["dark"], align=PP_ALIGN.CENTER, bold=True)
bp.diagram_arrow_v(s, node_cx, ret_y, y0 + bh, bp.PEOPLE["erik"]["p"])
exec_y = ret_y + 0.35
bp.diagram_arrow_v(s, node_cx, ret_y, exec_y, bp.PEOPLE["erik"]["p"])
bp.diagram_box(s, node_cx - 1.75, exec_y, 3.5, 0.8, "set_control.py → control_state.json",
                ["app.py liest jeden Poll-Zyklus → I2C"], "erik")
bp.add_text(s, 0.75, exec_y + 1.0, 11.5, 0.6,
            "Die lokale Regelung aus Challenge I läuft automatisch – Challenge II macht Zustand **sichtbar** "
            "und Aktoren **fernsteuerbar**, ohne die Ch-I-Logik zu ersetzen.",
            size=12.5, color=bp.FG)

# ---------- Slide 19: MQTT-Broker ----------
bp.content_slide(nxt(), "erik", "Challenge II", "MQTT & Topics · Bewertung: Kommunikation über MQTT realisiert (8 Pkt)",
    "MQTT-Broker: lokaler Mosquitto",
    bullets=[
        "Entscheidung: lokaler Mosquitto auf dem Pi statt ITECH-Broker (war schon installiert)",
        "Eigene Config: Listener auf `0.0.0.0:1883` statt nur `localhost`, **Passwort-Pflicht** (`allow_anonymous false`)",
        "ACL beschränkt den Nutzer `team13-1` strikt auf `team13-1/#`",
        "Getestet: authentifizierter Roundtrip, anonyme Verbindung abgelehnt, Publish außerhalb der ACL wird verworfen",
    ])

# ---------- Slide 20: Topic-Schema (table) ----------
bp.content_slide(nxt(), "erik", "Challenge II", "MQTT & Topics · Bewertung: Organisation/Hierarchie der Topics (5 Pkt)",
    "Topic-Schema & Hierarchie",
    table=[["Richtung", "Topics", "Payload"],
           ["Pi → Handy (retained)", "sensors/*_temp_c, actuators/fan_pwm, actuators/valve_angle, status", "Zahl bzw. JSON"],
           ["Handy → Pi", "control/mode/set, control/fan_pwm/set, control/valve_angle/set", "auto/manual, Zahl"]],
    table_widths=[2.6, 6.6, 2.6],
    table_caption="Präfix: team13-1/icetruck/",
    bullets=[
        "**Retained**, damit ein neu verbundenes Handy sofort den letzten Stand sieht, statt 5s auf den nächsten Poll zu warten",
    ])

# ---------- Slide 21: Block 5 divider ----------
bp.lead_slide(nxt(), "anton", "Block 5: Node-RED & Fernsteuerung", "Anton", eyebrow="Challenge II")

# ---------- Slide 22: Node-RED ----------
bp.content_slide(nxt(), "anton", "Challenge II", "Node-RED & Fernsteuerung · Bewertung: Steuerung über Node-RED realisiert (9 Pkt)",
    "Node-RED als Integrationsschicht",
    bullets=[
        "Ein Flow liest alle 5s die letzte Zeile aus `challenge_i.db` (`node-red-node-sqlite`) und publiziert sie auf die Topics aus dem Schema",
        "Gleicher Flow abonniert `control/#`, validiert eingehende Befehle, loggt sie nach `control_log.ndjson`",
        "Per Exec-Node ruft er `set_control.py` auf – das schreibt den gewünschten Zustand in `control_state.json`",
        "Damit ist Node-RED die Brücke in **beide** Richtungen zwischen Pi-Backend und MQTT",
    ])

# ---------- Slide 23: Fernsteuerung ----------
bp.content_slide(nxt(), "anton", "Challenge II", "Node-RED & Fernsteuerung · Bewertung: Zusätzliche Funktionen realisiert (8 Pkt)",
    "Fernsteuerung: auto/manual als Extra-Feature",
    bullets=[
        "`control/mode/set` schaltet zwischen automatischer Regellogik (`rules.py`) und manuellem Override vom Handy",
        "Im `manual`-Modus liest `app.py` `control_state.json` jeden Poll-Zyklus und schreibt die vom Handy gesendeten Werte **direkt per I2C** – statt der berechneten Werte",
        "Modul-seitig komplett getestet (`pytest`, 16/16 grün), auf der echten Hardware End-to-End noch nicht final verifiziert",
    ])

# ---------- Slide 24: Block 6 divider ----------
bp.lead_slide(nxt(), "felix", "Block 6: Mobiles Endgerät & Status", "Felix", eyebrow="Challenge II")

# ---------- Slide 25: Mobiles Endgerät ----------
bp.content_slide(nxt(), "felix", "Challenge II", "Mobiles Endgerät & Status · Bewertung: weiteres Endgerät über MQTT eingebunden (8 Pkt)",
    "Mobiles Endgerät statt Eigenbau-App",
    bullets=[
        "Aufgabenstellung erlaubt explizit MQTT Dash oder MQTT Explorer statt einer selbstgebauten App – genau das nutzen wir",
        "Einzelwert-Topics als reiner Zahlen-Payload → passen direkt in numerische Widgets/Gauges",
        "`status`-Topic zusätzlich als JSON für alle, die lieber Rohdaten sehen (z.B. MQTT Explorer)",
        "Retained Topics sorgen dafür, dass ein Widget sofort einen Wert zeigt, nicht erst nach dem nächsten Poll",
    ])

# ---------- Slide 26: Stand heute ----------
bp.content_slide(nxt(), "felix", "Challenge II", None, "Stand heute & offene Punkte",
    bullets=[
        "**Läuft:** I2C-Bug behoben, Regellogik pytest-getestet, SQLite-Logging live im Systemd-Service, Node-RED-Flow importiert und mit echten Live-Daten verifiziert (Lese-Richtung)",
        "**Noch offen, braucht kurz Root-Zugriff auf dem Pi:**",
        ("Broker-Auth hängt seit 24.09. in einer Reconnect-Schleife – Passwort/Credentials müssen neu gesetzt werden", 1),
        ("Backend-Service hält noch alten Code im Speicher (kein `control_state`-Support) – braucht `systemctl restart`", 1),
        ("MQTT Dash auf einem echten Handy noch nicht konfiguriert", 1),
        "**Ausblick:** Challenge III (Cloud-Speicherung/-Auswertung) – noch nicht begonnen",
    ])

# ---------- Slide 27: Fazit divider ----------
bp.lead_slide(nxt(), "dogan", "Fazit", "Dogan")

# ---------- Slide 28: Lessons Learned ----------
bp.content_slide(nxt(), "dogan", None, "Fazit", "Lessons Learned",
    bullets=[
        "Erst auf der echten Hardware messen, nicht raten – der DHT22 \"war kaputt\", nicht unser Code; der PWM-Timer-Konflikt war chip-spezifisch, keine Verkabelungsfrage",
        "Modul-Tests (pytest, Mock-I2C) geben Sicherheit *vor* dem Hardware-Test, ersetzen ihn aber nicht – der End-to-End-Test auf echter Hardware fand nochmal eigene Bugs",
        "Ehrliches Logging (Rohwert **und** kalibrierter Wert) macht Fehlersuche später erst möglich",
    ])

# ---------- Slide 29: Danke ----------
bp.lead_slide(nxt(), "team", "Danke!", "Fragen?", icon=False)

assert N == 29, N
bp.prs.save("ice-truck-praesentation.pptx")
print("Saved", N, "slides -> ice-truck-praesentation.pptx")
