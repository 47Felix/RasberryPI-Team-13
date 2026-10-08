# Challenge III – Folien und Sprechtext

Automatisch aus den Folien-Quellen (`deck-source/`) erzeugt: Titel jeder Folie, Sprecher und Sprechtext aus den Notizen. Die Aufteilung mit Richtzeiten steht im [Redemanuskript](redemanuskript.md).

## Folie 1: Ice Truck in der Cloud

*CHALLENGE III · IOT IN DER CLOUD*

SPRECHER: Anton · RICHTZEIT: 0:30 min — Guten Tag zusammen, wir sind Team 13-1. In Challenge III ging es darum, die Temperaturdaten vom Ice Truck automatisch in eine Cloud zu bringen. Ich beginne mit Problem und Lösung. Danach stellt Dogan die Cloud-Auswahl vor, Erik erklärt Datenschutz und Sicherheit, und Felix zeigt das Ergebnis, die Zusatzfunktionen und das Fazit. ÜBERGABE: Weiter mit Problem und Lösung (Anton bleibt).

## Folie 2: Heute liegen die Daten nur im Truck

*01 · PROBLEM*

SPRECHER: Anton · RICHTZEIT: 1:00 min — Die Ausgangslage: Die Messwerte liegen bisher nur auf dem Raspberry Pi im Truck und werden erst in der Zentrale von Hand gesichert. Gleichzeitig verlangen die EU-Verordnungen 178/2002 und 37/2005 einen Nachweis der Temperaturen. Kontrolliert wird bisher nur stichprobenartig, und Sensoren oder Kühlaggregate fallen trotz Wartung immer wieder aus. Unser Ziel: Die Daten sollen automatisch in die Cloud, damit sie jederzeit und überall abrufbar sind und auch bei einem Ausfall des Pi erhalten bleiben. ÜBERGABE: Weiter mit unserer Lösung (Anton bleibt).

## Folie 3: Vom Truck in die Cloud

*02 · LÖSUNG*

SPRECHER: Anton · RICHTZEIT: 1:00 min — So läuft es: Die Arduinos messen, der Raspberry Pi regelt und speichert jede Messung in einer SQLite-Datenbank. Unsere Cloud-Bridge, ein kleines Python-Programm, liest nur neue Messungen und schickt sie per HTTPS an ThingSpeak. Die Datenbank ist zugleich der Puffer: Fällt das Netz aus, wird später nachgeholt. In der Cloud gibt es Diagramme, Alarme und einen CSV-Export. Wir messen alle 5 Sekunden, jede Messung hat 8 Datenfelder, und der Free-Tarif kostet nichts. ÜBERGABE: Weiter mit dem Überblick zum Bewertungsbogen (Anton bleibt).

## Folie 4: Wir folgen dem Bewertungsbogen

*ÜBERBLICK*

SPRECHER: Anton · RICHTZEIT: 0:30 min — Wir haben die Präsentation entlang des Bewertungsbogens aufgebaut. Jede Folie von 5 bis 12 beantwortet genau ein Kriterium, oben rechts steht die Punktzahl. So könnt ihr direkt mitbewerten. Die größten Blöcke sind die sichere Datenübertragung und die Messdaten mit je 10 Punkten. ÜBERGABE: Ich übergebe an Dogan, er stellt die Clouddienste vor.

## Folie 5: Zwei Dienste im Vergleich

*KRITERIUM 1 · MINDESTENS ZWEI CLOUDDIENSTE*

SPRECHER: Dogan · RICHTZEIT: 1:00 min — Wir haben mehrere Dienste angeschaut und stellen zwei im Detail vor: Azure IoT Hub von Microsoft und ThingSpeak von MathWorks. Verglichen haben wir nach den Kriterien aus der Aufgabe: Protokolle, Speicherung, Visualisierung, Kosten und Datenschutz. Azure ist eine Plattform mit MQTT, Archiv im Blob Storage und EU-Regionen. ThingSpeak ist eine fertige Anwendung mit HTTP und MQTT, eingebauten Diagrammen und Servern in den USA. Zusätzlich geprüft: AWS IoT Core braucht eine Kreditkarte, die Arduino Cloud speichert im Free-Tarif nur einen Tag, und eine eigene VM wäre IaaS mit viel Betriebsaufwand. ÜBERGABE: Weiter mit unserer Entscheidung (Dogan bleibt).

## Folie 6: Entscheidung: ThingSpeak

*KRITERIUM 2 · TECHNISCH BEGRÜNDETE ENTSCHEIDUNG*

