# Präsentation "Digitaler Tresor" (Freitag, 28.08.2026)

- **`tresor-praesentation.md`** – Quelldatei im [Marp](https://marp.app/)-Format (Markdown-Folien). Das ist die Datei, die bei Änderungen bearbeitet werden sollte.
- **`tresor-praesentation.html`** – fertig gerenderte, eigenständige Version zum direkten Präsentieren im Browser (kein Internet/Installation nötig, einfach öffnen). Pfeiltasten/Bildlauf zum Blättern.

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

10 Folien, ausgelegt auf die 10-Minuten-Vorgabe: Aufgabe → Idee → Hardware → Architektur → Team/Tracks → Pi-Dashboard-Erweiterung → Lessons Learned → Live-Demo-Ankündigung → Danke. Die Live-Demo selbst (Tresor öffnen, Alarm auslösen, Dashboard zeigen, Publikum darf knacken) läuft am echten Aufbau, nicht in den Folien.
