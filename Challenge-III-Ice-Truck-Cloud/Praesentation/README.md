# Präsentation Challenge III: „Ice Truck in der Cloud“

Aufgebaut entlang des Bewertungsbogens (8 Kriterien, 50 sichtbare Punkte), 13 Folien, aufgeteilt auf vier Sprecher.

| Datei | Inhalt |
|---|---|
| **`ice-truck-in-der-cloud.pptx`** | PowerPoint-Datei mit 13 Folien. Der **Sprechtext steht in den Notizen** jeder Folie, mit Sprecher, Richtzeit und Übergabe. Im Referentenmodus (Bildschirmpräsentation mit Referentenansicht) sieht man die Notizen auf dem zweiten Bildschirm. Öffnet in PowerPoint und Keynote. |
| **`redemanuskript.md`** | Aufteilung auf Anton, Dogan, Erik und Felix mit Richtzeiten, Sprechtext je Folie, Übergaben und möglichen Rückfragen mit Antworten |
| `folien-und-sprechtext.md` | Folientitel und Sprechtext je Folie, direkt auf GitHub lesbar |
| `deck-source/` | Quelldateien der Live-Version (`deck.json` + `slides/*.html`) |
| Live-Version | https://claude.ai/artifact/VmjCaHCTtuXDeyr3WgLdfa (private Seite, im Teilen-Menü freigeben, damit andere sie öffnen können) |

## Aufteilung

| Sprecher | Folien | Richtzeit | Punkte |
|---|---|---|---|
| **Anton** | 1–4: Titel, Problem, Lösung, Überblick | 3:00 min | – |
| **Dogan** | 5–7: Clouddienste, Entscheidung, NIST | 3:30 min | 15 |
| **Erik** | 8–10: IaaS/PaaS/SaaS, Datensicherheit und DSGVO, sichere Übertragung | 4:00 min | 20 |
| **Felix** | 11–13: Messdaten, Zusatzfunktionen, Fazit | 3:30 min | 15 |

Gesamt ca. 14 Minuten. Die Aufteilung ist ein Vorschlag und lässt sich im `redemanuskript.md` und in den Notizen der Folien leicht ändern.

## Folien

| Folie | Inhalt | Bewertungskriterium | Punkte | Sprecher |
|---|---|---|---|---|
| 1 | Titel | | | Anton |
| 2 | Problem | | | Anton |
| 3 | Lösung: vom Truck in die Cloud | | | Anton |
| 4 | Überblick Bewertungsbogen | | | Anton |
| 5 | Zwei Dienste im Vergleich (ThingSpeak, Azure) | Mindestens zwei Clouddienste vorgestellt | 5 | Dogan |
| 6 | Entscheidung: ThingSpeak | Entscheidung technisch begründet | 5 | Dogan |
| 7 | NIST-Merkmale | NIST-Kriterien erfüllt oder Abweichungen begründet | 5 | Dogan |
| 8 | IaaS, PaaS oder SaaS | Einordnung begründet | 5 | Erik |
| 9 | Datensicherheit und DSGVO | Einschätzung zur Datensicherheit und DSGVO | 5 | Erik |
| 10 | Sichere Datenübertragung | Konzept zur sicheren Datenübertragung | 10 | Erik |
| 11 | Messdaten in der Cloud | Messdaten protokolliert und visualisiert | 10 | Felix |
| 12 | Zusätzliche Funktionen | Zusätzliche Funktionen realisiert | 5 | Felix |
| 13 | Fazit und Ausblick | | | Felix |

Die zugehörigen Dokumente stehen in [`../Code/`](../Code/): `ENTSCHEIDUNG.md`, `SICHERHEITSKONZEPT.md`, `DATENSCHUTZ.md`, `README.md`.

**Stand der PowerPoint-Datei (07.10.2026):** Die Datei ist von euch bearbeitet (Screenshot der ThingSpeak-Diagramme auf Folie 11) und ersetzt die von uns erzeugte Fassung. Die Folien-Quellen in `deck-source/` und die Live-Version bei claude.ai entsprechen noch der ursprünglichen Fassung, die `.pptx` ist die maßgebliche Datei.

**Stand 08.10.2026:** Auf Folie 12 ist die Karte „Sensor-Drift erkennen“ jetzt auf UMGESETZT gesetzt (MATLAB-Visualization in ThingSpeak, 1-Minuten-Mittel, Warnschwelle 3 °C). Sprechtext in den Notizen, im Redemanuskript und in `folien-und-sprechtext.md` entsprechend angepasst.

**Vor dem Vortrag noch tun:** Pi vorher durchlaufen lassen, damit Kanal und Drift-Diagramm frische Daten zeigen.
