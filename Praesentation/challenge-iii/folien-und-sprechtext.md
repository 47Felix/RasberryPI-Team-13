# Challenge III – Folien und Sprechtext

Automatisch aus den Folien-Quellen (`deck-source/`) erzeugt: Titel jeder Folie und der Sprechtext aus den Notizen. Die Reihenfolge entspricht der Präsentation.

## Folie 1: Ice Truck in der Cloud

*CHALLENGE III · IOT IN DER CLOUD*

Begrüßung. Kurz: Wir haben für den Ice Truck die Temperaturdaten vom Raspberry Pi automatisch in eine Cloud gebracht. Gleich zeigen wir, was wir ausgewählt haben, warum, wie sicher das ist und was dabei herauskam.

## Folie 2: Heute liegen die Daten nur im Truck

*01 · PROBLEM*

Ausgangslage aus der Aufgabe: Die Daten bleiben im Truck auf dem Pi und werden erst in der Zentrale von Hand gesichert. Gleichzeitig verlangen die EU-Verordnungen einen Nachweis, und Kühlung sowie Sensoren fallen immer wieder aus. Unser Ziel: automatisch in die Cloud, damit die Daten überall abrufbar sind und auch bei einem Pi-Ausfall erhalten bleiben.

## Folie 3: Vom Truck in die Cloud

*02 · LÖSUNG*

Der Weg der Daten: Die Arduinos messen, der Raspberry Pi regelt und speichert alles in einer SQLite-Datenbank. Unsere Cloud-Bridge liest nur neue Messungen aus dieser Datenbank und schickt sie per HTTPS an ThingSpeak. Die Datenbank ist gleichzeitig der Puffer: Fällt das Netz aus, wird später nachgeholt. In der Cloud gibt es Diagramme, Alarme und einen CSV-Export.

## Folie 4: Wir folgen dem Bewertungsbogen

*ÜBERBLICK*

Wir haben die Präsentation entlang des Bewertungsbogens aufgebaut. Jede Folie von 5 bis 12 beantwortet genau ein Kriterium, oben rechts steht die Punktzahl. So könnt ihr beim Zuhören direkt mitbewerten. Die größten Blöcke sind die sichere Datenübertragung und die Messdaten in der Cloud mit je 10 Punkten.

## Folie 5: Zwei Dienste im Vergleich

*KRITERIUM 1 · MINDESTENS ZWEI CLOUDDIENSTE*

Wir haben zwei Dienste im Detail verglichen: Azure IoT Hub als Plattform-Dienst und ThingSpeak als fertige IoT-Anwendung. Kriterien aus der Aufgabe: Protokolle, Speicherung, Visualisierung, Kosten, Datenschutz. Zusätzlich angeschaut: AWS IoT Core braucht eine Kreditkarte, die Arduino Cloud speichert im Free-Tarif nur einen Tag, und eine eigene VM wäre IaaS mit viel Betriebsaufwand. Die Free-Limits von ThingSpeak vor dem Vortrag noch einmal auf der Webseite prüfen.

## Folie 6: ThingSpeak – mit Azure als Plan A

*KRITERIUM 2 · TECHNISCH BEGRÜNDETE ENTSCHEIDUNG*

Ehrlich erzählt: Plan A war Azure IoT Hub. Code, Einrichtungsskript und Auswertung standen schon, aber der Zugriff auf unser Azure-Schülerkonto ging am 30.09. nicht. Weil unsere Bridge die Senderschicht von der restlichen Logik trennt, konnten wir ThingSpeak als zweites Backend ergänzen. Gründe für ThingSpeak: kostenlos ohne Kreditkarte, passende HTTPS-Schnittstelle, Speicherung und Diagramme sind eingebaut, sofort startklar. Für den späteren Flottenbetrieb bleibt Azure die Empfehlung (EU-Region, Archiv).

## Folie 7: Die fünf Cloud-Merkmale

*KRITERIUM 3 · NIST-KRITERIEN (SP 800-145)*

