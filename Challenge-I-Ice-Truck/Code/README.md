# Challenge I – The Ice Truck Problem: Code

Scaffolding fuer die Tracks A-F (siehe Issues [#176](https://github.com/47Felix/RasberryPI-Team-13/issues/176)-[#181](https://github.com/47Felix/RasberryPI-Team-13/issues/181)). Erstellt ohne Zugriff auf echte Hardware (kein Netzwerkzugriff auf den Pi aus dieser Sandbox, keine Arduino-Boards angeschlossen) - siehe "Was noch fehlt" unten, bevor irgendetwas davon als "fertig" gilt.

## Architektur

```
Sensor-Arduino (I2C-Slave 0x08)      Aktor-Arduino (I2C-Slave 0x09)
  KY-028 Analogwert (A0)               KY-028 Analogwert (A0) + LED (D5)
  LED fuer KY-028 (D9)                 Luefter (PWM, D9)
                                       Ventil-Servo (D6)
        │                                  │           ▲
        │ I2C read                         │ I2C read  │ I2C write
        ▼                                  ▼           │
                 pi-backend/app.py (Track F)
                   - liest beide KY-028-Rohwerte (siehe Hardware-Update 5)
                   - calibration.py: Rohwert -> Grad Celsius je Sensor
                   - rules.py: 2-Stufen-Regellogik aus dem Mittelwert
                     beider kalibrierter Temperaturen
                   - schreibt Aktor-Sollwerte
                   - loggt jede Messung in SQLite (beide Sensorwerte,
                     roh + kalibriert)
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

`sensor_arduino/` und `actor_arduino/` waren zwischenzeitlich (14.-17.09.) nur die Referenz fuer den Zwei-Board-Entwurf, waehrend real ein einzelnes Board (`ice_truck_single_board.ino`) verkabelt war - siehe Hardware-Update 4, das ist inzwischen wieder ueberholt.

## Hardware-Update 4 (Felix, 17.09.): zurueck auf zwei Boards, jetzt mit den echten Sensoren

Team hat jetzt zwei physische Arduino Unos zur Verfuegung und ist zurueck zum Zwei-Board-Entwurf gewechselt - `ice_truck_single_board.ino` ist damit wieder **nicht** die aktuell verkabelte Hardware (bleibt als Referenz stehen). Unterschied zum urspruenglichen Zwei-Board-Entwurf: die tatsaechlich verbauten Sensoren sind DHT22 (nicht DHT11) und ein KY-028-Modul (nicht Thermistor/LDR-Platzhalter), der DHT22 haengt physisch am **Aktor**-Board (nicht am Sensor-Board), und der Tuerkontakt/Taster aus dem urspruenglichen Entwurf ist komplett entfallen (kein entsprechendes Bauteil verkabelt):

| Board | Bauteil | Rolle | Pin(s) |
|---|---|---|---|
| Board 2, `sensor_arduino.ino` (I2C 0x08) | KY-028 (Analogausgang) | Sensor, analog, unkalibriert | AO → A0 |
| Board 2 | LED fuer KY-028 | Helligkeitsanzeige | → D9 (PWM) |
| Board 1, `actor_arduino.ino` (I2C 0x09) | DHT22 (Temp/Feuchte) | Sensor, digital/Bus-Protokoll | Signal → D2 |
| Board 1 | LED fuer DHT22 | Helligkeitsanzeige | → D5 (PWM) |
| Board 1 | Luefter (DC-Motor/H-Bruecke) | Aktor | PWM → D9 |
| Board 1 | Servo (Ventil) | Aktor | Signal → D6 |

I2C zum Pi (ohne Levelshifter, beide Boards am selben Bus): A4 (SDA) und A5 (SCL) beider Arduinos parallel an Pi GPIO2/GPIO3, gemeinsames GND. Pull-ups (4,7kΩ) von SDA/SCL auf **3,3V** (nicht 5V!), zusaetzlich auf beiden Arduinos nach `Wire.begin(...)` die internen 5V-Pull-ups per `digitalWrite(SDA, LOW); digitalWrite(SCL, LOW);` abschalten - sonst zieht der Bus Richtung 5V und gefaehrdet die Pi-GPIOs.

`pi-backend` liest den DHT22-Wert vom **Aktor**-Board (0x09) fuer die Kuehlstufen-Entscheidung (`rules.py`); der KY-028-Rohwert vom Sensor-Board (0x08) ist unkalibriert (kein bekannter Thermistor-Beta-Wert) und fliesst aktuell nur ins Logging (`db.py`), nicht in die Regellogik. *(Ueberholt, siehe Hardware-Update 5 - der DHT22 ist inzwischen komplett raus.)*

## Hardware-Update 5 (Felix, 17.09.): DHT22 durch zweites KY-028 ersetzt

Der DHT22 auf dem Aktor-Board hat **nie** eine gueltige Messung geliefert: `dht.readHumidity()`/`readTemperature()` gaben ab dem allerersten Aufruf nach jedem Reset durchgehend `NaN` zurueck (per Serial direkt verifiziert, nicht nur ueber I2C/den Pi) - Verkabelung (Pull-up, GND, Signalkabel) wurde mehrfach gegengeprueft, I2C selbst lief parallel fehlerfrei. Statt weiter zu raten, hat das Team den DHT22 durch ein zweites KY-028-Modul ersetzt - beide Boards haben jetzt exakt dasselbe Sensorprinzip:

| Board | Bauteil | Rolle | Pin(s) |
|---|---|---|---|
| Board 2, `sensor_arduino.ino` (I2C 0x08) | KY-028 (Analogausgang) | Sensor, analog, unkalibriert | AO → A0 |
| Board 2 | LED fuer KY-028 | Helligkeitsanzeige | → D9 (PWM) |
| Board 1, `actor_arduino.ino` (I2C 0x09) | KY-028 (Analogausgang) | Sensor, analog, unkalibriert | AO → A0 |
| Board 1 | LED fuer KY-028 | Helligkeitsanzeige | → D5 (PWM) |
| Board 1 | Luefter (DC-Motor/H-Bruecke) | Aktor | PWM → D9 |
| Board 1 | Servo (Ventil) | Aktor | Signal → D6 |

Beide Boards senden jetzt nur noch 2 Bytes (Rohwert) statt der bisherigen 4 (Temp/Feuchte) auf dem Aktor-Board. Die Umrechnung Rohwert → Grad Celsius passiert komplett im Pi-Backend (`pi-backend/calibration.py`, 2-Punkt-lineare Interpolation je Sensor) statt in der Firmware - **inzwischen kalibriert** (17./18.09., Felix, per Referenzthermometer: Sensor-Board 23.0C→raw 212 / 30.0C→raw 160, Aktor-Board 23.0C→raw 174 / 30.5C→raw 126; Details inkl. Drift-Hinweis zum Aktor-Board siehe Docstring in `calibration.py`). Die Kuehlstufen-Entscheidung (`rules.py`) nutzt den Mittelwert der beiden kalibrierten Temperaturen, mit Tischtest-Schwellwerten (noch nicht den echten Betriebswerten aus der Moodle-Aufgabenstellung).

## Hardware-Update 3 (15.09.2026, Issue #191): Sensor ist ein DHT22, nicht DHT11

Der Temp/Feuchte-Sensor hat ein weisses Gehaeuse (DHT22), nicht das blaue DHT11-Gehaeuse, das urspruenglich angenommen wurde. Der Sketch hatte `DHTTYPE` faelschlich auf `DHT11` stehen - DHT11 und DHT22 kodieren ihre Rohbytes unterschiedlich, DHT11-Parsing auf einem DHT22-Bytestream ergab die konstant ~20-22 Grad zu niedrigen Werte aus Issue #191, kein Verkabelungs-/Pull-up-Problem. Fix: `DHTTYPE` auf `DHT22` umgestellt (`ice_truck_single_board.ino`), der bisherige `+20°C`-Kalibrierungs-Offset ist damit hinfaellig und entfernt. **Noch nicht an echter Hardware verifiziert** - naechster Schritt bei Hardware-Zugriff: neu flashen, echte Werte gegen ein zweites Thermometer pruefen, Issue #191 danach schliessen.

## Was noch fehlt (braucht physischen Hardware-Zugriff)

- [x] **Beide Arduino-Sketches (jetzt beide KY-028) kompilieren + flashen** und auf den echten Boards testen
- [x] **I2C-Verkabelung** wie oben herstellen und mit `i2cdetect -y 1` auf `0x08` und `0x09` verifizieren
- [x] **`RealI2CBus` gegen echten Bus testen** (`smbus2`, `/dev/i2c-1` auf dem Pi)
- [x] **Beide KY-028 kalibrieren** (`pi-backend/calibration.py`, `SENSOR_BOARD_CALIBRATION`/`ACTOR_BOARD_CALIBRATION`) - je Sensor zwei Referenzpunkte per Referenzthermometer gemessen (17./18.09., Felix); Aktor-Board-Ruhewert driftet spuerbar (Eigenerwaermung), ggf. per Sensor-Board-Proxy neu abgleichen (siehe Docstring)
- [ ] **Schwellwerte in `rules.py` kalibrieren** (`FAN_ON_TEMP_C`, `VALVE_ON_TEMP_C` sind Platzhalter) - haengt an der eigentlichen Aufgabenstellung aus dem Moodle-Kurs (Issue [#167](https://github.com/47Felix/RasberryPI-Team-13/issues/167)) und an der realen Sensor-Kalibrierung
- [ ] **`app.py` als systemd-Service** auf dem Pi einrichten (gleiches Muster wie `tresor-dashboard.service`), sobald obiges steht

## Wo was liegt

- `sensor_arduino/sensor_arduino.ino` - **aktuell verkabelt** (Board 2, I2C 0x08): KY-028, Tracks A/B/C
- `actor_arduino/actor_arduino.ino` - **aktuell verkabelt** (Board 1, I2C 0x09): KY-028 + Luefter/Servo, Tracks D/E (kein DHT22 mehr, siehe Hardware-Update 5)
- `ice_truck_single_board/ice_truck_single_board.ino` - fruehere Ein-Board-Verkabelung (14.-17.09., siehe Hardware-Update 2), aktuell **nicht** verkabelt, bleibt als Referenz
- `pi-backend/` - Track C, E, F (Pi-Seite): `hardware.py` (I2C real+mock, zwei Adressen), `calibration.py` (Rohwert → Grad Celsius, kalibriert), `rules.py` (Regellogik), `db.py` (SQLite), `app.py` (Hauptschleife), `read_live.py` (manuelles Live-Auslesen beider Boards, nuetzlich zum Kalibrieren), `tests/`
