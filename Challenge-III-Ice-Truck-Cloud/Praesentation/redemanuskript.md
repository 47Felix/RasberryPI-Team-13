# Redemanuskript Challenge III: „Ice Truck in der Cloud“

Aufteilung auf vier Sprecher, mit Richtzeiten und Sprechtext je Folie. Der gleiche Text steht in den **Notizen der PowerPoint-Datei** (`ice-truck-in-der-cloud.pptx`), im Referentenmodus auf dem zweiten Bildschirm sichtbar. Zum Üben, nicht auswendig lernen. Die Aufteilung ist ein Vorschlag, tauscht nach Belieben.

## Aufteilung

| Sprecher | Folien | Inhalt | Richtzeit | Bewertungspunkte |
|---|---|---|---|---|
| **Anton** | 1–4 | Titel, Problem, Lösung, Überblick Bewertungsbogen | 3:00 min | 0 |
| **Dogan** | 5–7 | Zwei Dienste im Vergleich (Kriterium 1), Entscheidung ThingSpeak (Kriterium 2), NIST-Merkmale (Kriterium 3) | 3:30 min | 15 |
| **Erik** | 8–10 | IaaS, PaaS oder SaaS (Kriterium 4), Datensicherheit und DSGVO (Kriterium 5), Sichere Datenübertragung (Kriterium 6) | 4:00 min | 20 |
| **Felix** | 11–13 | Messdaten in der Cloud (Kriterium 7), Zusätzliche Funktionen (Kriterium 8), Fazit und Ausblick | 3:30 min | 15 |
| **Gesamt** | 1–13 | | 14:00 min | 50 |

Die Richtzeiten sind Schätzwerte (ca. 130 Wörter pro Minute). Ist weniger Zeit vorgegeben, kürzt jede Person ihren Text auf die Kernaussagen und lässt Details weg.

## Ablauf und Sprechtext

### Anton (Folien 1–4, 3:00 min)

**Folie 1: Titel** (Richtzeit 0:30 min)

Guten Tag zusammen, wir sind Team 13-1. In Challenge III ging es darum, die Temperaturdaten vom Ice Truck automatisch in eine Cloud zu bringen. Ich beginne mit Problem und Lösung. Danach stellt Dogan die Cloud-Auswahl vor, Erik erklärt Datenschutz und Sicherheit, und Felix zeigt das Ergebnis, die Zusatzfunktionen und das Fazit.

*Übergabe:* Weiter mit Problem und Lösung (Anton bleibt).

**Folie 2: Problem** (Richtzeit 1:00 min)

Die Ausgangslage: Die Messwerte liegen bisher nur auf dem Raspberry Pi im Truck und werden erst in der Zentrale von Hand gesichert. Gleichzeitig verlangen die EU-Verordnungen 178/2002 und 37/2005 einen Nachweis der Temperaturen. Kontrolliert wird bisher nur stichprobenartig, und Sensoren oder Kühlaggregate fallen trotz Wartung immer wieder aus. Unser Ziel: Die Daten sollen automatisch in die Cloud, damit sie jederzeit und überall abrufbar sind und auch bei einem Ausfall des Pi erhalten bleiben.

*Übergabe:* Weiter mit unserer Lösung (Anton bleibt).

**Folie 3: Lösung** (Richtzeit 1:00 min)

So läuft es: Die Arduinos messen, der Raspberry Pi regelt und speichert jede Messung in einer SQLite-Datenbank. Unsere Cloud-Bridge, ein kleines Python-Programm, liest nur neue Messungen und schickt sie per HTTPS an ThingSpeak. Die Datenbank ist zugleich der Puffer: Fällt das Netz aus, wird später nachgeholt. In der Cloud gibt es Diagramme, Alarme und einen CSV-Export. Wir messen alle 5 Sekunden, jede Messung hat 8 Datenfelder, und der Free-Tarif kostet nichts.

*Übergabe:* Weiter mit dem Überblick zum Bewertungsbogen (Anton bleibt).

**Folie 4: Überblick Bewertungsbogen** (Richtzeit 0:30 min)

Wir haben die Präsentation entlang des Bewertungsbogens aufgebaut. Jede Folie von 5 bis 12 beantwortet genau ein Kriterium, oben rechts steht die Punktzahl. So könnt ihr direkt mitbewerten. Die größten Blöcke sind die sichere Datenübertragung und die Messdaten mit je 10 Punkten.

*Übergabe:* Ich übergebe an Dogan, er stellt die Clouddienste vor.

### Dogan (Folien 5–7, 3:30 min)

**Folie 5: Zwei Dienste im Vergleich (Kriterium 1)** (Richtzeit 1:00 min · 5 Punkte)

