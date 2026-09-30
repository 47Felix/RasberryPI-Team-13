# Redemanuskript – Fachgespräch Challenge I + II

Zum Vorlesen/Üben, kein Folien-Teil. Richtwert Gesamtzeit: **~15 Minuten** Vortrag, Rest der Zeit für Rückfragen (dafür gibt's `fragen-antworten.md`). Zeiten sind Richtwerte, nicht auswendig lernen – lieber in eigenen Worten sagen.

Auf den Folien steht oben rechts/links jeweils klein, welcher Bewertungspunkt gerade dran ist (z.B. "Bewertung: Lüfter über Transistor vom Pi gesteuert (8 Pkt)") – das ist nur Orientierung für euch, **nicht vorlesen**. Drei Folien haben zusätzlich ein "Live-Demo"-Badge – an der Stelle wirklich kurz die Hardware anfassen statt nur zu erzählen, das ist explizit im Bewertungsbogen gefordert ("es wird gezeigt").

Sprecherwechsel sind im Text markiert. Wer gerade nicht dran ist, steht einfach ruhig daneben – keiner muss die Bühne verlassen.

---

## Intro (Erik) – ca. 1,5 Min

**[Folie: Titel]**

"Hallo zusammen. Wir sind Team 13, und wir zeigen euch heute, was aus unserem Ice-Truck-Kühlketten-Szenario geworden ist – einmal Challenge I, Signale und Bus-Systeme, und Challenge II, Kommunikation und Entwicklungswerkzeuge."

**[Folie: Worum geht's heute]**

"Beide Challenges hängen an derselben Hardware, deshalb zeigen wir sie zusammen statt getrennt. Der rote Faden ist der Datenfluss: Sensor misst, Arduino gibt weiter, der Pi liest per I2C aus, rechnet und regelt, loggt in eine Datenbank – und in Challenge II kommt zusätzlich noch MQTT, Node-RED und ein Handy dazu, damit man das Ganze auch von unterwegs sieht und steuern kann."

**[Folie: Team & Aufteilung]**

"Wir gehen einfach diesen Datenfluss entlang. Anton fängt bei der Hardware an, dann übernimmt Felix die Datenübertragung, Dogan macht Regellogik und Aktorik, und danach steige ich bei Challenge II ein – bevor Anton und Felix uns nochmal zu Node-RED, Handy und dem aktuellen Stand mitnehmen. Dogan macht am Ende das Fazit. Anton, du bist dran."

---

## Block 1 – Hardware & Sensorik (Anton) – ca. 3 Min

**[Folie: Systemarchitektur Challenge I]**

"Danke Erik. Wir haben zwei Arduino Unos im Einsatz, jeder hängt als eigener I2C-Slave am Bus – einer auf Adresse 0x08, das ist unser 'Sensor-Board', der andere auf 0x09, unser 'Aktor-Board', weil da zusätzlich Lüfter und Servo dranhängen. Beide reden über denselben I2C-Bus mit dem Pi, und der Pi ist quasi das Gehirn: liest beide aus, rechnet, regelt, loggt."

**[Folie: Sensorik: von DHT22 zu 2× KY-028]**

"Ursprünglich wollten wir auf dem Aktor-Board einen DHT22 für Temperatur und Feuchte. Der hat aber ab dem ersten Aufruf nach jedem Reset konsequent nur NaN geliefert – wir haben das direkt per Serial geprüft, Verkabelung mehrfach kontrolliert, es lag nicht an uns, der Sensor war schlicht defekt oder inkompatibel. Statt weiter zu raten, haben wir ihn durch ein zweites KY-028 ersetzt – jetzt messen beide Boards nach demselben Prinzip, und wir haben beide einzeln mit einem echten Referenzthermometer kalibriert."

**[Folie: LED zeigt den Messwert]**

"Jedes Board hat außerdem eine eigene LED, die per PWM die Helligkeit passend zur gemessenen Temperatur anzeigt – und das rechnet der Arduino komplett selbst, ohne dass er dafür erst beim Pi nachfragen muss. Voll hell ab etwa 30 Grad, aus ab etwa minus 10 Grad, dazwischen linear."

**[Live-Demo jetzt: Finger auf den KY-028 legen oder ihn kurz anpusten/anhauchen – Helligkeit ändert sich sichtbar in Echtzeit. Kurz warten, bis alle es gesehen haben, dann weiter.]**

"Damit übergebe ich an Felix, der erklärt, wie die Daten vom Arduino zum Pi kommen und was wir da für einen Bug gefunden haben."

---

## Block 2 – Datenübertragung & Speicherung (Felix) – ca. 3 Min

**[Folie: I2C-Kommunikation Pi ↔ beide Arduinos]**

"Danke Anton. Der Pi liest beide Boards per I2C aus, über die Python-Bibliothek smbus2. Und dabei sind wir auf einen ziemlich hartnäckigen Bug gestoßen: Die Standard-Funktionen von smbus2 für Block-Reads und -Writes sprechen die sogenannte SMBus-Block-Konvention – die schicken vorab ein Register-Byte und interpretieren das erste übertragene Byte als Längenangabe. Unsere Arduino-Sketches kennen dieses Protokoll aber gar nicht, die schicken einfach rohe Bytes. Ergebnis: Lüfter- und Ventil-Sollwerte kamen vertauscht an, und die Sensorwerte waren um ein Byte verschoben."

"Der Fix war, stattdessen die raw i2c_msg-Funktionen von smbus2 zu nutzen, die schicken und lesen exakt die angegebene Byte-Anzahl, ohne Präfix und ohne Interpretation."

**[Folie: Datenformate der Sensoren]**

"Was tatsächlich über den Bus geht, sind pro Board zwei rohe Bytes – der unkalibrierte KY-028-Analogwert. Die Umrechnung in Grad Celsius passiert komplett im Pi-Backend, mit einer Zwei-Punkt-linearen Interpolation, und zwar für jedes Board mit seiner eigenen Kalibrierkurve, weil die beiden Sensoren sich unterschiedlich verhalten."

**[Folie: Messdaten in SQLite protokolliert]**

"Jede Messung landet in einer SQLite-Tabelle – Zeitstempel, beide Rohwerte, beide kalibrierten Temperaturen, und die daraus berechneten Lüfter- und Ventil-Sollwerte. Das läuft als systemd-Service, startet also automatisch bei jedem Neustart des Pi, ohne dass wir manuell irgendwas anstoßen müssen. Und wir loggen bewusst Rohwert und kalibrierten Wert – falls wir die Kalibrierung später nachjustieren, bleiben die alten Rohdaten trotzdem auswertbar."

"Dogan macht jetzt weiter mit der Regellogik und der Aktorik."

---

## Block 3 – Regellogik & Aktorik (Dogan) – ca. 3,5 Min

**[Folie: Regellogik: zwei Kühlstufen]**

"Danke Felix. Aus dem Mittelwert beider kalibrierter Temperaturen berechnen wir zwei Kühlstufen: Unter 25 Grad passiert nichts. Zwischen 25 und 28 Grad fährt der Lüfter proportional hoch. Ab 28 Grad bleibt der Lüfter voll an, und zusätzlich öffnet das Ventil proportional. Die genauen Schwellwerte sind aktuell noch Tischtest-Werte, nicht die realen Betriebswerte aus der Aufgabenstellung – das ist ein offener Punkt, den wir noch kalibrieren müssen."

**[Folie: Lüfter: Ansteuerung über Transistor]**

"Der Lüfter hängt über einen Transistor am Arduino, und der Pi gibt den PWM-Sollwert per I2C vor. Bis der lief, war es ehrlich gesagt eine Odyssee: Erst kollidierte unser PWM-Pin mit der Servo-Bibliothek, die intern denselben Timer belegt. Dann haben wir auf einen anderen Timer-Pin umgesteckt – der hat auf unserem konkreten Board aber gar kein PWM ausgegeben, vermutlich weil es kein echter Original-Chip ist, sondern ein günstiger Klon mit anderem Timer-Verhalten. Also sind wir auf Software-PWM umgestiegen, komplett ohne Hardware-Timer. Und dann drehte der Lüfter erstmal rückwärts – schneller bei Kälte statt bei Wärme, weil das Board active-low schaltet. Auch das ist jetzt invertiert und korrekt."

**[Live-Demo jetzt: Sensor erwärmen (Finger/Handwärme reicht meist, notfalls kurz mit den Händen reiben) und zeigen, wie der Lüfter hörbar hochdreht, sobald die Schwelle überschritten wird.]**

**[Folie: Ventil: Servo-Ansteuerung]**

"Das Ventil steuern wir über einen Servo an, Winkel null bis 180 Grad, direkt aus der Regellogik berechnet und vom Pi per I2C geschrieben. Und genau diese Servo-Bibliothek war übrigens die Ursache für den Lüfter-Timer-Konflikt von eben – sie belegt beim Anschließen automatisch den Timer, egal an welchem Pin sie hängt."

**[Live-Demo jetzt, falls Zeit reicht: Sensor weiter erwärmen bis zur zweiten Schwelle, Servo-Ausschlag am Ventil zeigen. Sonst kurz beschreiben statt vorführen, um die Zeit zu halten.]**

**[Folie: Szenario sinnvoll erweitert]**

"Über das geforderte Minimum sind wir an ein paar Stellen hinausgegangen: zwei echte Sensor-Boards statt nur einem, echte Kalibrierung mit Referenzthermometer statt geschätzten Werten, automatischer Systemstart, und ein manueller Override-Kanal, den wir für Challenge II gebaut haben – dazu übergebe ich jetzt an Erik."

---

## Block 4 – MQTT & Topics (Erik) – ca. 3 Min

**[Folie: Von Challenge I zu Challenge II]**

"Danke Dogan. Challenge I regelt lokal und automatisch – aber niemand steht dauerhaft neben dem Pi, um den Status zu sehen. Deshalb haben wir in Challenge II eine Schicht draufgesetzt: Ein Node-RED-Flow liest regelmäßig die Datenbank, veröffentlicht die Werte per MQTT, und ein Handy kann sich das anschauen – und sogar zurücksteuern. Wichtig: Das ersetzt die Regellogik aus Challenge I nicht, es kommt nur obendrauf."

**[Folie: MQTT-Broker: lokaler Mosquitto]**

"Wir nutzen einen lokalen Mosquitto-Broker direkt auf dem Pi statt des ITECH-Broker. Der war zwar schon installiert, aber nur auf localhost erreichbar. Wir haben ihn so konfiguriert, dass er auf allen Netzwerkschnittstellen lauscht, Passwort-Pflicht hat, und eine Zugriffsliste, die unseren Nutzer strikt auf unser eigenes Topic-Präfix beschränkt. Getestet haben wir: authentifizierter Roundtrip funktioniert, anonyme Verbindungen werden abgelehnt, und Zugriffe außerhalb unseres Präfixes werden verworfen."

**[Folie: Topic-Schema & Hierarchie]**

"Alle unsere Topics liegen unter einem gemeinsamen Präfix, darunter sauber getrennt in Sensoren, Aktoren und einen Sammel-Status, den der Pi veröffentlicht, und Control-Topics, über die das Handy zurückschreiben kann. Die Veröffentlichungen sind retained – das heißt, ein Handy, das sich neu verbindet, sieht sofort den letzten Stand, statt erst auf den nächsten Messzyklus warten zu müssen."

"Anton, magst du weitermachen mit Node-RED und der Fernsteuerung?"

---

## Block 5 – Node-RED & Fernsteuerung (Anton) – ca. 2 Min

**[Folie: Node-RED als Integrationsschicht]**

"Klar, danke Erik. Node-RED ist bei uns die Brücke in beide Richtungen: Ein Flow liest regelmäßig die letzte Zeile aus der Datenbank und veröffentlicht sie auf die passenden MQTT-Topics. Derselbe Flow abonniert außerdem die Control-Topics, validiert eingehende Befehle vom Handy, protokolliert sie, und reicht sie über einen Exec-Knoten an ein Python-Skript weiter."

**[Folie: Fernsteuerung: auto/manual als Extra-Feature]**

"Damit haben wir einen Modus-Umschalter gebaut: automatisch, wie in Challenge I, oder manuell vom Handy aus. Im manuellen Modus liest unser Backend bei jedem Messzyklus, ob ein manueller Sollwert vorliegt, und schreibt den dann direkt per I2C an den Aktor – statt den berechneten Wert zu nehmen. Auf Modul-Ebene ist das komplett getestet, auf der echten Hardware Ende-zu-Ende steht der letzte Test noch aus, dazu gleich mehr von Felix."

---

## Block 6 – Mobiles Endgerät & Status (Felix) – ca. 2,5 Min

**[Folie: Mobiles Endgerät statt Eigenbau-App]**

"Danke Anton. Die Aufgabenstellung erlaubt ausdrücklich, statt einer selbstgebauten App eine fertige MQTT-App zu nutzen – MQTT Dash oder MQTT Explorer. Genau das machen wir: Einzelwerte kommen als reine Zahl, die passen direkt in numerische Widgets, und zusätzlich gibt's einen Status als JSON für alle, die lieber Rohdaten sehen wollen."

**[Folie: Stand heute & offene Punkte]**

"Ganz ehrlich zum aktuellen Stand: Was läuft, läuft stabil – der I2C-Bug ist behoben, die Regellogik ist getestet, das Logging läuft als Dienst, und der Node-RED-Flow ist importiert und mit echten Live-Daten verifiziert, zumindest in Leserichtung. Offen sind noch zwei Dinge, die beide kurzen Root-Zugriff auf dem Pi brauchen: Die Broker-Authentifizierung hängt seit Kurzem in einer Reconnect-Schleife und muss neu gesetzt werden, und unser Backend-Dienst muss einmal neu gestartet werden, damit er den neuesten Code mit der Fernsteuerung überhaupt kennt. Und ein echtes Handy mit MQTT Dash haben wir noch nicht final konfiguriert. Als Ausblick steht Challenge III noch komplett offen – Speicherung und Auswertung in der Cloud."

"Dogan macht den Abschluss."

---

## Fazit (Dogan) – ca. 1 Min

**[Folie: Lessons Learned]**

"Danke Felix. Was wir mitnehmen: Erst auf der echten Hardware messen, nicht raten – unser kaputter Sensor und der Timer-Konflikt waren beides Dinge, die man am Schreibtisch nie gefunden hätte. Modul-Tests geben uns Sicherheit, bevor wir überhaupt Hardware anfassen, ersetzen den echten Hardware-Test aber nicht – der hat nochmal eigene Bugs zutage gebracht. Und ehrliches Logging, also Rohwert und kalibrierter Wert gleichzeitig, macht die Fehlersuche später erst möglich."

**[Folie: Danke]**

"Damit sind wir durch. Danke fürs Zuhören – wir beantworten gerne eure Fragen."
