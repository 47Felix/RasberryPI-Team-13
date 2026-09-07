---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0809 (Dienstag) – Weiterarbeit am Prototyp, Input "Final presentation", MiniaturWunderland

Vorbereitung für Dienstag, 08.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Case bleibt **Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung**. Ruhigerer Tag ohne festen Präsentationstermin am Team-Board – Hauptaufgabe ist Weiterarbeit am Prototyp. Wie an den Vortagen: Alles mit 📝 markiert **muss vor Ort/live im Team passieren**.

## Aufgaben von morgen (laut Haupt-Board, live geprüft 07.09. abends)

- Workshop-Start 09:00 in Raum 23, weitere Räume 119, 127, 215, 217, 225
- Daily (was gestern, was heute, Blocker)
- **Group work on prototype**: "Keep working on prototypes and deliverables!"
- **Input: Final presentation** – "Present your prototype", Foliensatz `Presenting prototypes_DTEW2026HH.pdf` vom Haupt-Board (Inhalt unten zusammengefasst)
- 13:30 Exchange session
- **16:00 MiniaturWunderland-Ausflug** (Kehrwieder 2/Block D, 20457 Hamburg), vorher Anmelde-Umfrage ("Voting Miniaturwunderland", Link auf dem Board)

## 📝 Nur vor Ort/live möglich

- **Daily** – ehrliche Antworten (heute leichter zu beantworten, siehe ✅ unten: gestern = Prototyp-Vorstellung/Retro/Sprint-Ende Montag)
- **Tatsächliche Weiterarbeit am Code/Prototyp** – welche der offenen Punkte als nächstes angegangen werden, muss das Team entscheiden
- **Input-Session "Final presentation"** – die Slides sind unten zusammengefasst, aber die Session selbst (Fragen, Diskussion) braucht das Team vor Ort
- **Abstimmen, wer zum MiniaturWunderland mitkommt** (Umfrage ausfüllen)
- Weiterhin offen aus Montag: **Rollen festlegen** ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)), **Retrospektive** ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))

## ✅ Vorbereitet: Antwort auf "Was haben wir gestern gemacht?" (fürs Daily)

*(Übernommen aus [[DTEW 0709 - Prototyp-Vorstellung und Sprint-Ende]] und gegen den Code-Stand von Montagabend geprüft.)*

Montag (07.09.) wurde die erste Prototyp-Version + Planung vorgestellt (11 Uhr) und der Sprint (Do 03.09.–Mo 07.09.) retrospektiv abgeschlossen. Am Prototyp selbst kam danach noch einiges dazu:

- Statischer Datensatz (`data/posts.json`) und die Persona-Schnellauswahl "Mia"/"Tom" komplett entfernt – der Feed zeigt jetzt ausschließlich echte Supabase-Posts, mit explizitem Leer-Zustand statt Platzhaltern
- Echte Accounts (Supabase Auth: Registrierung/Login/Logout) statt anonymer Session-Cookies, inkl. Profile mit Anzeigename/Handle
- Kommentare pro Post (aufklappbar, mit Formular), eigene Kommentare per Account löschbar (serverseitig auf Eigentümerschaft geprüft)
- **Neu und inhaltlich relevant für die Case-3-Demo:** Likes fließen jetzt ins Ranking ein – `ranking.dominant_perspective()` wertet die Like-Historie eines Accounts aus und lässt den Standard-Feed sich mit jedem weiteren Like stärker in eine Richtung verstärken (bewusst *ohne* eingebauten Ausweg – genau das ist der Demo-Punkt für die Bubble-Verstärkung). Der Diversity-aware-Feed nutzt denselben Wert, um die Account-Neigung gezielt zu durchbrechen
- Ein PostgREST-Ambiguitätsfehler beim `posts`↔`profiles`-Embed wurde behoben (expliziter Foreign-Key-Hint nötig, weil `likes` eine zweite many-to-many-Beziehung zwischen beiden Tabellen erzeugt)

