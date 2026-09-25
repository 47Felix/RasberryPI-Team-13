# Fragen & Antworten – Vorbereitung für das Fachgespräch

Nur für euch zur Vorbereitung, kein Teil der eigentlichen Folien. Sortiert nach Themenblock, deckt Challenge I und II ab. Direkt relevant für den Bewertungspunkt "Rückfragen zu technischen Entscheidungen fachlich fundiert erläutert" (7 Punkte).

---

## Zur Architektur allgemein

**Warum zwei Arduinos statt einem?**
Weil real zwei Boards zur Verfügung standen und sich damit Sensorik (Board 2) und Aktorik (Board 1) sauber trennen lassen. Es gab zwischenzeitlich auch eine Ein-Board-Version (`ice_truck_single_board.ino`), die bleibt als Referenz im Repo, ist aber nicht die aktuell verkabelte Hardware.

**Warum I2C und nicht z.B. Serial/UART?**
I2C erlaubt mehrere Teilnehmer (hier: zwei Arduinos) an einem gemeinsamen Bus mit dem Pi als Master, ohne für jedes Board einen eigenen UART-Port zu brauchen. Passt außerdem zur Aufgabenstellung ("Bus-Protokoll").

**Warum 3,3V-Pull-ups und nicht die Standard-5V-Pull-ups der Arduinos?**
Der Pi hat 3,3V-GPIOs, die nicht 5V-tolerant sind. Externe Pull-ups auf 3,3V plus Abschalten der internen 5V-Pull-ups auf beiden Arduinos verhindert, dass der Bus Richtung 5V gezogen wird und die Pi-GPIOs beschädigt.

---

## Zur Sensorik (Challenge I)

**Warum KY-028 und nicht ein "richtiger" digitaler Temperatursensor?**
War im Kit vorhanden und funktioniert zuverlässig als Analogsensor. Der ursprünglich geplante DHT22 lieferte durchgehend NaN – nicht an der Software gelegen, per Serial direkt gegengeprüft.

**Wie kalibriert ihr einen Analogsensor ohne bekannte Sensorkennlinie?**
Zwei-Punkt-Messung gegen ein Referenzthermometer (z.B. 23°C und 30°C), dazwischen lineare Interpolation. Kein Datenblatt-Kennwert nötig, dafür nur im kalibrierten Bereich genau.

**Warum hat jedes Board eine eigene Kalibrierkurve statt einer gemeinsamen?**
Bauteilstreuung – die beiden KY-028-Module verhalten sich nicht identisch. Zusätzlich beobachtet: Der Rohwert des Aktor-Boards schwankt sichtbar mit dem Lüfterzustand (vermutlich elektrische Störung durch den Motorstrom auf derselben Platine) – noch offen, braucht vermutlich einen Entkopplungskondensator.

---

## Zu I2C / Datenübertragung

**Was genau war der SMBus-Bug, könnt ihr das nochmal technisch erklären?**
`smbus2`s `write_i2c_block_data()`/`read_i2c_block_data()` implementieren die SMBus-Block-Konvention: ein Register-Byte wird vorab gesendet, das erste übertragene Nutzdaten-Byte gilt als Längenangabe. Unsere Arduino-Sketches sprechen dieses Protokoll nicht – sie senden/erwarten rohe Bytes ohne Register-Präfix. Fix: `smbus2.i2c_msg.read()`/`.write()`, die exakt die angegebene Byte-Anzahl ohne Präfix/Längen-Interpretation übertragen.

**Wie würde man diesen Bug ohne Oszilloskop/Logic-Analyzer finden?**
Über die Symptome von beiden Seiten: Am Arduino kamen vertauschte Sollwerte an (Lüfter immer 0, Ventil bekam den Lüfterwert), am Pi waren die gelesenen Sensorwerte um ein Byte verschoben. Beides zusammen zeigt ein systematisches Byte-Offset-Problem, kein Zufallsfehler – das deutet auf ein Protokoll-Missverständnis statt auf ein Verkabelungsproblem hin.

---

## Zur Regellogik & Aktorik

**Im Bewertungsbogen steht "Luftsensor" bei der Transistor-Steuerung – habt ihr da auch einen?**
Nein, das ist im Bogen erkennbar mit "Lüfter" gemeint (Transistor-Ansteuerung passt zum DC-Lüfter aus dem Elegoo-Kit, ein separater Luftsensor kommt in der Aufgabenstellung und in unserem Aufbau nicht vor). Falls das angesprochen wird: kurz richtigstellen und den Lüfter zeigen.

**Warum zwei Kühlstufen und nicht stufenlos oder nur ein/aus?**
Kompromiss zwischen einfacher, nachvollziehbarer Logik und realistischem Verhalten: leichte Kühlung reicht oft schon (nur Lüfter), erst bei stärkerer Abweichung öffnet zusätzlich das Ventil.