Die fünf Merkmale nach NIST. Wir erfüllen sie, aber nicht alle gleich stark, und das sagen wir offen: Self-Service und Broad Network Access sind klar erfüllt. Resource Pooling können wir nicht selbst überprüfen, das ist nur die Aussage des Herstellers. Rapid Elasticity gibt es nur über einen Lizenzwechsel, im Free-Tarif gelten feste Limits. Measured Service: Laut Licensing FAQ (Frage 16) zeigt die Seite My Account Restkontingent und Verbrauchsrate, ThingSpeak warnt auch bei knappem Kontingent. Dazu den Screenshot aus dem eigenen Konto zeigen. Elasticity: Weitere Units lassen sich jederzeit zukaufen, eine Unit sind 33 Millionen Nachrichten im Jahr und das Intervall sinkt auf 1 Sekunde. Im Free-Tarif nimmt der Kanal aber keine Daten mehr an, wenn das Kontingent leer ist. Ein privater Server zu Hause wäre keine Cloud, weil dort Pooling, Elastizität und verbrauchsabhängige Abrechnung fehlen.

## Folie 8: IaaS, PaaS oder SaaS?

*KRITERIUM 4 · EINORDNUNG IAAS, PAAS ODER SAAS*

Die Einordnung hängt davon ab, wer was verwaltet. Bei einer eigenen VM wäre es IaaS: Wir müssten Betriebssystem, Broker und Datenbank selbst betreiben. Azure IoT Hub ist PaaS: Die Plattform gehört dem Anbieter, wir betreiben nur unsere Geräte und die Auswertung. ThingSpeak ist SaaS: Wir konfigurieren nur einen Kanal in einer fertigen Anwendung und liefern Daten. Die MATLAB-Skripte sind ein Zusatz innerhalb dieser Anwendung, kein eigener Plattformbetrieb.

## Folie 9: Datensicherheit und DSGVO

*KRITERIUM 5 · DATENSICHERHEIT UND DSGVO*

Datenschutz-Einschätzung. Was wir übertragen: Truck-ID, Temperaturen, Aktorwerte und Zeitstempel. Im Prototyp ist das kein Personenbezug. Risiken: Der Anbieter sitzt in den USA, das ist eine Drittlandübermittlung. Und wenn die Truck-ID später einem Fahrer zugeordnet wird, könnten die Daten personenbezogen werden. Maßnahmen: nur nötige Daten, HTTPS und getrennte Keys (inzwischen erneuert), das Original bleibt lokal in der Datenbank. Der Kanal ist bewusst öffentlich, weil er nur nicht-sensible Messdaten enthält und Prüfer den Verlauf ohne Anmeldung sehen können. Geschrieben werden kann nur mit dem geheimen Write Key. Im Realbetrieb wäre der Kanal privat. Die Aufbewahrung legen wir auf 12 Monate fest (Annahme, passt zur Lizenzlaufzeit), dazu monatlich ein CSV-Export. Aus der MathWorks Privacy Policy (Stand März 2026): Daten werden dort gespeichert, wo MathWorks oder seine Dienstleister arbeiten, also nicht zwingend in der EU. Eintrag im Verzeichnis dataprivacyframework.gov am 07.10.2026 geprüft: The MathWorks, Inc. ist aktiver Teilnehmer im EU-US Framework (zertifiziert seit 2016, nächste Zertifizierung fällig 07/2027), in der UK-Erweiterung und im Swiss-US Framework. Abgedeckt sind Nicht-HR-Daten, also keine Beschäftigtendaten. Kämen später Fahrerdaten dazu, wäre das DPF-Zertifikat dafür keine Grundlage. Einen Auftragsverarbeitungsvertrag für Kunden nennt die Policy nicht, für den Prototyp ohne Personendaten ist das unkritisch. Die vollständige Einschätzung steht in DATENSCHUTZ.md, die technischen Maßnahmen im SICHERHEITSKONZEPT.md. Im Realbetrieb wäre eine EU-Region die bessere Wahl, und ein Unternehmen bräuchte die Standard-Lizenz.