SPRECHER: Dogan · RICHTZEIT: 1:30 min — Wir haben uns für ThingSpeak entschieden. Azure IoT Hub hatten wir ebenfalls vorbereitet, mit Einrichtungsskript und Auswertung. Am Ende hat uns ThingSpeak für unseren Prototyp aber besser gefallen, aus vier Gründen. Kosten: Es ist kostenlos und braucht keine Kreditkarte. Protokolle: Die HTTPS-Schnittstelle passt zu unserer Bridge und nimmt viele Messungen mit eigenem Zeitstempel an, MQTT wäre auch möglich. Speicherung und Visualisierung: Kanal, Diagramme und MATLAB sind eingebaut, wir brauchen keinen eigenen Server und waren in Minuten startklar. Datenschutz: Wir übertragen keine Personendaten, deshalb ist ein US-Anbieter vertretbar. Für eine ganze Flotte würden wir Azure empfehlen. FALLS GEFRAGT, warum nicht Azure: ehrlich antworten, dass der Zugang zu unserem Azure-Schülerkonto zum Start nicht verfügbar war und ThingSpeak dann alle Anforderungen erfüllt hat und uns besser gefallen hat. ÜBERGABE: Weiter mit den NIST-Merkmalen (Dogan bleibt).

## Folie 7: Die fünf Cloud-Merkmale

*KRITERIUM 3 · NIST-KRITERIEN (SP 800-145)*

SPRECHER: Dogan · RICHTZEIT: 1:00 min — Die fünf NIST-Merkmale. Self-Service: Wir haben Konto und Kanal in Minuten selbst angelegt. Broad Network Access: HTTPS aus jedem Netz, Diagramme im Browser. Resource Pooling: Die Plattform bedient viele Kunden gemeinsam, das können wir aber nicht selbst überprüfen. Rapid Elasticity: Weitere Einheiten lassen sich jederzeit zukaufen, eine Einheit sind 33 Millionen Nachrichten im Jahr, im Free-Tarif gelten aber feste Limits und es gibt kein automatisches Skalieren. Measured Service: Auf der Seite My Account sehen wir Verbrauch und Restkontingent, dazu den Screenshot zeigen. Ein privater Server zu Hause wäre keine Cloud, weil Pooling, Elastizität und Abrechnung fehlen. ÜBERGABE: Ich übergebe an Erik: Einordnung, Datenschutz und Sicherheit.

## Folie 8: IaaS, PaaS oder SaaS?

*KRITERIUM 4 · EINORDNUNG IAAS, PAAS ODER SAAS*

SPRECHER: Erik · RICHTZEIT: 1:00 min — Die Einordnung hängt davon ab, wer was verwaltet. Bei einer eigenen VM wäre es IaaS: Wir müssten Betriebssystem, Broker und Datenbank selbst betreiben. Azure IoT Hub ist PaaS: Die Plattform gehört dem Anbieter, wir betreiben nur Geräte, Routing und Auswertung. ThingSpeak ist SaaS: Wir konfigurieren nur einen Kanal in einer fertigen Anwendung und liefern Daten. Die MATLAB-Skripte sind ein Zusatz innerhalb dieser Anwendung, kein eigener Plattformbetrieb. ÜBERGABE: Weiter mit Datensicherheit und DSGVO (Erik bleibt).

## Folie 9: Datensicherheit und DSGVO

*KRITERIUM 5 · DATENSICHERHEIT UND DSGVO*

SPRECHER: Erik · RICHTZEIT: 1:30 min — Was wir übertragen: Truck-ID, Temperaturen, Aktorwerte und Zeitstempel. In den Messdaten steckt kein Personenbezug, personenbezogen sind nur die Kontodaten des Teams bei MathWorks. Risiken: Laut MathWorks werden Daten dort gespeichert, wo MathWorks oder seine Dienstleister arbeiten, also auch in den USA. Das wäre eine Drittlandübermittlung. Wir haben im Verzeichnis nachgesehen: MathWorks ist im EU-US Data Privacy Framework aktiv gelistet, zertifiziert seit 2016. Das gilt aber nur für Nicht-Beschäftigtendaten, bei Fahrerdaten wäre es keine Grundlage. Der Kanal ist bewusst öffentlich, weil er nur nicht-sensible Messdaten enthält und Prüfer den Verlauf ohne Anmeldung sehen können. Geschrieben werden kann nur mit dem geheimen Write Key. Aufbewahrung: 12 Monate als unsere Festlegung, dazu monatlich ein CSV-Export. Im Realbetrieb wäre der Kanal privat, mit EU-Hosting und Auftragsverarbeitungsvertrag. Details stehen in DATENSCHUTZ.md. ÜBERGABE: Weiter mit der sicheren Datenübertragung (Erik bleibt).

## Folie 10: Sichere Datenübertragung

*KRITERIUM 6 · KONZEPT SICHERE DATENÜBERTRAGUNG*