Wir haben mehrere Dienste angeschaut und stellen zwei im Detail vor: Azure IoT Hub von Microsoft und ThingSpeak von MathWorks. Verglichen haben wir nach den Kriterien aus der Aufgabe: Protokolle, Speicherung, Visualisierung, Kosten und Datenschutz. Azure ist eine Plattform mit MQTT, Archiv im Blob Storage und EU-Regionen. ThingSpeak ist eine fertige Anwendung mit HTTP und MQTT, eingebauten Diagrammen und Servern in den USA. Zusätzlich geprüft: AWS IoT Core braucht eine Kreditkarte, die Arduino Cloud speichert im Free-Tarif nur einen Tag, und eine eigene VM wäre IaaS mit viel Betriebsaufwand.

*Übergabe:* Weiter mit unserer Entscheidung (Dogan bleibt).

**Folie 6: Entscheidung ThingSpeak (Kriterium 2)** (Richtzeit 1:30 min · 5 Punkte)

Wir haben uns für ThingSpeak entschieden. Azure IoT Hub hatten wir ebenfalls vorbereitet, mit Einrichtungsskript und Auswertung. Am Ende hat uns ThingSpeak für unseren Prototyp aber besser gefallen, aus vier Gründen. Kosten: Es ist kostenlos und braucht keine Kreditkarte. Protokolle: Die HTTPS-Schnittstelle passt zu unserer Bridge und nimmt viele Messungen mit eigenem Zeitstempel an, MQTT wäre auch möglich. Speicherung und Visualisierung: Kanal, Diagramme und MATLAB sind eingebaut, wir brauchen keinen eigenen Server und waren in Minuten startklar. Datenschutz: Wir übertragen keine Personendaten, deshalb ist ein US-Anbieter vertretbar. Für eine ganze Flotte würden wir Azure empfehlen. FALLS GEFRAGT, warum nicht Azure: ehrlich antworten, dass der Zugang zu unserem Azure-Schülerkonto zum Start nicht verfügbar war und ThingSpeak dann alle Anforderungen erfüllt hat und uns besser gefallen hat.

*Übergabe:* Weiter mit den NIST-Merkmalen (Dogan bleibt).

**Folie 7: NIST-Merkmale (Kriterium 3)** (Richtzeit 1:00 min · 5 Punkte)

Die fünf NIST-Merkmale. Self-Service: Wir haben Konto und Kanal in Minuten selbst angelegt. Broad Network Access: HTTPS aus jedem Netz, Diagramme im Browser. Resource Pooling: Die Plattform bedient viele Kunden gemeinsam, das können wir aber nicht selbst überprüfen. Rapid Elasticity: Weitere Einheiten lassen sich jederzeit zukaufen, eine Einheit sind 33 Millionen Nachrichten im Jahr, im Free-Tarif gelten aber feste Limits und es gibt kein automatisches Skalieren. Measured Service: Auf der Seite My Account sehen wir Verbrauch und Restkontingent, dazu den Screenshot zeigen. Ein privater Server zu Hause wäre keine Cloud, weil Pooling, Elastizität und Abrechnung fehlen.

*Übergabe:* Ich übergebe an Erik: Einordnung, Datenschutz und Sicherheit.

### Erik (Folien 8–10, 4:00 min)

**Folie 8: IaaS, PaaS oder SaaS (Kriterium 4)** (Richtzeit 1:00 min · 5 Punkte)

Die Einordnung hängt davon ab, wer was verwaltet. Bei einer eigenen VM wäre es IaaS: Wir müssten Betriebssystem, Broker und Datenbank selbst betreiben. Azure IoT Hub ist PaaS: Die Plattform gehört dem Anbieter, wir betreiben nur Geräte, Routing und Auswertung. ThingSpeak ist SaaS: Wir konfigurieren nur einen Kanal in einer fertigen Anwendung und liefern Daten. Die MATLAB-Skripte sind ein Zusatz innerhalb dieser Anwendung, kein eigener Plattformbetrieb.

*Übergabe:* Weiter mit Datensicherheit und DSGVO (Erik bleibt).

**Folie 9: Datensicherheit und DSGVO (Kriterium 5)** (Richtzeit 1:30 min · 5 Punkte)

