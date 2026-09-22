# Challenge I – The Ice Truck Problem: Code

Scaffolding fuer die Tracks A-F (siehe Issues [#176](https://github.com/47Felix/RasberryPI-Team-13/issues/176)-[#181](https://github.com/47Felix/RasberryPI-Team-13/issues/181)). Erstellt ohne Zugriff auf echte Hardware (kein Netzwerkzugriff auf den Pi aus dieser Sandbox, keine Arduino-Boards angeschlossen) - siehe "Was noch fehlt" unten, bevor irgendetwas davon als "fertig" gilt.

## Architektur

```
Sensor-Arduino (I2C-Slave 0x08)      Aktor-Arduino (I2C-Slave 0x09)
  KY-028 Analogwert (A0)               KY-028 Analogwert (A0) + LED (D5)
  LED fuer KY-028 (D9)                 Luefter (Software-PWM, D4)
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
| Board 1 | Luefter (DC-Motor/H-Bruecke) | Aktor | Software-PWM → D4 *(war D9, dann D3, siehe Hardware-Update 7+8)* |
| Board 1 | Servo (Ventil) | Aktor | Signal → D6 |

Beide Boards senden jetzt nur noch 2 Bytes (Rohwert) statt der bisherigen 4 (Temp/Feuchte) auf dem Aktor-Board. Die Umrechnung Rohwert → Grad Celsius passiert komplett im Pi-Backend (`pi-backend/calibration.py`, 2-Punkt-lineare Interpolation je Sensor) statt in der Firmware - **inzwischen kalibriert** (17./18.09., Felix, per Referenzthermometer: Sensor-Board 23.0C→raw 212 / 30.0C→raw 160, Aktor-Board 23.0C→raw 174 / 30.5C→raw 126; Details inkl. Drift-Hinweis zum Aktor-Board siehe Docstring in `calibration.py`). Die Kuehlstufen-Entscheidung (`rules.py`) nutzt den Mittelwert der beiden kalibrierten Temperaturen, mit Tischtest-Schwellwerten (noch nicht den echten Betriebswerten aus der Moodle-Aufgabenstellung).

## Hardware-Update 6 (Felix, 18.09.): I2C-Bug bei SMBus-Block-Reads/-Writes gefunden und behoben

Beim Live-Testen ergaben sich falsche Werte auf beiden Seiten des I2C-Verkehrs (Aktor-Sollwerte kamen falsch am Arduino an, Sensor-Rohwerte kamen falsch am Pi an). Ursache in beiden Faellen dieselbe: `smbus2`s `write_i2c_block_data()`/`read_i2c_block_data()` implementieren die SMBus-Block-Konvention (ein Register-Byte wird vorab geschickt, das erste gelesene/geschriebene Byte gilt als Laengenangabe), unsere Arduino-Sketches sprechen dieses Protokoll aber nicht - sie senden/erwarten einfach rohe Bytes ohne Register-Praefix (`Wire.write(...)` ohne vorherige Registeradresse).

- **Schreiben** (`write_actor_setpoints`): `write_i2c_block_data()` schickte zusaetzlich ein fuehrendes `0`-Byte, wodurch der Arduino das Register-Byte als `fanPwm` las (Luefter immer 0) und den echten `fan_pwm`-Wert als `valveAngle`. Fix: `smbus2.i2c_msg.write()` statt `write_i2c_block_data()`.
- **Lesen** (`read_sensor_board`/`read_actor_board`): `read_i2c_block_data()` interpretierte das erste gelesene Byte als Laenge und verwarf es, die beiden zurueckgegebenen Bytes waren dadurch um eins verschoben. Fix: `smbus2.i2c_msg.read()` statt `read_i2c_block_data()` (Retry-Logik `I2C_READ_RETRIES`/`I2C_RETRY_DELAY_SECONDS` unveraendert).

`i2c_msg.read()`/`i2c_msg.write()` (per `bus.i2c_rdwr(msg)`) senden/lesen exakt die angegebene Byte-Anzahl ohne Register-Praefix und ohne Laengen-Interpretation - das passt zum tatsaechlichen Firmware-Verhalten. Details siehe Docstring in `pi-backend/hardware.py`.

## Hardware-Update 7 (18.09.2026): Luefter-PWM lief auf demselben Timer wie der Servo

Auch nach dem I2C-Fix (Hardware-Update 6) drehte der Luefter nicht richtig: `analogWrite()` auf `PIN_FAN_PWM` (D9) blieb wirkungslos bzw. lieferte kein sauberes PWM-Signal. Ursache: Auf dem Arduino Uno belegt die `Servo`-Bibliothek fest **Timer1**, um ihre Pulse per Interrupt zu erzeugen, egal an welchem Pin der Servo haengt - das gilt auch hier, wo `valveServo` an D6 attached ist. Timer1 ist aber gleichzeitig der Hardware-Timer hinter `analogWrite()` auf den Pins **9 und 10**. Sobald `valveServo.attach()` (in `setup()`) laeuft, konfiguriert die Servo-Bibliothek Timer1 fuer ihre eigenen Zwecke um, wodurch `analogWrite(9, ...)` kein normales PWM mehr erzeugt - ein bekanntes Arduino-Uno-Verhalten, keine Verkabelungsfrage.

Fix in `actor_arduino.ino`: `PIN_FAN_PWM` von D9 auf **D3** verschoben (Timer2, unabhaengig vom Servo/Timer1 und von der LED auf D5/Timer0). Das Luefter-PWM funktioniert damit unabhaengig davon, ob der Servo attached ist.

> [!warning] Physische Verkabelung noetig
> Das ist ein Pin-Wechsel auf real schon verkabelter Hardware - das Signalkabel vom Luefter-Transistor/H-Bruecken-Eingang muss am Aktor-Board von **D9 auf D3** umgesteckt werden, bevor der neue Sketch getestet werden kann. Ohne Umstecken bleibt der Luefter aus, weil D9 jetzt nichts mehr ausgibt.

## Hardware-Update 8 (21.09.2026): Timer2 (D3/D11) liefert auf diesem Board generell kein PWM - Umstieg auf Software-PWM

Nach dem Umstecken auf D3 (Hardware-Update 7) drehte der Luefter immer noch nicht. Live getestet mit einem minimalen Sketch, der **nur** `analogWrite()` auf D3 macht - kein Servo, kein I2C, nichts sonst: lief trotzdem nicht. Zur Kontrolle D11 probiert (der zweite Pin an Timer2) - lief ebenfalls nicht, wieder mit einem minimalen Sketch ohne Servo/I2C. Das schliesst den Servo/Timer1-Konflikt aus Hardware-Update 7 als Ursache aus (der betraf nur D9/D10) und zeigt: **Timer2-PWM funktioniert auf diesem konkreten Aktor-Board generell nicht.**

Moeglicher Grund: beim Flashen meldete `avrdude` (`Device signature = 1E 95 0F`) eine Signatur, die neben echtem ATmega328P auch zu einem **LGT8F328P**-Klon passt - einem guenstigen "Arduino Uno"-kompatiblen Chip, der intern teils anders funktioniert als ein echter ATmega328P, gerade bei Timer-Interna. Nicht 100% verifiziert, aber die beobachteten Symptome (Timer1 funktioniert wie erwartet, Timer2 gar nicht) passen dazu.

Fix in `actor_arduino.ino`: kein Hardware-Timer mehr fuer den Luefter. Stattdessen **Software-PWM** - `updateFanSoftwarePwm()` toggelt `PIN_FAN_PWM` per `digitalWrite()` mit einem aus `millis()` berechneten Tastverhaeltnis (Periode 20ms = 50Hz), unabhaengig von jeglicher Timer-Hardware. `PIN_FAN_PWM` auf **D4** verschoben (kein Hardware-PWM-Pin, also auch keine Timer-Ueberraschungen mehr moeglich). `applySetpointsFromPi()` schreibt den empfangenen Sollwert nur noch in `currentFanPwm`, die eigentliche Pin-Ansteuerung passiert in `loop()`.

> [!warning] Physische Verkabelung noetig
> Wieder ein Pin-Wechsel auf real verkabelter Hardware - das Luefter-Signalkabel muss von D3 auf **D4** umgesteckt werden. Verifiziert per Live-Test auf dem Pi (2026-09-21): mit einem minimalen Testsketch liefen weder D3 noch D11 (Timer2), die eigentliche Ursache war also nicht der Servo/Timer1-Konflikt.

## Hardware-Update 9 (21.09.2026): Luefter-PWM invertiert - schneller statt langsamer bei Waerme

Nach Hardware-Update 8 lief die Software-PWM technisch, aber der Luefter reagierte **falsch herum**: er wurde beim Erwaermen langsamer statt schneller (sollte natuerlich umgekehrt sein - mehr Kuehlung bei mehr Waerme). Live per `read_live.py` + SQLite-Log (`challenge_i.db`, Tabelle `readings`) verifiziert waehrend eines Erwaermungstests: `sensor_board_temp_c` stieg korrekt (22,2°C -> 29,6°C), und `fan_pwm` in der DB stieg ebenfalls korrekt mit (0 -> 40) - `rules.py`/`calibration.py` rechneten also die ganze Zeit richtig. Der Fehler lag ausschliesslich in `updateFanSoftwarePwm()` (`actor_arduino.ino`, siehe Hardware-Update 8): das Board schaltet offenbar **active-low** (HIGH am Transistor-/H-Bruecken-Eingang = Luefter AUS statt AN), die Software ging aber von active-high aus.

Fix: `digitalWrite(PIN_FAN_PWM, ...)` in `updateFanSoftwarePwm()` invertiert (`LOW` waehrend der "Ein"-Zeit, `HIGH` sonst). Kein Pin-Wechsel noetig, reine Software-Aenderung.

> [!warning] Noch nicht auf echter Hardware bestaetigt
> Fix beruht auf der DB-Auswertung (korrekter `fan_pwm`-Sollwert, falsches physisches Verhalten) und ist logisch die einzige verbleibende Erklaerung, aber noch nicht durch einen erneuten Live-Test nach dem Flashen verifiziert. Naechster Schritt: neu flashen, wieder erwaermen, pruefen ob der Luefter jetzt bei steigender Temperatur schneller wird.

## Hardware-Update 10 (22.09.2026): Aktor-Board-LED (D5) konnte nie leuchten - falsche Kalibrierungskonstanten

`actor_arduino.ino` hatte `RAW_AT_LED_FULL = 13` / `RAW_AT_LED_OFF = 35` - Werte aus einer frueheren Hardware-Iteration, die nie an die aktuelle Kalibrierung (`pi-backend/calibration.py::ACTOR_BOARD_CALIBRATION`, 23.0C -> Rohwert 174, 30.5C -> Rohwert 126) angepasst wurden. Der reale Rohwert liegt immer bei ~120-220, weit ausserhalb von `[13, 35]` - `map()` extrapolierte damit staendig unter 0, `constrain()` klemmte die Helligkeit dauerhaft auf 0. Die Aktor-LED konnte also mit den alten Konstanten **nie** leuchten, unabhaengig von der echten Temperatur.

Fix: `RAW_AT_LED_FULL`/`RAW_AT_LED_OFF` aus der echten Kalibriergeraden neu hochgerechnet (gleiche Methode wie in `sensor_arduino.ino`, LED voll hell ab 30C, aus ab -10C, linear dazwischen): `129`/`385`.

Zusaetzlich beobachtet, aber noch offen: der Aktor-Board-Rohwert selbst schwankt live sichtbar mit dem Luefterzustand (z.B. ~208 bei `fan_pwm=0`, ~166 bei `fan_pwm>0`, Sprung innerhalb einer einzelnen Messung) - das ist zu schnell fuer echte Thermik und deutet auf eine elektrische Stoerung (Spannungseinbruch durch den Luefterstrom auf derselben Platine wie der KY-028-Analogausgang) hin, nicht auf eine falsche Kalibrierung. Braucht vermutlich einen Entkopplungskondensator nah am KY-028 auf dem Aktor-Board - noch nicht behoben, physischer Hardware-Zugriff noetig.

## Hardware-Update 3 (15.09.2026, Issue #191): Sensor ist ein DHT22, nicht DHT11

Der Temp/Feuchte-Sensor hat ein weisses Gehaeuse (DHT22), nicht das blaue DHT11-Gehaeuse, das urspruenglich angenommen wurde. Der Sketch hatte `DHTTYPE` faelschlich auf `DHT11` stehen - DHT11 und DHT22 kodieren ihre Rohbytes unterschiedlich, DHT11-Parsing auf einem DHT22-Bytestream ergab die konstant ~20-22 Grad zu niedrigen Werte aus Issue #191, kein Verkabelungs-/Pull-up-Problem. Fix: `DHTTYPE` auf `DHT22` umgestellt (`ice_truck_single_board.ino`), der bisherige `+20°C`-Kalibrierungs-Offset ist damit hinfaellig und entfernt. **Noch nicht an echter Hardware verifiziert** - naechster Schritt bei Hardware-Zugriff: neu flashen, echte Werte gegen ein zweites Thermometer pruefen, Issue #191 danach schliessen.

## Was noch fehlt (braucht physischen Hardware-Zugriff)

- [x] **Beide Arduino-Sketches (jetzt beide KY-028) kompilieren + flashen** und auf den echten Boards testen
- [x] **I2C-Verkabelung** wie oben herstellen und mit `i2cdetect -y 1` auf `0x08` und `0x09` verifizieren
- [x] **`RealI2CBus` gegen echten Bus testen** (`smbus2`, `/dev/i2c-1` auf dem Pi)
- [x] **Beide KY-028 kalibrieren** (`pi-backend/calibration.py`, `SENSOR_BOARD_CALIBRATION`/`ACTOR_BOARD_CALIBRATION`) - je Sensor zwei Referenzpunkte per Referenzthermometer gemessen (17./18.09., Felix); Aktor-Board-Ruhewert driftet spuerbar (Eigenerwaermung), ggf. per Sensor-Board-Proxy neu abgleichen (siehe Docstring)
- [ ] **Schwellwerte in `rules.py` kalibrieren** (`FAN_ON_TEMP_C`, `VALVE_ON_TEMP_C` sind Platzhalter) - haengt an der eigentlichen Aufgabenstellung aus dem Moodle-Kurs (Issue [#167](https://github.com/47Felix/RasberryPI-Team-13/issues/167)) und an der realen Sensor-Kalibrierung
- [x] **`app.py` als systemd-Service** auf dem Pi eingerichtet (18.09., `pi-backend/challenge-i-backend.service`, `enable --now` ausgefuehrt) - laeuft, loggt live in `challenge_i.db`, fan/valve bei 0 solange unter `FAN_ON_TEMP_C` (aktuell Tischtest-Platzhalter, siehe naechster Punkt)

## Wo was liegt

- `sensor_arduino/sensor_arduino.ino` - **aktuell verkabelt** (Board 2, I2C 0x08): KY-028, Tracks A/B/C
- `actor_arduino/actor_arduino.ino` - **aktuell verkabelt** (Board 1, I2C 0x09): KY-028 + Luefter/Servo, Tracks D/E (kein DHT22 mehr, siehe Hardware-Update 5)
- `ice_truck_single_board/ice_truck_single_board.ino` - fruehere Ein-Board-Verkabelung (14.-17.09., siehe Hardware-Update 2), aktuell **nicht** verkabelt, bleibt als Referenz
- `pi-backend/` - Track C, E, F (Pi-Seite): `hardware.py` (I2C real+mock, zwei Adressen), `calibration.py` (Rohwert → Grad Celsius, kalibriert), `rules.py` (Regellogik), `db.py` (SQLite), `app.py` (Hauptschleife), `read_live.py` (manuelles Live-Auslesen beider Boards, nuetzlich zum Kalibrieren), `tests/`