> [!warning] Ältere Notiz veraltet
> Die Kernfeatures-Liste in [[DTEW 0709 - Prototyp-Vorstellung und Sprint-Ende]] (Stand Montagmorgen) nennt noch "Persona-Schnellauswahl" und "Likes fließen nicht ins Ranking ein" – beides stimmt nach den Montagabend-Commits nicht mehr. Aktueller Stand ist ausschließlich [`Code/feed-diversity-prototype/README.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/README.md) (Abschnitt "Aktueller Stand / offen").

## ✅ Vorbereitet: Input "Final presentation" – Struktur zum Mitdenken

Der Foliensatz `Presenting prototypes_DTEW2026HH.pdf` (Haupt-Board, Dienstag-Spalte) ist die Vorbereitung auf die **eigentliche** Abschlusspräsentation am 10./11.09. (Pitches Raum 23, Innovation Fair), nicht auf einen Termin morgen – aber die Struktur lässt sich schon jetzt mit unserem aktuellen Stand durchspielen, damit in der Session mitgearbeitet werden kann statt nur zuzuhören:

1. **Before you start**: Setting kennen, Publikum kennen, sich selbst vorbereiten – "it's not only products, it's also people"
2. **The setting**: Ablaufplan für den Pitch-Tag selbst (9:00 Stand aufbauen, 9:50 Gruppenfoto, 10:00 1-Min-Pitch Raum 23, 10:30 Innovation Fair, 12:30 Aufräumen, 13:00 Abschluss) – für morgen nicht relevant, erst für 10./11.09.
3. **The problem – the Why**: Storytelling, Kontext geben → passt zu unserem bestehenden Problem-Statement (Filterblasen/Echo-Kammern, digi&demo-Fokus)
4. **Your customer/users**: wer nutzt es, wie wird es Teil ihres Alltags → Personas Mia/Tom (Steckbriefe: [`personas-mia-tom.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/personas-mia-tom/personas-mia-tom.md)) – **Hinweis:** die Personas sind im Code nicht mehr als UI-Feature vorhanden (siehe oben), bleiben aber als Zielgruppen-Beschreibung für die Präsentation gültig
5. **Solution – the How**: Prototyp Schritt für Schritt erklären (wie funktioniert's, welche Features, was macht es besonders) → Standard- vs. Diversity-aware-Feed, Tab-Umschalter, Vielfalts-Score, Like-basierte Bubble-Verstärkung als Kernszene der Demo
6. **Business model**: kann kurz sein, sollte aber vorkommen – Value Proposition/Social Impact, Revenue-Modell, nächste Schritte → bisher nur im Social Business Model Canvas skizziert (siehe [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]), für den Pitch nochmal auf 2-3 Sätze eindampfen
7. **The team**: "An A-team with a B-idea is better than a B-team with an A-idea" – alle sollen bei der Präsentation eingebunden sein
8. **Final tips**: pünktlich sein, Blickkontakt, Stand gestalten, verschiedene Medien nutzen, alles vorher testen ("Perfect practice makes")

> [!tip] Für morgen
> Die Session lässt sich nutzen, um Punkt 5 (Solution) und 6 (Business Model) für unseren Fall schon mal laut durchzusprechen – das nimmt einen Teil der Vorbereitung für den 10./11.09. vorweg, wenn ohnehin am Prototyp weitergearbeitet wird.

## MiniaturWunderland (16:00)

Reines Freizeitprogramm, keine Aufgabe. 📝 Anmelde-Umfrage ("Voting Miniaturwunderland", Nextcloud-Link auf der Dienstag-Karte) im Team ausfüllen, falls Interesse besteht.

## Board-Update (heute erledigt)

Auf dem Teams-Übersicht-Board (eigenes Team-13-Board) war seit mehreren Tagen offen, die Karte zu aktualisieren (siehe "Was noch fehlt" in [[DTEW 0709 - Prototyp-Vorstellung und Sprint-Ende]]). Heute Abend erledigt:

- **Technology-stack-Karte** aktualisiert: nennt jetzt den tatsächlichen Stand (Flask + TF-IDF/Cosine Similarity + Supabase Auth/Postgres, Single-Feed-UI) statt der alten, überholten Beschreibung ("zwei Feed-Versionen nebeneinander")
- **Neue Karte "Planning board"** mit Link zum Live-Kanban-Board (`https://47felix.github.io/RasberryPI-Team-13/DTEW-Workshop/kanban-board/`) hinzugefügt

📝 **Nicht angefasst:** Das Feld "Target Group" auf der Team-13-Karte enthält aktuell fälschlich denselben Text wie "Technology stack" (vermutlich ein Copy-Paste-Versehen) – eine echte Zielgruppenbeschreibung fehlt dort. Bitte im Team kurz korrigieren (Vorschlag: Kurzfassung aus Mia/Tom-Personas).

## Was noch fehlt

- [ ] Rollen (Scrum Master/Product Owner) im Team festlegen und eintragen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- [ ] Retrospektive durchführen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))
- [ ] Supabase-Token widerrufen ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92))
- [ ] "Target Group"-Feld auf der Team-13-Karte im Teams-Übersicht-Board korrigieren (siehe oben)
- [ ] Donnerstag (03.09.) rückwirkend dokumentieren ([#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97))
- [ ] Business-Model-Teil (Punkt 6 oben) für den Pitch am 10./11.09. auf 2-3 Sätze zuspitzen
- [ ] Übrige Punkte siehe [Kanban-Board](https://47felix.github.io/RasberryPI-Team-13/DTEW-Workshop/kanban-board/) bzw. [Issues #92–#102](https://github.com/47Felix/RasberryPI-Team-13/issues?q=is%3Aissue+92..102+in%3Anumber)

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[DTEW 0709 - Prototyp-Vorstellung und Sprint-Ende]]
- [[Team 13 - Digitale Demokratie]]
- [`Code/feed-diversity-prototype/README.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/README.md)
- [`DTEW-Workshop/kanban-board/kanban-board.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/kanban-board/kanban-board.md)
- [[TaskCards Board]]
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
