---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  @import url('https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&display=swap');
  section { font-family: "Inter", "Helvetica Neue", Arial, sans-serif; color: #1c1f22; }
  h1, h2 { color: #1c1f22; letter-spacing: -0.01em; }
  h2 { border-bottom: 3px solid var(--p, #e2e6e8); padding-bottom: 0.2em; }
  h3 { color: var(--p, #6b6f73); font-weight: 700; font-family: "Kalam", cursive; font-size: 1.3em; }
  code { background: #f4f7f8; color: #124a5e; border-radius: 4px; }
  pre { background: #f4f7f8; border-left: 3px solid var(--p, #1c6e8c); border-radius: 0 6px 6px 0; }
  th { background: var(--pbg, #eaf4f7); color: var(--p, #124a5e); border-bottom: 2px solid #e2e6e8; }
  td, th { border-color: #e2e6e8; }
  li::marker { color: var(--p, #1c6e8c); }
  section.lead { background: var(--pbg, #ffffff); }
  section.p-anton { --p: #c2650a; --pbg: #fdf1e3; }
  section.p-felix { --p: #1f8a4c; --pbg: #e8f7ee; }
  section.p-dogan { --p: #9333c9; --pbg: #f5ecfc; }
  section.p-erik  { --p: #2f6fb0; --pbg: #eaf2fa; }
  section.p-team  { --p: #1c6e8c; --pbg: #eaf4f7; }
  .eyebrow { font-family: "Kalam", cursive; font-weight: 700; font-size: 0.65em; color: var(--p, #1c6e8c); }
  .chip { position: absolute; top: 28px; right: 40px; font-family: "Kalam", cursive; font-weight: 700; font-size: 0.5em; color: var(--p, #124a5e); background: var(--pbg, #eaf4f7); border: 1.5px dashed var(--p, #bfe0ea); padding: 0.3em 0.9em; border-radius: 10px; transform: rotate(-2deg); }
  .badge { display: inline-block; background: #ffe066; color: #5c4400; font-family: "Kalam", cursive; font-weight: 700; font-size: 0.55em; padding: 0.3em 0.8em; border-radius: 6px 14px 6px 14px; transform: rotate(-1.5deg); }
---

<!-- _class: "lead p-team" -->

<svg viewBox="0 0 100 60" width="72" height="43" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 8px auto;;color:var(--p,#1c6e8c)">
  <rect x="6" y="14" width="54" height="30" rx="4" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="62" y="24" width="24" height="20" rx="3" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="66" y="27" width="8" height="8" rx="1" fill="#ffffff" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="22" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="22" cy="48" r="2.5" fill="currentColor"/>
  <circle cx="78" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="78" cy="48" r="2.5" fill="currentColor"/>
  <line x1="24" y1="29" x2="42" y2="29" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <line x1="28.5" y1="21.2" x2="37.5" y2="36.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <line x1="37.5" y1="21.2" x2="28.5" y2="36.8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>

# The Ice Truck Problem(s)
### Team 13 – Technisches Fachgespräch Challenge I + II

Anton · Felix · Dogan · Erik · Smart Systems (BH4ab)

---


<!-- _class: "p-team" -->

## Worum geht's heute

- **Ein** Kühl-Truck-Szenario, zwei Challenges nacheinander gebaut:
  - **Challenge I** – Signale & Bus-Systeme (Sensoren, LEDs, I2C, Aktorik)
  - **Challenge II** – Kommunikation & Entwicklungswerkzeuge (MQTT, Node-RED, Handy)
- Roter Faden: Sensor → Arduino → I2C → Pi (Regellogik + SQL) → Aktor, danach zusätzlich → MQTT → Node-RED → Handy
- Wir gehen den Datenfluss entlang – jede:r erklärt den Abschnitt, an dem er/sie am tiefsten drin war

---


<!-- _class: "p-team" -->

## Team & Aufteilung

| Block | Thema | Wer |
|---|---|---|
| 1 | Hardware & Sensorik (Ch I) | Anton |
| 2 | Datenübertragung & Speicherung (Ch I) | Felix |
| 3 | Regellogik & Aktorik (Ch I) | Dogan |
| 4 | MQTT & Topics (Ch II) | Erik |
| 5 | Node-RED & Fernsteuerung (Ch II) | Anton |
| 6 | Mobiles Endgerät & Status (Ch II) | Felix |
| 7 | Fazit | Dogan |

*Gesamtdauer: ca. 15 Minuten Vortrag, danach Rückfragen · 5 Folien pro Person*

---


<!-- _class: "lead p-anton" -->

<svg viewBox="0 0 100 60" width="48" height="29" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 6px auto;;color:var(--p,#1c6e8c)">
  <rect x="6" y="14" width="54" height="30" rx="4" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="62" y="24" width="24" height="20" rx="3" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="22" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="78" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
</svg>

<div class="eyebrow">Challenge I</div>

# Block 1: Hardware & Sensorik
### Anton

---


<!-- _class: "p-anton" -->

<span class="chip">Challenge I</span>

## Systemarchitektur Challenge I

<svg viewBox="0 0 900 300" width="100%" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#c2650a"/>
    </marker>
  </defs>
  <rect x="40" y="20" width="330" height="130" rx="8" fill="#fdf1e3" stroke="#c2650a" stroke-width="2"/>
  <text x="58" y="46" font-size="16" font-weight="700" fill="#7a3d05">Sensor-Board · I2C 0x08</text>
  <text x="58" y="70" font-size="13" fill="#333">KY-028 Temperatursensor → A0</text>
  <text x="58" y="92" font-size="13" fill="#333">Status-LED (PWM) → D9</text>
  <rect x="530" y="20" width="330" height="130" rx="8" fill="#fdf1e3" stroke="#c2650a" stroke-width="2"/>
  <text x="548" y="46" font-size="16" font-weight="700" fill="#7a3d05">Aktor-Board · I2C 0x09</text>
  <text x="548" y="70" font-size="13" fill="#333">KY-028 Temperatursensor → A0</text>
  <text x="548" y="92" font-size="13" fill="#333">Status-LED (PWM) → D5</text>
  <text x="548" y="114" font-size="13" fill="#333">Lüfter (Software-PWM) → D4</text>
  <text x="548" y="136" font-size="13" fill="#333">Servo/Ventil → D6</text>
  <line x1="205" y1="150" x2="205" y2="192" stroke="#c2650a" stroke-width="2"/>
  <line x1="695" y1="150" x2="695" y2="192" stroke="#c2650a" stroke-width="2"/>
  <line x1="205" y1="192" x2="695" y2="192" stroke="#c2650a" stroke-width="2"/>
  <text x="450" y="184" text-anchor="middle" font-size="13" fill="#7a3d05">I2C · SDA/SCL · Pull-ups auf 3,3V</text>
  <line x1="450" y1="192" x2="450" y2="216" stroke="#c2650a" stroke-width="2.5" marker-end="url(#arrow1)"/>
  <rect x="250" y="222" width="400" height="66" rx="8" fill="#c2650a"/>
  <text x="450" y="250" text-anchor="middle" font-size="15" font-weight="700" fill="#ffffff">Raspberry Pi — pi-backend/app.py</text>
  <text x="450" y="272" text-anchor="middle" font-size="12.5" fill="#fdf1e3">liest beide Boards · rechnet &amp; regelt · loggt in SQLite</text>
</svg>

Zwei Arduino Unos, ein gemeinsamer I2C-Bus, ein Pi als Gehirn.

---


<!-- _class: "p-anton" -->

<span class="chip">Challenge I</span>
<div class="eyebrow">Bewertung: Sensor funktionstüchtig (5 Pkt)</div>

## Sensorik: von DHT22 zu 2× KY-028

- Ursprünglich geplant: DHT22 (Temp/Feuchte) auf dem Aktor-Board
- **Problem:** `readTemperature()`/`readHumidity()` lieferten ab dem ersten Aufruf nach jedem Reset nur `NaN` – per Serial direkt verifiziert, Verkabelung mehrfach gegengeprüft
- **Entscheidung:** DHT22 raus, stattdessen ein zweites KY-028 – beide Boards messen jetzt nach demselben Prinzip
- Beide Sensoren einzeln mit einem Referenzthermometer kalibriert (2 Punkte je Board)

---


<!-- _class: "p-anton" -->

<span class="chip">Challenge I</span>
<div class="eyebrow">Bewertung: LED + Helligkeit folgt Sensor (4 + 6 Pkt)</div>

## LED zeigt den Messwert

<span class="badge">👉 Live-Demo</span>

- Jedes Board hat eine eigene PWM-LED, die **lokal auf dem Arduino** aus dem Rohwert berechnet wird – kein I2C-Umweg nötig
- Kalibrierte Eckwerte pro Board (z.B. Aktor-Board: `RAW_AT_LED_FULL=129`, `RAW_AT_LED_OFF=385`), dazwischen linear interpoliert
- LED voll hell ab ~30°C, aus ab ~-10°C
- Wir zeigen das jetzt kurz live: Finger auf den Sensor, Helligkeit ändert sich in Echtzeit

---


<!-- _class: "lead p-felix" -->

<svg viewBox="0 0 100 60" width="48" height="29" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 6px auto;;color:var(--p,#1c6e8c)">
  <rect x="6" y="14" width="54" height="30" rx="4" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="62" y="24" width="24" height="20" rx="3" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="22" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="78" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
</svg>

<div class="eyebrow">Challenge I</div>

# Block 2: Datenübertragung & Speicherung
### Felix

---


<!-- _class: "p-felix" -->

<span class="chip">Challenge I</span>
<div class="eyebrow">Bewertung: Kommunikation mehrerer Arduinos mit dem Pi (5 Pkt)</div>

## I2C-Kommunikation Pi ↔ beide Arduinos

- Pi liest beide Boards per I2C aus (`smbus2`, `/dev/i2c-1`), Adressen `0x08` / `0x09`
- **Bug, den wir gefunden haben:** `smbus2`s `write_i2c_block_data()`/`read_i2c_block_data()` sprechen die SMBus-Block-Konvention (ein Register-Byte vorab, erstes Byte = Längenangabe) – unsere Sketches senden aber rohe Bytes ohne Präfix
- Symptom: Lüfter- und Ventil-Sollwerte vertauscht, Sensorwerte um ein Byte verschoben
- **Fix:** `smbus2.i2c_msg.read()`/`.write()` statt der Block-Funktionen – exakte Byte-Anzahl, kein Präfix

---


<!-- _class: "p-felix" -->

<span class="chip">Challenge I</span>
<div class="eyebrow">Bewertung: Datenformate dargestellt (5 Pkt)</div>

## Datenformate der Sensoren

- Jedes Board sendet **2 rohe Bytes** (KY-028-Analogwert) über I2C – keine Umrechnung in der Firmware
- Umrechnung passiert komplett im Pi-Backend (`calibration.py`): 2-Punkt-lineare Interpolation, **pro Board eigene Kurve**

| Board | 23°C → Rohwert | 30°C → Rohwert |
|---|---|---|
| Sensor-Board | 212 | 160 |
| Aktor-Board | 174 | 126 (bei 30,5°C) |

---


<!-- _class: "p-felix" -->

<span class="chip">Challenge I</span>
<div class="eyebrow">Bewertung: Messdaten in SQL-DB protokolliert (4 Pkt)</div>

## Messdaten in SQLite protokolliert

- Tabelle `readings` (`db.py`), eine Zeile je Poll-Zyklus (alle 5s)
- Felder: `timestamp`, `sensor_board_raw`, `sensor_board_temp_c`, `actor_board_raw`, `actor_board_temp_c`, `fan_pwm`, `valve_angle`
- Läuft als systemd-Service (`challenge-i-backend.service`) – startet automatisch bei jedem Boot, kein manuelles Starten nötig
- Rohwert **und** kalibrierter Wert werden geloggt – falls die Kalibrierung später nachjustiert wird, bleiben die Rohdaten auswertbar

---


<!-- _class: "lead p-dogan" -->

<svg viewBox="0 0 100 60" width="48" height="29" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 6px auto;;color:var(--p,#1c6e8c)">
  <rect x="6" y="14" width="54" height="30" rx="4" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="62" y="24" width="24" height="20" rx="3" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="22" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="78" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
</svg>

<div class="eyebrow">Challenge I</div>

# Block 3: Regellogik & Aktorik
### Dogan

---


<!-- _class: "p-dogan" -->

<span class="chip">Challenge I</span>

## Regellogik: zwei Kühlstufen

```python
# rules.py – vereinfacht
if temp < 25°C:        fan = 0,          valve = 0
if 25°C <= temp < 28°C: fan = 40..255,   valve = 0     # Stufe 1
if temp >= 28°C:        fan = 255,       valve = 30..180  # Stufe 2
```

- Berechnungsgrundlage: **Mittelwert** beider kalibrierter Temperaturen
- Schwellwerte (`FAN_ON_TEMP_C`, `VALVE_ON_TEMP_C`) sind aktuell Tischtest-Platzhalter, nicht die echten Betriebswerte aus der Moodle-Aufgabenstellung – offener Punkt

---


<!-- _class: "p-dogan" -->

<span class="chip">Challenge I</span>
<div class="eyebrow">Bewertung: Lüfter über Transistor vom Pi gesteuert (8 Pkt)</div>

## Lüfter: Ansteuerung über Transistor

<span class="badge">👉 Live-Demo</span>

- DC-Lüfter hängt über einen Transistor/H-Brücke am Arduino, der Pi liefert den PWM-Sollwert per I2C
- **Die Odyssee dahin:** D9 (Timer1) kollidierte mit der Servo-Bibliothek → auf D3 (Timer2) umverkabelt → Timer2 lief auf diesem Board generell nicht (vermutlich LGT8F328P-Klon-Chip statt echtem ATmega328P) → **Software-PWM auf D4**, per `digitalWrite()` und `millis()`
- Danach drehte der Lüfter erst **rückwärts** (schneller bei Kälte) – Board schaltet active-low, Logik invertiert, jetzt korrekt

---


<!-- _class: "p-dogan" -->

<span class="chip">Challenge I</span>
<div class="eyebrow">Bewertung: Servomotor vom Pi gesteuert (3 Pkt)</div>

## Ventil: Servo-Ansteuerung

<span class="badge">👉 Live-Demo</span>

- Servo am Ventil, Signal auf D6, Standard-Arduino-`Servo`-Bibliothek
- Winkel 0–180° direkt aus `rules.py`, vom Pi per I2C an den Aktor-Arduino geschrieben
- Genau diese Bibliothek belegt intern Timer1 – **das** war die Ursache für den Lüfter-Konflikt auf D9/D10 (siehe vorherige Folie)

---


<!-- _class: "p-dogan" -->

<span class="chip">Challenge I</span>
<div class="eyebrow">Bewertung: Szenario sinnvoll erweitert (5 Pkt)</div>

## Szenario sinnvoll erweitert

- Zwei physische Boards statt nur des geforderten Minimums (Sensor + Platzhalter-Slave) – echte 2-Sensor-Redundanz
- Kalibrierung nicht geschätzt, sondern mit Referenzthermometer gemessen
- Automatischer Systemd-Start, kein manuelles Hochfahren nötig
- `control_state.py`/`set_control.py`: manueller Override-Kanal – die Brücke, die Challenge II die Fernsteuerung erst ermöglicht (dazu gleich mehr)

---


<!-- _class: "lead p-erik" -->

<svg viewBox="0 0 100 60" width="48" height="29" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 6px auto;;color:var(--p,#1c6e8c)">
  <rect x="6" y="14" width="54" height="30" rx="4" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="62" y="24" width="24" height="20" rx="3" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="22" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="78" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
</svg>

<div class="eyebrow">Challenge II</div>

# Block 4: MQTT & Topics
### Erik

---


<!-- _class: "p-erik" -->

<span class="chip">Challenge II</span>

## Von Challenge I zu Challenge II

<svg viewBox="0 0 900 290" width="100%" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M0,0 L10,5 L0,10 z" fill="#2f6fb0"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="160" height="56" rx="7" fill="#eaf2fa" stroke="#2f6fb0" stroke-width="2"/>
  <text x="100" y="54" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1d4a78">SQLite</text>
  <text x="100" y="72" text-anchor="middle" font-size="11" fill="#333">challenge_i.db</text>
  <rect x="250" y="30" width="160" height="56" rx="7" fill="#eaf2fa" stroke="#2f6fb0" stroke-width="2"/>
  <text x="330" y="54" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1d4a78">Node-RED</text>
  <text x="330" y="72" text-anchor="middle" font-size="11" fill="#333">Flow</text>
  <rect x="480" y="30" width="180" height="56" rx="7" fill="#eaf2fa" stroke="#2f6fb0" stroke-width="2"/>
  <text x="570" y="54" text-anchor="middle" font-size="12.5" font-weight="700" fill="#1d4a78">MQTT-Broker</text>
  <text x="570" y="72" text-anchor="middle" font-size="11" fill="#333">Mosquitto (Pi)</text>
  <rect x="710" y="30" width="170" height="56" rx="7" fill="#2f6fb0"/>
  <text x="795" y="54" text-anchor="middle" font-size="12.5" font-weight="700" fill="#ffffff">Handy</text>
  <text x="795" y="72" text-anchor="middle" font-size="11" fill="#eaf2fa">MQTT Dash / Explorer</text>
  <line x1="180" y1="58" x2="248" y2="58" stroke="#2f6fb0" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="214" y="49" text-anchor="middle" font-size="10.5" fill="#1d4a78">alle 5s</text>
  <line x1="410" y1="58" x2="478" y2="58" stroke="#2f6fb0" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="444" y="49" text-anchor="middle" font-size="10.5" fill="#1d4a78">publish</text>
  <line x1="660" y1="58" x2="708" y2="58" stroke="#2f6fb0" stroke-width="2" marker-end="url(#arrow2)"/>
  <text x="684" y="49" text-anchor="middle" font-size="10.5" fill="#1d4a78">MQTT</text>
  <line x1="795" y1="86" x2="795" y2="172" stroke="#2f6fb0" stroke-width="2"/>
  <line x1="330" y1="172" x2="795" y2="172" stroke="#2f6fb0" stroke-width="2"/>
  <text x="562" y="164" text-anchor="middle" font-size="11" fill="#1d4a78">control/* (Fernsteuerung)</text>
  <line x1="330" y1="172" x2="330" y2="88" stroke="#2f6fb0" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="330" y1="172" x2="330" y2="208" stroke="#2f6fb0" stroke-width="2" marker-end="url(#arrow2)"/>
  <rect x="180" y="212" width="300" height="56" rx="7" fill="#eaf2fa" stroke="#2f6fb0" stroke-width="2"/>
  <text x="330" y="236" text-anchor="middle" font-size="11.5" font-weight="700" fill="#1d4a78">set_control.py → control_state.json</text>
  <text x="330" y="254" text-anchor="middle" font-size="11" fill="#333">app.py liest jeden Poll-Zyklus → I2C</text>
</svg>

Die lokale Regelung aus Challenge I läuft automatisch – aber niemand steht dauerhaft neben dem Pi. Challenge II macht Zustand **sichtbar** und Aktoren **fernsteuerbar**, ohne die Ch-I-Logik zu ersetzen.

---


<!-- _class: "p-erik" -->

<span class="chip">Challenge II</span>
<div class="eyebrow">Bewertung: Kommunikation über MQTT realisiert (8 Pkt)</div>

## MQTT-Broker: lokaler Mosquitto

- Entscheidung: lokaler Mosquitto auf dem Pi statt ITECH-Broker (war schon installiert)
- Eigene Config (`team13-icetruck.conf`): Listener auf `0.0.0.0:1883` statt nur `localhost`, **Passwort-Pflicht** (`allow_anonymous false`)
- ACL beschränkt den Nutzer `team13-1` strikt auf `team13-1/#`
- Getestet: authentifizierter Roundtrip ✅, anonyme Verbindung abgelehnt ✅, Publish außerhalb der ACL wird verworfen ✅

---


<!-- _class: "p-erik" -->

<span class="chip">Challenge II</span>
<div class="eyebrow">Bewertung: Organisation/Hierarchie der Topics (5 Pkt)</div>

## Topic-Schema & Hierarchie

Präfix: `team13-1/icetruck/`

| Richtung | Topics | Payload |
|---|---|---|
| Pi → Handy (retained) | `sensors/sensor_board_temp_c`, `sensors/actor_board_temp_c`, `actuators/fan_pwm`, `actuators/valve_angle`, `status` | Zahl bzw. JSON |
| Handy → Pi | `control/mode/set`, `control/fan_pwm/set`, `control/valve_angle/set` | `auto`/`manual`, Zahl |

**Retained**, damit ein neu verbundenes Handy sofort den letzten Stand sieht, statt 5s auf den nächsten Poll zu warten.

---


<!-- _class: "lead p-anton" -->

<svg viewBox="0 0 100 60" width="48" height="29" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 6px auto;;color:var(--p,#1c6e8c)">
  <rect x="6" y="14" width="54" height="30" rx="4" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="62" y="24" width="24" height="20" rx="3" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="22" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="78" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
</svg>

<div class="eyebrow">Challenge II</div>

# Block 5: Node-RED & Fernsteuerung
### Anton

---


<!-- _class: "p-anton" -->

<span class="chip">Challenge II</span>
<div class="eyebrow">Bewertung: Steuerung über Node-RED realisiert (9 Pkt)</div>

## Node-RED als Integrationsschicht

- Ein Flow liest alle 5s die letzte Zeile aus `challenge_i.db` (`node-red-node-sqlite`) und publiziert sie auf die Topics aus dem Schema
- Gleicher Flow abonniert `control/#`, validiert eingehende Befehle, loggt sie nach `control_log.ndjson`
- Per Exec-Node ruft er `set_control.py` auf – das schreibt den gewünschten Zustand in `control_state.json`
- Damit ist Node-RED die Brücke in **beide** Richtungen zwischen Pi-Backend und MQTT

---


<!-- _class: "p-anton" -->

<span class="chip">Challenge II</span>
<div class="eyebrow">Bewertung: Zusätzliche Funktionen realisiert (8 Pkt)</div>

## Fernsteuerung: auto/manual als Extra-Feature

- `control/mode/set` schaltet zwischen automatischer Regellogik (`rules.py`) und manuellem Override vom Handy
- Im `manual`-Modus liest `app.py` `control_state.json` jeden Poll-Zyklus und schreibt die vom Handy gesendeten `fan_pwm`/`valve_angle`-Werte **direkt per I2C** – statt der berechneten Werte
- Modul-seitig komplett getestet (`pytest`, 16/16 grün), auf der echten Hardware End-to-End noch nicht final verifiziert (siehe Status gleich)

---


<!-- _class: "lead p-felix" -->

<svg viewBox="0 0 100 60" width="48" height="29" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 6px auto;;color:var(--p,#1c6e8c)">
  <rect x="6" y="14" width="54" height="30" rx="4" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="62" y="24" width="24" height="20" rx="3" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="22" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="78" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
</svg>

<div class="eyebrow">Challenge II</div>

# Block 6: Mobiles Endgerät & Status
### Felix

---


<!-- _class: "p-felix" -->

<span class="chip">Challenge II</span>
<div class="eyebrow">Bewertung: weiteres Endgerät über MQTT eingebunden (8 Pkt)</div>

## Mobiles Endgerät statt Eigenbau-App

- Aufgabenstellung erlaubt explizit MQTT Dash oder MQTT Explorer statt einer selbstgebauten App – genau das nutzen wir
- Einzelwert-Topics als reiner Zahlen-Payload → passen direkt in numerische Widgets/Gauges
- `status`-Topic zusätzlich als JSON für alle, die lieber Rohdaten sehen (z.B. MQTT Explorer)
- Retained Topics sorgen dafür, dass ein Widget sofort einen Wert zeigt, nicht erst nach dem nächsten Poll

---


<!-- _class: "p-felix" -->

<span class="chip">Challenge II</span>

## Stand heute & offene Punkte

**Läuft:** I2C-Bug behoben, Regellogik pytest-getestet, SQLite-Logging live im Systemd-Service, Node-RED-Flow importiert und mit echten Live-Daten verifiziert (Lese-Richtung)

**Noch offen, braucht kurz Root-Zugriff auf dem Pi:**
- Broker-Auth hängt seit 24.09. in einer Reconnect-Schleife – Passwort/Credentials müssen neu gesetzt werden
- Backend-Service hält noch alten Code im Speicher (kein `control_state`-Support) – braucht `systemctl restart`
- MQTT Dash auf einem echten Handy noch nicht konfiguriert

**Ausblick:** Challenge III (Cloud-Speicherung/-Auswertung) – noch nicht begonnen

---


<!-- _class: "lead p-dogan" -->

<svg viewBox="0 0 100 60" width="48" height="29" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto 6px auto;;color:var(--p,#1c6e8c)">
  <rect x="6" y="14" width="54" height="30" rx="4" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <rect x="62" y="24" width="24" height="20" rx="3" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="22" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
  <circle cx="78" cy="48" r="7" fill="#ffffff" stroke="currentColor" stroke-width="3"/>
</svg>

# Fazit
### Dogan

---


<!-- _class: "p-dogan" -->

## Lessons Learned

- Erst auf der echten Hardware messen, nicht raten – der DHT22 "war kaputt", nicht unser Code; der PWM-Timer-Konflikt war chip-spezifisch, keine Verkabelungsfrage
- Modul-Tests (pytest, Mock-I2C) geben Sicherheit *vor* dem Hardware-Test, ersetzen ihn aber nicht – der End-to-End-Test auf echter Hardware fand nochmal eigene Bugs
- Ehrliches Logging (Rohwert **und** kalibrierter Wert) macht Fehlersuche später erst möglich

---


<!-- _class: "lead p-team" -->

# Danke! 🎉
### Fragen?