**Woher kommen die Schwellwerte 25°C/28°C – sind das die realen Betriebswerte?**
Nein, aktuell Tischtest-Platzhalter (per Umgebungsvariable überschreibbar, `FAN_ON_TEMP_C`/`VALVE_ON_TEMP_C`). Die echten Werte aus der Moodle-Aufgabenstellung sind noch nicht eingetragen – offener Punkt.

**Warum Software-PWM für den Lüfter statt Hardware-PWM?**
Weil auf unserem konkreten Board keiner der beiden Timer2-Pins (D3/D11) ein PWM-Signal ausgab, live mit einem minimalen Test-Sketch ohne Servo/I2C verifiziert. Der wahrscheinliche Grund: `avrdude` meldete eine Chip-Signatur, die zu einem LGT8F328P-Klon statt einem echten ATmega328P passt – dessen Timer-Interna funktionieren teils anders. Software-PWM (per `millis()`/`digitalWrite()`) umgeht das Problem komplett, unabhängig von der Timer-Hardware.

**Was heißt "active-low" beim Lüfter genau?**
Der Transistor/die H-Brücke auf diesem Board schaltet den Lüfter ein, wenn der Steuerpin LOW ist, nicht HIGH wie ursprünglich angenommen. Ohne Invertierung lief der Lüfter bei Wärme langsamer statt schneller – am Verlauf von `fan_pwm` in der DB (stieg korrekt) gegen das reale Verhalten (falsch) erkannt.

---

## Zu MQTT / Node-RED (Challenge II)

**Warum ein eigener lokaler Broker statt des ITECH-Brokers?**
Volle Kontrolle über Auth/ACL und keine Abhängigkeit von Schul-Infrastruktur/Internetzugang – der Broker lief schon lokal auf dem Pi, wir mussten ihn nur extern erreichbar und authentifiziert machen.

**Ist das sicher, wenn der Broker jetzt von außen erreichbar ist?**
Passwort-Pflicht (`allow_anonymous false`) plus ACL, die den einzigen Nutzer strikt auf unser Topic-Präfix beschränkt. Zugangsdaten liegen nicht im Repo. Erreichbar nur im Schul-WLAN bzw. per Tailscale-VPN für Fernwartung, nicht offen im Internet.

**Warum retained Topics – was wäre ohne?**
Ohne retained müsste ein neu verbundenes Handy bis zum nächsten Messzyklus (5s) warten, bevor es überhaupt einen Wert sieht. Retained liefert sofort den letzten bekannten Stand.

**Was passiert, wenn zwei Handys gleichzeitig fernsteuern?**
Aktuell keine Konfliktbehandlung – wer zuletzt schreibt, gewinnt (letzter `control/*`-Befehl gilt). Für den Schulkontext akzeptabel, wäre bei echtem Mehrbenutzerbetrieb ein offener Punkt.

**Warum Node-RED und nicht z.B. ein eigenes Python-Skript als Brücke?**
Node-RED ist die in der Aufgabenstellung vorgesehene Integrationsschicht, bringt fertige Knoten für SQLite und MQTT mit, und der Flow lässt sich visuell nachvollziehen statt in Code versteckt zu sein – passt zum Kursziel "Entwicklungswerkzeuge".

---

## Zum Vorgehen / Stand / Team

**Was ist aktuell tatsächlich noch kaputt, ganz ehrlich?**
Zwei Dinge, beide brauchen kurz interaktiven Root-Zugriff auf dem Pi: Die Broker-Authentifizierung hängt in einer Reconnect-Schleife (Passwort/Credentials driften auseinander), und der Backend-Dienst läuft noch mit älterem Code ohne Fernsteuerungs-Unterstützung, weil er seit dem letzten Reboot nicht neu gestartet wurde. Beides ist verstanden und lösbar, nur (noch) nicht ausgeführt.

**Wie habt ihr getestet, ohne ständig an der echten Hardware zu sein?**
Mit einem Mock-I2C-Bus (`MockI2CBus` in `hardware.py`) für die komplette Pi-Software – Regellogik, Kalibrierung, Logging, Fernsteuerungs-Zustand –, alles per `pytest` automatisiert getestet, bevor überhaupt wieder echte Hardware verfügbar war. Gleiches Prinzip wie beim `socat`-Mock für unser Tresor-Kurzprojekt.

**Wie habt ihr euch die Arbeit aufgeteilt?**
Entlang der Pipeline: Hardware/Sensorik, Datenübertragung/Speicherung, Regellogik/Aktorik, und bei Challenge II zusätzlich MQTT/Topics sowie Node-RED/mobile Anbindung – jede:r hat mindestens einen Abschnitt durchgängig verantwortet und kann ihn im Detail erklären.

**Was würdet ihr mit mehr Zeit noch machen?**
Die beiden offenen Pi-Zugriffs-Punkte fixen und den kompletten Pfad Handy → MQTT → Node-RED → I2C → Aktor einmal live durchtesten, die realen Schwellwerte aus der Aufgabenstellung statt der Tischtest-Werte eintragen, und den Entkopplungskondensator für das rauschende Aktor-Board ergänzen.
