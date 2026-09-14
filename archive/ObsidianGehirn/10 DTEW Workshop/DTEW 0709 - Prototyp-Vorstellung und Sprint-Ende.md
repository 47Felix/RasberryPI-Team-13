---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0709 (Montag) – Prototyp-Vorstellung, Planning Board & Sprint-Ende

Vorbereitung für Montag, 07.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Case bleibt **Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung**, Personas Mia/Tom. Diese Notiz konsolidiert die Präsentations-Vorbereitung aus [[DTEW 0509 - Freier Tag und Vorbereitung auf Montag]] und ergänzt das nachträglich angelegte Kanban-Board. Wie an den Vortagen: Alles mit 📝 markiert **muss vor Ort/live im Team passieren**.

## Aufgaben von heute (laut Haupt-Board, live geprüft 07.09. morgens)

- Daily (was letzte Woche gemacht, was heute, Blocker)
- Input "From ideas to Business" + Social Business Model Canvas / Business Model Canvas (Vorlagen vom Haupt-Board)
- **11:00 Peer-Feedback-Sessions**
- **11:00 Erste Prototyp-Version + Planung zeigen**: Zielgruppe/Personas, Bedürfnisse/Pain Points, Kernfeatures, was bewusst weggelassen wurde, **Planning Board zeigen (Aufgabenverteilung erklären)**
- Retrospektive – Sprint-Ende
- 14:00 KIXX Kicker-Turnier (Anmelde-Umfrage steht auf dem Board)

## 📝 Nur vor Ort/live möglich

- **Daily** – ehrliche Antworten
- **Peer-Feedback-Gespräch** selbst
- **Prototyp-Vorstellung** – Inhalt unten vorbereitet, der eigentliche Vortrag/Live-Demo braucht das Team
- **Retrospektive** – echte Team-Reflexion, hier bewusst nicht vorweggenommen (siehe [Issue #98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))
- **Rollen (Scrum Master/Product Owner) final festlegen** und auf dem Teams-Übersicht-Board eintragen ([Issue #99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))

## ⚠️ Wichtiger Kontext: Kanban-Board nachträglich angelegt

Donnerstag (03.09.) sollte laut Haupt-Board ein Kanban-Board angelegt und Rollen (mind. Scrum Master + Product Owner) verteilt werden. Dazu existierte weder eine Vault-Notiz noch ein Eintrag auf dem Teams-Übersicht-Board (anders als z.B. Team 1, 5, 12, die dort "Roles"/"Sprint Planning (Kanban-Board)"-Karten haben) – vermutlich ist das schlicht untergegangen. Da die heutige 11-Uhr-Aufgabe explizit "Show your planning board, explain your planning and the distribution of the tasks" verlangt, wurde am Montagmorgen nachträglich eines aufgesetzt:

- **Kanban-Board:** [`DTEW-Workshop/kanban-board/kanban-board.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/kanban-board/kanban-board.md) (To Do / In Progress / Done), unterlegt mit echten GitHub Issues [#92–#102](https://github.com/47Felix/RasberryPI-Team-13/issues?q=is%3Aissue+92..102+in%3Anumber)
- Rollen-Felder sind darin bewusst leer gelassen – das ist eine echte Team-Entscheidung, keine, die sich nachträglich erfinden lässt
- **Vor der Präsentation:** kurz zu zweit/dritt Rollen eintragen (im Kanban-Dokument UND auf der Team-13-Karte im Teams-Übersicht-Board), damit "Planning: Show your planning board" ehrlich beantwortet ist

## ✅ Vorbereitet: Prototyp-Vorstellung für 11:00 Uhr

*(Übernommen und gegen den aktuellen Code-Stand geprüft, siehe `Code/feed-diversity-prototype/` – Stand 07.09. morgens: Single-Feed-UI mit Tab-Switch, Supabase-Anbindung für nutzergenerierte Posts, Vielfalts-Score.)*

**Zielgruppe/Personas:**
- **Mia (20)**, "The Everyperson" – merkt nicht, dass ihr Feed fast ausschließlich eine Perspektive zeigt; sieht sich selbst als informiert.
- **Tom (22)**, "The Seeker" – merkt die Einseitigkeit, versucht aktiv auszubrechen, wird vom Algorithmus aber immer wieder zurückgezogen.
- Vollständige Steckbriefe: [`DTEW-Workshop/personas-mia-tom/personas-mia-tom.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/personas-mia-tom/personas-mia-tom.md)

**Bedürfnisse:**
- Mia: Sichtbarmachen des eigenen Bubble-Effekts, ohne dass sie aktiv danach suchen muss.
- Tom: ein Werkzeug, das ihn zuverlässig mit thematisch relevanten Gegenperspektiven versorgt.
- Gemeinsam: Transparenz – nachvollziehen können, *warum* ein Post im Feed erscheint.

**Kernfeatures (aktueller Code-Stand):**
- Single-Feed-UI mit Tab-Umschalter zwischen **Standard** (reine TF-IDF-Ähnlichkeit, bubble-verstärkend) und **Diversity-aware** (mischt bewusst thematisch passende Gegenperspektiven ein, markiert als "Vorgeschlagen")
- Persona-Schnellauswahl ("Ansicht als Mia/Tom")
- **Vielfalts-Score**: sichtbare Kennzahl für Perspektivenvielfalt – Antwort auf den Mittwoch-Kritikpunkt "fehlende Metrik"
- Nutzergenerierte Posts über Supabase (Titel/Text/Kategorie/Perspektive), TF-IDF-Kategorie-Vorschlag, anonymes Like-Toggle; degradiert sauber auf statischen Datensatz falls Supabase nicht erreichbar

**Was bewusst weggelassen wurde:**
- Kein selbst trainiertes ML-Modell – klassisches Content-Based Filtering reicht für die Kernfrage
- Likes fließen nicht ins Ranking ein (Scope-Grenze)
- Keine echte Plattform-Integration (Bluesky/Mastodon wäre nächster Schritt, kein MVP-Bestandteil)
- Kein visuelles Logo, kein finaler Produktname (Textkonzept "Perspektivenkompass" liegt vor)

**Planning (neu für heute):** Kanban-Board zeigen (siehe oben), kurz erklären: Backlog/Done-Stand, wer woran arbeitet (sobald Rollen eingetragen sind).

> [!tip] Für die Live-Runde
> Reihenfolge Zielgruppe → Bedürfnis → Feature → Grenze → Planning lässt sich fast direkt als 1-2-Minuten-Vorstellung sprechen.

## Was noch fehlt

- [ ] Rollen (Scrum Master/Product Owner) im Team festlegen und eintragen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- [ ] Retrospektive durchführen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))
- [ ] Supabase-Token widerrufen ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92))
- [ ] Team-13-Karte auf dem Teams-Übersicht-Board mit Freitag-Stand + Kanban-Link aktualisieren
- [ ] Donnerstag rückwirkend dokumentieren ([#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97))
- [ ] Übrige Punkte siehe [Kanban-Board](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/kanban-board/kanban-board.md)

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[Team 13 - Digitale Demokratie]]
- [[DTEW 0509 - Freier Tag und Vorbereitung auf Montag]]
- [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]
- [`DTEW-Workshop/kanban-board/kanban-board.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/kanban-board/kanban-board.md)
- [[TaskCards Board]]
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