Was wir übertragen: Truck-ID, Temperaturen, Aktorwerte und Zeitstempel. In den Messdaten steckt kein Personenbezug, personenbezogen sind nur die Kontodaten des Teams bei MathWorks. Risiken: Laut MathWorks werden Daten dort gespeichert, wo MathWorks oder seine Dienstleister arbeiten, also auch in den USA. Das wäre eine Drittlandübermittlung. Wir haben im Verzeichnis nachgesehen: MathWorks ist im EU-US Data Privacy Framework aktiv gelistet, zertifiziert seit 2016. Das gilt aber nur für Nicht-Beschäftigtendaten, bei Fahrerdaten wäre es keine Grundlage. Der Kanal ist bewusst öffentlich, weil er nur nicht-sensible Messdaten enthält und Prüfer den Verlauf ohne Anmeldung sehen können. Geschrieben werden kann nur mit dem geheimen Write Key. Aufbewahrung: 12 Monate als unsere Festlegung, dazu monatlich ein CSV-Export. Im Realbetrieb wäre der Kanal privat, mit EU-Hosting und Auftragsverarbeitungsvertrag. Details stehen in DATENSCHUTZ.md.

*Übergabe:* Weiter mit der sicheren Datenübertragung (Erik bleibt).

**Folie 10: Sichere Datenübertragung (Kriterium 6)** (Richtzeit 1:30 min · 10 Punkte)

Unser Konzept in sechs Punkten. Verschlüsselung: nur HTTPS. Authentifizierung: Der Write Key liegt nur auf dem Pi, und wir haben die Keys bereits einmal erneuert. Geheimnisse: in einer .env-Datei mit eingeschränkten Rechten, nie im Git-Repository. Vollständigkeit: Jede Messung hat eine lokale ID, der Cursor rückt erst nach erfolgreichem Upload weiter, nach einem Funkloch wird nachgeholt. Nachweisbarkeit: UTC-Zeitstempel, Pi-Zeit per NTP. Minimale Rechte: Die Bridge liest die Datenbank nur und läuft ohne Zusatzrechte. Nachweise zeigen: curl auf ThingSpeak für TLS, ls -l der .env, git check-ignore. Ehrlich benannte Grenzen: Das Web-Terminal des Pi hat noch keine eigene Anmeldung, die Pi-Uhr hat keine Batterie, und der Free-Tarif bietet keinen Löschschutz, deshalb bleibt das Original in der lokalen Datenbank. Details stehen im SICHERHEITSKONZEPT.md.

*Übergabe:* Ich übergebe an Felix: Ergebnis, Zusatzfunktionen und Fazit.

### Felix (Folien 11–13, 3:30 min)

**Folie 11: Messdaten in der Cloud (Kriterium 7)** (Richtzeit 1:30 min · 10 Punkte)

Hier zeigen wir die Ergebnisse. LIVE-DEMO oder Screenshot: ThingSpeak-Kanal mit Temperaturverlauf, Lüfter und Ventil. Die Messung läuft alle 5 Sekunden. Der Upload wird wegen der Free-Grenze alle 15 Sekunden gebündelt, jede Messung behält ihre eigene Uhrzeit. Es gibt 8 Felder, und der CSV-Export dient als Nachweis für Kontrollen. Der Kanal ist öffentlich, deshalb kann jeder ohne Anmeldung zuschauen. VOR DEM VORTRAG: Pi vorher durchlaufen lassen und prüfen, dass die Punkte im 5-Sekunden-Abstand ankommen.

*Übergabe:* Weiter mit den Zusatzfunktionen (Felix bleibt).

**Folie 12: Zusätzliche Funktionen (Kriterium 8)** (Richtzeit 1:00 min · 5 Punkte)

Store and Forward: Bei einem Funkloch werden fehlende Messungen später mit ihrer Originalzeit nachgeliefert. Health-Flags: Die Bridge warnt schon am Truck bei zu hoher Temperatur, abweichenden Sensoren oder einem eingefrorenen Sensor. Alarm: Sobald Field 3 über 30 Grad steigt, startet ThingSpeak React eine MATLAB-Analyse, die eine Nachricht an unseren Discord-Server und eine E-Mail schickt. Die Zugangsdaten liegen nur in ThingSpeak. Laut My Account sind 800 Alarm-Mails im Jahr erlaubt. Sensor-Drift: Ein MATLAB-Diagramm in ThingSpeak zeigt pro Minute, wie weit die beiden Temperatursensoren auseinanderliegen, mit gleitendem Mittelwert und Warnschwelle bei 3 Grad. Wächst die Abweichung stetig, deutet das auf einen defekten Sensor oder Wackelkontakt hin, und die Wartung lässt sich planen, bevor der Truck ausfällt. VOR DEM VORTRAG: Pi vorher durchlaufen lassen, damit das Diagramm frische Minutenwerte zeigt.

*Übergabe:* Weiter mit dem Fazit (Felix bleibt).

**Folie 13: Fazit und Ausblick** (Richtzeit 1:00 min)

