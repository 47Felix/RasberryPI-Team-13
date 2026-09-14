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

## Was noch fehlt (braucht physischen Hardware-Zugriff)

- [ ] **Beide Arduino-Sketches kompilieren + flashen** und auf echten Boards testen (Track A/B/D) - Verkabelung von Thermistor/Fotowiderstand, Tuerkontakt, zwei LEDs, Transistor/H-Bruecke fuer den Luefter, Servo fuer das Ventil
- [ ] **I2C-Verkabelung** SDA/SCL beider Arduinos mit dem Pi verbinden, gemeinsame GND, Pull-up-Widerstaende pruefen falls noetig (Track C/E)
- [ ] **`RealI2CBus` gegen echten Bus testen** (`smbus2`, `/dev/i2c-1` auf dem Pi - Issue [#168](https://github.com/47Felix/RasberryPI-Team-13/issues/168) muss zuerst erledigt sein)
- [ ] **Schwellwerte in `rules.py` kalibrieren** (`FAN_ON_THRESHOLD`, `VALVE_ON_THRESHOLD` sind Platzhalter) - haengt an der eigentlichen Aufgabenstellung aus dem Moodle-Kurs (Issue [#167](https://github.com/47Felix/RasberryPI-Team-13/issues/167), noch nicht freigeschaltet) und an der realen Sensor-Kalibrierung
- [ ] **`app.py` als systemd-Service** auf dem Pi einrichten (gleiches Muster wie `tresor-dashboard.service`), sobald obiges steht

## Wo was liegt

- `sensor-arduino/sensor_arduino.ino` - Track A, B, C (Arduino-Seite)
- `actor-arduino/actor_arduino.ino` - Track D, E (Arduino-Seite)
- `pi-backend/` - Track C, E, F (Pi-Seite): `hardware.py` (I2C real+mock), `rules.py` (Regellogik), `db.py` (SQLite), `app.py` (Hauptschleife), `tests/`
