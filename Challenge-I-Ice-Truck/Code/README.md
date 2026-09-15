# Challenge I – The Ice Truck Problem: Code

Scaffolding fuer die Tracks A-F (siehe Issues [#176](https://github.com/47Felix/RasberryPI-Team-13/issues/176)-[#181](https://github.com/47Felix/RasberryPI-Team-13/issues/181)). Erstellt ohne Zugriff auf echte Hardware (kein Netzwerkzugriff auf den Pi aus dieser Sandbox, keine Arduino-Boards angeschlossen) - siehe "Was noch fehlt" unten, bevor irgendetwas davon als "fertig" gilt.

## Architektur

```
Sensor-Arduino (I2C-Slave 0x08)      Aktor-Arduino (I2C-Slave 0x09)
  Thermistor/Fotowiderstand (A0)       Luefter (PWM, D9)
  Tuerkontakt-Schalter (D2)            Ventil-Servo (D6)
  LED je Sensor (D9, D10)
        │                                     ▲
        │ I2C read                            │ I2C write
        ▼                                     │
                 pi-backend/app.py (Track F)
                   - liest Sensor-Arduino
                   - rules.py: 2-Stufen-Regellogik
                   - schreibt Aktor-Sollwerte
                   - loggt jede Messung in SQLite
```

## Design-Entscheidung: Sensor-Arduino ist sein eigener I2C-Slave

Track A verlangt ein Sensor-Beispiel im "Bus-Protokoll"-Format und erlaubt dafuer explizit einen zusaetzlichen Arduino nur als I2C-Slave-Platzhalter. Stattdessen macht `sensor_arduino.ino` sich selbst zum I2C-Slave (Adresse 0x08) - deckt Track A (Bus-Format) und Track C (Pi liest Sensor-Arduino per I2C) in einem Sketch ab, ein Board weniger im Aufbau. Falls das Team lieber einen dedizierten dritten Arduino moechte (z.B. weil ein echtes I2C-Sensormodul aus dem Kit verfuegbar ist), ist das ein kleiner Umbau, keine Neukonzeption.

## Was echt verifiziert ist (ohne Hardware moeglich)

```bash
cd Challenge-I-Ice-Truck/Code/pi-backend
python3 -m pytest tests/ -v
```

9 Tests, alle gruen: Regellogik (`rules.py`, beide Kuehlstufen + Tuer-Boost + Grenzwerte), SQLite-Logging (`db.py`), und der Mock-I2C-Bus (`hardware.py`, `MockI2CBus`) im Zusammenspiel - gleiches Prinzip wie der `socat`-Mock-Test fuer den Tresor-Arduino (siehe `Tresor-Kurzprojekt/Code/pi-dashboard`, Vault-Notiz "Erweiterung - Raspberry Pi Dashboard").

## Hardware-Update (Felix, 14.09., siehe Issue #179)

Fruehere Annahme "kein Luefter vorhanden" war falsch/vorlaeufig - siehe naechster Abschnitt, ein Luefter ist tatsaechlich angeschlossen. Fuer den `pi-backend`/I2C-Split-Entwurf (`rules.py`, `sensor_arduino`, `actor_arduino`) bleibt trotzdem dokumentiert, wie beide Kuehlstufen ohne Luefter allein ueber `valve_angle` liefen (kleiner Winkel = leicht, groesserer Winkel = stark) - relevant, falls der Luefter mal wieder abgeklemmt wird.

## Hardware-Update 2 (Felix, 14.09.): reale Verkabelung ist EIN Board, nicht zwei

Tatsaechlich verkabelt ist bisher ein einzelner Arduino Uno mit allen drei Sensoren, allen drei LEDs und beiden Aktoren gleichzeitig - nicht die urspruenglich angenommene Zwei-Arduino-I2C-Aufteilung (`sensor_arduino` + `actor_arduino`). Neuer Sketch `ice_truck_single_board/ice_truck_single_board.ino` deckt das ab:

| Bauteil | Rolle | Pin(s) |
|---|---|---|
| DHT22 (Temp/Feuchte) | Sensor, digital/Bus-Protokoll | Signal → D2 |
| Fotowiderstand (LDR) | Sensor, analog | über Spannungsteiler → A0 |
| Kippschalter/Taster | Sensor, digital 1/0 | → D4 |
| LED für DHT22 | Helligkeitsanzeige | → D5 (PWM) |
| LED für Fotowiderstand | Helligkeitsanzeige | → D6 (PWM) |
| LED für Schalter | Helligkeitsanzeige | → D11 (PWM) |
| Lüfter (DC-Motor) über Transistor | Aktor | Basis über 1kΩ → D3 (PWM) |
| Servo (Ventil) | Aktor | Signal → D9 |
| — reserviert für später — | I2C zum Pi | A4 (SDA), A5 (SCL) frei lassen |

Wichtig: der Taster an D4 ist ein **Taster**, kein Kippschalter - haelt seinen Zustand nicht selbst. Im Sketch deshalb als entprellter Software-Toggle umgesetzt (jeder Tastendruck kehrt den gespeicherten Zustand um), nicht als direkter Pin-Read wie beim urspruenglichen `sensor_arduino.ino`-Entwurf.

Kuehlstufen-Logik laeuft in dieser Version lokal auf dem Arduino (`computeCoolingStage()`/`applyCoolingStage()` im neuen Sketch), basierend auf der DHT22-Temperatur - nicht auf dem LDR (der misst Licht, nicht Temperatur). I2C zum Pi ist vorbereitet (Slave-Adresse 0x08, liefert Temp/Feuchte/LDR/Taster auf Anfrage) aber SDA/SCL bewusst noch unverkabelt ("reserviert für später") - sobald das steht, kann die Kuehlstufen-Entscheidung nach `pi-backend/rules.py` wandern (Issue #180), analog zum urspruenglichen Zwei-Board-Entwurf.

`sensor_arduino/` und `actor_arduino/` bleiben als Referenz fuer den Zwei-Board-Entwurf stehen (z.B. falls ein zweites Board dazukommt), sind aber **nicht** die aktuell verkabelte Hardware.

## Hardware-Update 3 (15.09.2026, Issue #191): Sensor ist ein DHT22, nicht DHT11

Der Temp/Feuchte-Sensor hat ein weisses Gehaeuse (DHT22), nicht das blaue DHT11-Gehaeuse, das urspruenglich angenommen wurde. Der Sketch hatte `DHTTYPE` faelschlich auf `DHT11` stehen - DHT11 und DHT22 kodieren ihre Rohbytes unterschiedlich, DHT11-Parsing auf einem DHT22-Bytestream ergab die konstant ~20-22 Grad zu niedrigen Werte aus Issue #191, kein Verkabelungs-/Pull-up-Problem. Fix: `DHTTYPE` auf `DHT22` umgestellt (`ice_truck_single_board.ino`), der bisherige `+20°C`-Kalibrierungs-Offset ist damit hinfaellig und entfernt. **Noch nicht an echter Hardware verifiziert** - naechster Schritt bei Hardware-Zugriff: neu flashen, echte Werte gegen ein zweites Thermometer pruefen, Issue #191 danach schliessen.

## Was noch fehlt (braucht physischen Hardware-Zugriff)

- [ ] **Sketch neu flashen + DHT22-Fix verifizieren** (Issue #191, siehe Hardware-Update 3 oben) - echte Temperatur/Feuchte gegen ein zweites Messgeraet gegenpruefen
- [ ] **Beide Arduino-Sketches kompilieren + flashen** und auf echten Boards testen (Track A/B/D) - Verkabelung von Thermistor/Fotowiderstand, Tuerkontakt, zwei LEDs, Servo fuer das Ventil (Luefter/Transistor siehe Hardware-Update oben)
- [ ] **I2C-Verkabelung** SDA/SCL beider Arduinos mit dem Pi verbinden, gemeinsame GND, Pull-up-Widerstaende pruefen falls noetig (Track C/E)
- [ ] **`RealI2CBus` gegen echten Bus testen** (`smbus2`, `/dev/i2c-1` auf dem Pi - Issue [#168](https://github.com/47Felix/RasberryPI-Team-13/issues/168) muss zuerst erledigt sein)
- [ ] **Schwellwerte in `rules.py` kalibrieren** (`FAN_ON_THRESHOLD`, `VALVE_ON_THRESHOLD` sind Platzhalter) - haengt an der eigentlichen Aufgabenstellung aus dem Moodle-Kurs (Issue [#167](https://github.com/47Felix/RasberryPI-Team-13/issues/167), noch nicht freigeschaltet) und an der realen Sensor-Kalibrierung
- [ ] **`app.py` als systemd-Service** auf dem Pi einrichten (gleiches Muster wie `tresor-dashboard.service`), sobald obiges steht

## Wo was liegt

- `ice_truck_single_board/ice_truck_single_board.ino` - **aktuell verkabelte Hardware** (ein Board, alle Sensoren+Aktoren, siehe Hardware-Update 2 oben), Tracks A/B/D lokal, C vorbereitet
- `sensor_arduino/sensor_arduino.ino` - Track A, B, C (Zwei-Board-Entwurf, Referenz)
- `actor_arduino/actor_arduino.ino` - Track D, E (Zwei-Board-Entwurf, Referenz)
- `pi-backend/` - Track C, E, F (Pi-Seite): `hardware.py` (I2C real+mock), `rules.py` (Regellogik), `db.py` (SQLite), `app.py` (Hauptschleife), `tests/`