## Folie 10: Sichere Datenübertragung

*KRITERIUM 6 · KONZEPT SICHERE DATENÜBERTRAGUNG*

Unser Konzept für die sichere Übertragung in sechs Punkten. Verschlüsselung: nur HTTPS. Authentifizierung: Der Write API Key liegt nur auf dem Pi, für Auswertungen gibt es einen getrennten Read Key. Geheimnisse: in einer .env-Datei mit eingeschränkten Rechten, nie im Git-Repository. Vollständigkeit: jede Messung hat eine lokale ID, der Cursor rückt erst nach erfolgreichem Upload weiter, nach einem Funkloch wird nachgeholt. Nachweisbarkeit: UTC-Zeitstempel, Pi-Zeit per NTP. Minimale Rechte: Die Bridge liest die Datenbank nur. Das Konzept steht ausführlich im SICHERHEITSKONZEPT.md, mit Bedrohungstabelle, Key-Rotation und Prüfbefehlen. Nachweise zeigen: curl auf ThingSpeak (TLS), ls -l der .env (nur Besitzer), git check-ignore. Ehrlich benannte Grenzen: Das Web-Terminal des Pi hat noch keine eigene Anmeldung, die Pi-Uhr hat keine Batterie, und der Free-Tarif bietet keinen Löschschutz wie ein Azure-Archiv, deshalb bleibt das Original in der lokalen Datenbank.

## Folie 11: Messdaten in der Cloud

*KRITERIUM 7 · MESSDATEN PROTOKOLLIERT UND VISUALISIERT*

Hier die Live-Demo oder den Screenshot zeigen: ThingSpeak, Private View des Kanals. Zu sehen sind die Temperaturen beider Sensoren sowie Lüfter und Ventil. Die Messung läuft im 5-Sekunden-Takt am Truck, der Upload wird wegen der Free-Grenze von einer Übertragung alle 15 Sekunden gebündelt, jede Messung behält ihre eigene Uhrzeit. Für Kontrollen gibt es den CSV-Export. Den Platzhalter links durch einen echten Screenshot ersetzen und vor dem Vortrag prüfen, dass die Punkte wirklich im 5-Sekunden-Abstand ankommen.

## Folie 12: Mehr als nur speichern

*KRITERIUM 8 · ZUSÄTZLICHE FUNKTIONEN*

Zusatzfunktionen. Schon umgesetzt: Store and Forward, also das Nachholen nach einem Funkloch, und die Health-Flags, die die Bridge schon am Truck berechnet. Dazu kommt der Alarm: Sobald Field 3 über 30 Grad steigt, startet ThingSpeak React eine MATLAB-Analyse. Sie schickt eine Nachricht in unseren Discord-Server und eine E-Mail. Die Zugangsdaten (Webhook, Alerts-Key) liegen nur in ThingSpeak, nicht im Repository. Laut My Account sind 800 Alarm-Mails pro Jahr erlaubt, zwei waren beim Testen schon verbraucht. Als Nächstes das MATLAB-Diagramm zur Sensor-Drift als Beispiel für Predictive Maintenance. VOR DEM VORTRAG: Wenn das Diagramm läuft, die Karte auf UMGESETZT setzen, sonst die Karte von der Folie löschen.

## Folie 13: Fazit und Ausblick

*ABSCHLUSS*

Fazit: Wir erfüllen die Nachweispflicht deutlich besser, weil die Daten automatisch, zeitnah und von überall abrufbar sind. Die Daten sind doppelt gesichert: lokal im Pi und in der Cloud. Ausblick: Für den echten Flottenbetrieb würden wir auf Azure IoT Hub mit EU-Region wechseln, die Alarme ausbauen und die Sensor-Drift für Predictive Maintenance nutzen. Gelernt: Weil unsere Bridge die Logik vom Sender trennt, konnten wir bei Problemen mit Azure schnell auf ThingSpeak ausweichen.
