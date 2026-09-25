# Präsentation "The Ice Truck Problem(s)" – Fachgespräch Challenge I + II

- **`ice-truck-praesentation.pptx`** – PowerPoint-Version, 29 Folien, identischer Inhalt wie die HTML-Version. Öffnet in PowerPoint (Windows/Mac/Web) und in Keynote.
- **`ice-truck-praesentation.key`** – native Keynote-Version für Mac, aus der `.pptx` in Keynote selbst erzeugt (Datei → Sichern) und danach gegengeprüft (29 Folien, Bild-für-Bild identisch zur `.pptx`-Version). Einfach doppelklicken, öffnet direkt in Keynote.
- **`ice-truck-praesentation.md`** – Quelldatei im [Marp](https://marp.app/)-Format (Markdown-Folien) für die HTML-Version. Diese Datei bei Änderungen an der HTML-Version bearbeiten.
- **`ice-truck-praesentation.html`** – Browser-Version zum direkten Präsentieren (kein Internet/Installation nötig, einfach öffnen). Pfeiltasten/Bildlauf zum Blättern.
- **`redemanuskript.md`** – Sprechtext je Folie, aufgeteilt auf Anton/Felix/Dogan/Erik, mit Richtzeiten. Zum Üben, nicht auswendig lernen. Gilt für alle vier Versionen (Folienreihenfolge/-inhalt ist identisch).
- **`fragen-antworten.md`** – Vorbereitung auf mögliche Rückfragen im Fachgespräch, kein Folien-Teil.
- **`pptx-build/`** – Python-Skripte, mit denen die `.pptx` erzeugt wurde (`python-pptx`, kein Node/PowerPoint nötig). Nur relevant, falls die PowerPoint-Version später nochmal automatisiert neu gebaut werden soll, statt sie direkt in PowerPoint/Keynote zu bearbeiten.

**Welche Version nehmen?** Auf dem Mac/mit Keynote: `.key`. Mit Windows-PowerPoint oder um noch was am Text zu ändern: `.pptx` (öffnet überall). Ohne Office-Software, direkt im Browser: `.html`.

## Neu rendern nach Änderungen an der `.md` (HTML-Version)

```bash
cd Challenge-I-Ice-Truck/Praesentation
npx --yes @marp-team/marp-cli ice-truck-praesentation.md --html -o ice-truck-praesentation.html
```

Für eine PDF-Version wird zusätzlich ein installierter Browser (Chrome/Edge/Firefox) auf der Maschine gebraucht:

```bash
npx --yes @marp-team/marp-cli ice-truck-praesentation.md --pdf -o ice-truck-praesentation.pdf
```

**Wichtig:** Die `.pptx`/`.key`-Version wird davon **nicht** automatisch aktualisiert – Inhaltsänderungen müssten separat auch in `pptx-build/make_deck.py` nachgezogen und neu gebaut werden (oder einfach direkt in PowerPoint/Keynote editieren, das ist meist schneller für kleine Textänderungen).

## Struktur

Überblick → Hardware & Sensorik (Anton) → Datenübertragung & Speicherung (Felix) → Regellogik & Aktorik (Dogan) → MQTT & Topics (Erik) → Node-RED & Fernsteuerung (Anton) → Mobiles Endgerät & Status (Felix) → Fazit (Dogan). Jede:r hat 5 Folien am Stück, Rollen wechseln entlang der Datenfluss-Pipeline statt strikt pro Challenge – so kennt am Ende jede:r das Gesamtsystem, nicht nur den eigenen Teil.

## Design

Bewusst kein Corporate-Deck-Look (keine Stock-Grafiken, keine Gradient-Effekte) – jede:r bekommt seine eigene Farbe, die sich durch alle seine/ihre Folien zieht (Anton = Bernstein, Felix = Grün, Dogan = Violett, Erik = Blau, gemeinsame Folien = Eisblau): farbig getönter Hintergrund auf Titel-/Kapitelfolien, farbige Überschriften-Unterstreichung, farbiger Seitenzähler, ein handschriftlicher Font (Kalam) für Namen und kleine Anmerkungen statt durchgehend cleaner Systemschrift. Die beiden Architektur-Diagramme sind echte SVGs (kein ASCII) und in der Farbe der Person eingefärbt, die die Folie hält – wirkt wie mit eigenem Stift gezeichnet statt aus einer Vorlage generiert. Live-Demo-Momente haben ein gelbes, leicht schräg sitzendes "Textmarker"-Badge statt eines cleanen Icons. Jede Inhaltsfolie trägt oben klein den zugehörigen Bewertungspunkt samt Punktzahl (nur zur eigenen Orientierung, nicht zum Vorlesen – siehe `redemanuskript.md`) sowie eine handschriftlich wirkende, leicht schief sitzende "Challenge I"/"Challenge II"-Marke wie ein Sticky Note.

## Abgleich mit dem Bewertungsbogen

Vollständigkeitsprüfung gegen "Bewertungsbogen SmSy Fachgespräch_2026_ChI+II" – **jeder einzelne bewertete Punkt** (Ch I: 45 Pkt, Ch II: 55 Pkt, Summe 100 Pkt) ist einer Folie zugeordnet und auf dieser auch als Eyebrow-Text sichtbar gemacht:

| # | Bewertungspunkt (Wortlaut Bogen) | Pkt | Folie |
|---|---|---|---|
| Ch I.1 | An den Arduinos ist mind. 1 Sensor funktionstüchtig angeschlossen | 5 | Sensorik: von DHT22 zu 2× KY-028 |
| Ch I.2 | An den Arduinos ist mind. 1 LED funktionstüchtig angeschlossen | 4 | LED zeigt den Messwert *(Live-Demo)* |
| Ch I.3 | Leuchtstärke der LED ändert sich abhängig vom Sensorwert – wird gezeigt | 6 | LED zeigt den Messwert *(Live-Demo)* |
| Ch I.4 | Kommunikation mehrerer Arduinos mit dem Pi umgesetzt & beschreibbar | 5 | I2C-Kommunikation Pi ↔ beide Arduinos |
| Ch I.5 | Messdaten werden in einer SQL-Datenbank protokolliert | 4 | Messdaten in SQLite protokolliert |
| Ch I.6 | Formate der Daten der angeschlossenen Sensoren werden dargestellt | 5 | Datenformate der Sensoren |
| Ch I.7 | Lüfter wird vom Pi über den Arduino mit einem Transistor gesteuert¹ | 8 | Lüfter: Ansteuerung über Transistor *(Live-Demo)* |
| Ch I.8 | Ventil (Servomotor) wird vom Pi über den Arduino gesteuert | 3 | Ventil: Servo-Ansteuerung *(Live-Demo)* |
| Ch I.9 | Szenario ist sinnvoll erweitert worden | 5 | Szenario sinnvoll erweitert |
| **Σ Ch I** | | **45** | |
| Ch II.1 | Kommunikation über MQTT ist realisiert | 8 | MQTT-Broker: lokaler Mosquitto |
| Ch II.2 | Organisation und Hierarchie der Topics wird dargestellt | 5 | Topic-Schema & Hierarchie |
| Ch II.3 | Steuerung ist über Node-RED realisiert | 9 | Node-RED als Integrationsschicht |
| Ch II.4 | Weiteres digitales Endgerät über MQTT eingebunden | 8 | Mobiles Endgerät statt Eigenbau-App |
| Ch II.5 | Zusätzliche Funktionen sind realisiert worden | 8 | Fernsteuerung: auto/manual als Extra-Feature |
| Ch II.6 | Präsentation: Überblick, roter Faden, jede:r hat Anteil, Visualisierung, Zeitplanung | 10 | gesamtes Deck – Faden explizit auf "Worum geht's heute", Aufteilung auf "Team & Aufteilung" (inkl. Zeitangabe), Visualisierung = SVG-Diagramme statt ASCII |
| Ch II.7 | Rückfragen zu technischen Entscheidungen fachlich fundiert erläutert | 7 | `fragen-antworten.md` |
| **Σ Ch II** | | **55** | |
| **Gesamt** | | **100** | |

¹ Im Bogen-Wortlaut steht "Der Luftsensor wird ... mit einem Transistor gesteuert" – im Kontext (Transistor-Ansteuerung, Elegoo-Kit) ist damit erkennbar der **Lüfter** gemeint, nicht ein separater Luftsensor (den es im Aufbau nicht gibt). Falls beim Fachgespräch danach gefragt wird: kurz ansprechen und richtigstellen, steht auch in `fragen-antworten.md`.
