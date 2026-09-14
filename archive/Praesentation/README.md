# Präsentation "Digitaler Tresor" (Freitag, 28.08.2026)

- **`tresor-praesentation.md`** – Quelldatei im [Marp](https://marp.app/)-Format (Markdown-Folien). Das ist die Datei, die bei Änderungen bearbeitet werden sollte.
- **`tresor-praesentation.html`** – fertig gerenderte Version zum direkten Präsentieren im Browser (kein Internet/Installation nötig, einfach öffnen). Pfeiltasten/Bildlauf zum Blättern. **Nicht eigenständig** – braucht den `assets/`-Ordner im selben Verzeichnis (Bilder sind per Pfad eingebunden, nicht eingebettet).
- **`assets/`** – Bilder für die Folien (aktuell: Tinkercad-Schaltplan).
- **`fragen-antworten.md`** – Vorbereitung auf mögliche Rückfragen, kein Folien-Teil.

## Neu rendern nach Änderungen an der `.md`

```bash
cd Praesentation
npx --yes @marp-team/marp-cli tresor-praesentation.md --html --allow-local-files -o tresor-praesentation.html
```

Für eine PDF-Version wird zusätzlich ein installierter Browser (Chrome/Edge/Firefox) auf der Maschine gebraucht, auf der gerendert wird:

```bash
npx --yes @marp-team/marp-cli tresor-praesentation.md --pdf --allow-local-files -o tresor-praesentation.pdf
```

## Struktur

Idee → Hardware → Aufbau (Schaltplan) → Architektur → Pi-Dashboard-Erweiterung → Lessons Learned → Live-Demo-Ankündigung → Danke. Die Live-Demo selbst (Tresor öffnen, Alarm auslösen, Dashboard zeigen, Publikum darf knacken) läuft am echten Aufbau, nicht in den Folien.