SPRECHER: Erik · RICHTZEIT: 1:30 min — Unser Konzept in sechs Punkten. Verschlüsselung: nur HTTPS. Authentifizierung: Der Write Key liegt nur auf dem Pi, und wir haben die Keys bereits einmal erneuert. Geheimnisse: in einer .env-Datei mit eingeschränkten Rechten, nie im Git-Repository. Vollständigkeit: Jede Messung hat eine lokale ID, der Cursor rückt erst nach erfolgreichem Upload weiter, nach einem Funkloch wird nachgeholt. Nachweisbarkeit: UTC-Zeitstempel, Pi-Zeit per NTP. Minimale Rechte: Die Bridge liest die Datenbank nur und läuft ohne Zusatzrechte. Nachweise zeigen: curl auf ThingSpeak für TLS, ls -l der .env, git check-ignore. Ehrlich benannte Grenzen: Das Web-Terminal des Pi hat noch keine eigene Anmeldung, die Pi-Uhr hat keine Batterie, und der Free-Tarif bietet keinen Löschschutz, deshalb bleibt das Original in der lokalen Datenbank. Details stehen im SICHERHEITSKONZEPT.md. ÜBERGABE: Ich übergebe an Felix: Ergebnis, Zusatzfunktionen und Fazit.

## Folie 11: Messdaten in der Cloud

*KRITERIUM 7 · MESSDATEN PROTOKOLLIERT UND VISUALISIERT*

SPRECHER: Felix · RICHTZEIT: 1:30 min — Hier zeigen wir die Ergebnisse. LIVE-DEMO oder Screenshot: ThingSpeak-Kanal mit Temperaturverlauf, Lüfter und Ventil. Die Messung läuft alle 5 Sekunden. Der Upload wird wegen der Free-Grenze alle 15 Sekunden gebündelt, jede Messung behält ihre eigene Uhrzeit. Es gibt 8 Felder, und der CSV-Export dient als Nachweis für Kontrollen. Der Kanal ist öffentlich, deshalb kann jeder ohne Anmeldung zuschauen. VOR DEM VORTRAG: Pi vorher durchlaufen lassen und prüfen, dass die Punkte im 5-Sekunden-Abstand ankommen. ÜBERGABE: Weiter mit den Zusatzfunktionen (Felix bleibt).

## Folie 12: Mehr als nur speichern

*KRITERIUM 8 · ZUSÄTZLICHE FUNKTIONEN*

SPRECHER: Felix · RICHTZEIT: 1:00 min — Store and Forward: Bei einem Funkloch werden fehlende Messungen später mit ihrer Originalzeit nachgeliefert. Health-Flags: Die Bridge warnt schon am Truck bei zu hoher Temperatur, abweichenden Sensoren oder einem eingefrorenen Sensor. Alarm: Sobald Field 3 über 30 Grad steigt, startet ThingSpeak React eine MATLAB-Analyse, die eine Nachricht an unseren Discord-Server und eine E-Mail schickt. Die Zugangsdaten liegen nur in ThingSpeak. Laut My Account sind 800 Alarm-Mails im Jahr erlaubt. Sensor-Drift: Ein MATLAB-Diagramm in ThingSpeak zeigt pro Minute, wie weit die beiden Temperatursensoren auseinanderliegen, mit gleitendem Mittelwert und Warnschwelle bei 3 Grad. Wächst die Abweichung stetig, deutet das auf einen defekten Sensor oder Wackelkontakt hin, und die Wartung lässt sich planen, bevor der Truck ausfällt. VOR DEM VORTRAG: Pi vorher durchlaufen lassen, damit das Diagramm frische Minutenwerte zeigt. ÜBERGABE: Weiter mit dem Fazit (Felix bleibt).

## Folie 13: Fazit und Ausblick

*ABSCHLUSS*

SPRECHER: Felix · RICHTZEIT: 1:00 min — Wir erfüllen die Nachweispflicht deutlich besser: Die Daten kommen automatisch und zeitnah in die Cloud und sind von überall abrufbar. Sie sind doppelt gesichert, lokal im Pi und in der Cloud. Ausblick: Für den echten Flottenbetrieb würden wir Azure IoT Hub mit EU-Region wählen, die Alarme ausbauen und die Sensor-Drift-Auswertung zur Wartungsplanung der ganzen Flotte nutzen. Gelernt: Unsere Bridge trennt Logik und Sender, der Anbieter lässt sich austauschen. ThingSpeak jetzt, Azure für die Flotte. Vielen Dank, wir freuen uns auf eure Fragen. ÜBERGABE: Fragen beantwortet, wer fachlich dran ist (siehe Rückfragen im Redemanuskript).