Wir erfüllen die Nachweispflicht deutlich besser: Die Daten kommen automatisch und zeitnah in die Cloud und sind von überall abrufbar. Sie sind doppelt gesichert, lokal im Pi und in der Cloud. Ausblick: Für den echten Flottenbetrieb würden wir Azure IoT Hub mit EU-Region wählen, die Alarme ausbauen und die Sensor-Drift-Auswertung zur Wartungsplanung der ganzen Flotte nutzen. Gelernt: Unsere Bridge trennt Logik und Sender, der Anbieter lässt sich austauschen. ThingSpeak jetzt, Azure für die Flotte. Vielen Dank, wir freuen uns auf eure Fragen.

*Übergabe:* Fragen beantwortet, wer fachlich dran ist (siehe Rückfragen im Redemanuskript).

## Mögliche Rückfragen und Antworten

Wer fachlich dran ist, antwortet. Vorschlag in Klammern.

**Warum ThingSpeak und nicht Azure?** (Dogan) Beide Dienste haben wir verglichen, Azure IoT Hub haben wir auch vorbereitet. Für unseren Prototyp hat uns ThingSpeak besser gefallen: kostenlos ohne Kreditkarte, Diagramme und Auswertung eingebaut, kein eigener Server, in Minuten startklar. Ehrlich dazu: Der Zugang zu unserem Azure-Schülerkonto war zum Start nicht verfügbar. Für eine ganze Flotte würden wir Azure empfehlen (EU-Region, unveränderliches Archiv, Schlüssel pro Gerät).

**Ist das wirklich eine Cloud nach NIST?** (Dogan) Ja: Self-Service, Zugriff über das Internet, gemeinsam genutzte Plattform, zukaufbare Kapazität und gemessener Verbrauch. Einschränkungen nennen wir offen: Pooling können wir nicht prüfen, und im Free-Tarif gibt es feste Limits ohne automatisches Skalieren. Ein Pi zu Hause wäre keine Cloud.

**Warum ist das SaaS und nicht PaaS?** (Erik) Wir konfigurieren nur einen Kanal in einer fertigen Anwendung und betreiben keine Plattform. Die MATLAB-Skripte sind eine Funktion der Anwendung. Bei Azure IoT Hub (PaaS) würden wir Routing und Auswertung selbst bauen.

**Was passiert bei Netzausfall?** (Felix) Store and Forward: Jede Messung wird zuerst lokal in der Datenbank gespeichert. Die Bridge merkt sich, bis wohin die Cloud bestätigt hat, und schickt nach dem Ausfall alles Fehlende mit der Originalzeit nach. Vorführbar mit `sudo systemctl stop cloud-bridge`, kurz warten, `start`.

**Wie sicher ist die Übertragung?** (Erik) HTTPS mit Zertifikatsprüfung, Schreiben nur mit dem geheimen Write Key, Keys nur in der `.env` des Pi (chmod 600, nicht im Git) und bereits einmal erneuert. Die Bridge liest die Datenbank nur. Grenzen: Pi-Terminal ohne Anmeldung, Uhr ohne Batterie, kein Löschschutz bei ThingSpeak.

**Warum ist der Kanal öffentlich?** (Erik) Er enthält nur nicht-sensible Messdaten, und Prüfer können den Verlauf ohne Anmeldung sehen, das passt zum Ziel der Nachweispflicht. Schreiben geht nur mit dem geheimen Key. Im Realbetrieb wäre er privat und nur für Berechtigte freigegeben.

**Ist das DSGVO-konform?** (Erik) In den Messdaten steckt kein Personenbezug. MathWorks ist im EU-US Data Privacy Framework aktiv gelistet, das gilt für Nicht-Beschäftigtendaten. Bei Fahrerdaten bräuchte es eine andere Grundlage, EU-Hosting und einen Auftragsverarbeitungsvertrag.

**Warum messt ihr alle 5 Sekunden und ladet alle 15 Sekunden hoch?** (Felix) ThingSpeak Free erlaubt höchstens ein Update alle 15 Sekunden pro Kanal. Die Bridge bündelt deshalb drei Messungen, jede mit ihrer eigenen Uhrzeit. So geht keine Messung verloren.

**Wie lange werden die Daten aufbewahrt?** (Felix) Wir haben 12 Monate festgelegt, weil uns keine Frist vorgegeben war. Dazu ein monatlicher CSV-Export, das Original bleibt in der lokalen Datenbank. Im Realbetrieb müsste die gesetzliche Frist geklärt werden.

**Was kostet der Betrieb für eine Flotte?** (Dogan) Der Free-Tarif gilt nur für nicht-kommerzielle Projekte mit einem Limit von 3 Millionen Nachrichten im Jahr und 4 Kanälen. Ein Unternehmen bräuchte die kostenpflichtige Standard-Lizenz oder Azure IoT Hub.
