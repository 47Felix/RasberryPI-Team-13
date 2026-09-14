---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0911 (Freitag, Woche 2) – Pitches, Innovation Fair & Abschlusssession

Vorbereitung für Freitag, 11.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Case bleibt **Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung**, Arbeitstitel weiterhin "Perspective Compass"/"Perspektivenkompass" (Namensentscheidung weiterhin offen, [#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)). Wie an den Vortagen: Alles mit 📝 markiert **muss vor Ort/live im Team passieren**.

> [!success] Board-Zugriff heute Nacht erfolgreich – anders als 09./10.09.
> Anders als in [[DTEW 0909 - Stand-Vorbereitung, Blogpost und Website-Eintrag]] und [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] dokumentiert (dort beide Nächte 403/`connect_rejected` beim direkten `curl`-Zugriff aus der Cloud-Sandbox) konnte heute Nacht **Playwright direkt gegen `itech-bs14.taskcards.app`** erfolgreich beide Boards öffnen (`waitUntil: networkidle`), Volltext lesen und Screenshots erstellen – sowohl das Haupt-Board als auch das Teams-Übersicht-Board.
> - **Teams-Übersicht-Board:** Team-13-Karte war entgegen der alten Annahme in [[DTEW Hamburg - Übersicht]] ("unsere Team-13-Karte dort ist aktuell noch leer") längst befüllt (Team members, Problem, Lösungsidee, Zielgruppe, Tech-Stack, 3 PDFs). Heute Nacht **ergänzt** (nicht überschrieben): neue Karte **"Status – Friday 11/09"** unten in der Team-13-Spalte hinzugefügt, mit kurzem Status + Freitags-Plan (Text siehe unten). Vor/nach dem Edit erneut live gegengelesen, keine leere Karte liegen geblieben, keine Nachbar-Spalte (Team 12/14) berührt.
> - **Ungeklärt:** Ob der separate VM-Cronjob `board-sync.sh` (laut [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100), Kanban „Done" seit 07.09.) unabhängig von diesem Lauf ebenfalls aktiv ist/war. Falls ja, besteht ein kleines Risiko von doppelten/widersprüchlichen Board-Updates in derselben Nacht – bitte morgens früh einmal gegenchecken, ob die Team-13-Karte nur die eine neue Karte von heute Nacht zusätzlich hat und nicht doppelt beschrieben wurde.
> - Live-Issue-Check (GitHub, heute Nacht): [#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93) (Name), [#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96) (Logo), [#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99) (Rollen), [#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98) (Retro) sind alle weiterhin **offen, ohne Kommentare** – seit Erstellung (07.09.) keine Fortschritts-Spur auf GitHub sichtbar.

## Aufgaben von morgen (Freitags-Spalte auf dem Haupt-Board, live gelesen – nicht nur aus der Übersicht)

> [!warning] Korrektur gegenüber der bisherigen Annahme
> Die bisherigen Notizen (0909/0910, basierend auf der Übersicht vom 01.09.) gingen von **"12:00 Uhr Pitches"** am Donnerstag aus. Die tatsächliche Freitags-Spalte auf dem Haupt-Board zeigt: **Pitches sind erst Freitag, 10:00 Uhr**, nicht Donnerstagmittag. Donnerstag hatte laut Board gar keinen Pitch-Termin, nur die Blogpost-Deadline (12:00) und Marktstand-Vorbereitung. Falls der Pitch gestern (10.09.) schon vorgetragen wurde, ist das zusätzlich zum Plan gewesen – heute ist der eigentliche, vom Haupt-Board vorgesehene Pitch-Termin.

- **Preparation and set up market stands** – Rooms 23/119/215/217/225: Stand gestalten (reale + digitale Ergebnisse kombinieren), Monitore/Boards/Flipcharts nutzen, Prototypen zeigen (Besucher:innen selbst ausprobieren lassen), Prozess zeigen (Personas, Empathy Map, Kanban-Board etc. am Stand)
- **Workshop-T-Shirt tragen**
- **Gruppenfoto**
- **10:00 Uhr Pitches, Room 23** – max. 1 Minute, keine Folien nötig
- **10:30 Uhr Innovation Fair** – Präsentation der Ergebnisse, Fair/Marktplatz mit Ständen (dieselben Show-Prototyp/Show-Prozess-Punkte wie beim Stand-Aufbau)
- **13:00–13:30 Uhr Closing Session** – Feedback zum "2026 International Design and Entrepreneurship Model Workshop", Room 23

Kein Daily-Fragen-Kärtchen und kein Blogpost-Punkt in der Freitags-Spalte gefunden (anders als an den Vortagen) – Freitag ist laut Board reiner Präsentations-/Abschlusstag.

## 📝 Nur vor Ort/live möglich

- **Pitch tatsächlich üben, laut, mit Stoppuhr** – Skript unten (aus dem 10.09.-Entwurf übernommen, weiterhin gültig) auf **10:00 Uhr Room 23** statt Mittag einstellen; wer vorträgt ist weiterhin offen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- **Marktstand tatsächlich aufbauen** – Poster/Flyer aus dem 09.09.-Entwurf müssen gedruckt vorliegen (siehe [[DTEW 0909 - Stand-Vorbereitung, Blogpost und Website-Eintrag]])
- **Live-Demo-URL am Stand bereithalten** – laut [[Feed-Diversity-Prototyp - Deployment]] läuft der Prototyp auf einer festen Azure-VM, aber ohne fest dokumentierte öffentliche Domain/IP im Vault/Repo (`deploy/README.md` nutzt nur Platzhalter `<domain>`) – die tatsächliche URL vor Ort bei Felix/Anton erfragen
- **Prüfen, ob der gestrige (10.09.) Blogpost bis 12:00 Uhr tatsächlich veröffentlicht wurde** – laut [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] war das Automation-seitig nicht prüfbar (Login/Format der Website)
- **Produktname/Logo final entscheiden** ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)/[#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96)), **Rollen festlegen** ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)), **Retro nachholen** ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98)) – alle laut heutigem Live-Check weiterhin ohne jede Aktivität seit 07.09.
- **Supabase-Token widerrufen** ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92)) – Sicherheitsvorfall vom 04.09., weiterhin offen, sollte vor dem letzten Workshop-Tag nicht liegen bleiben
- **Team-13-Karte auf dem Team-Board morgens gegenchecken** – heute Nacht nur ergänzt (siehe Warnkasten), nicht überschrieben; bitte kurz bestätigen, dass es nicht doppelt/inkonsistent aussieht
- **Farewell-Party-Buffet/3P-Voting** – Links standen bereits auf der Donnerstags-Spalte des Haupt-Boards (Voting-Formular + Buffet-Sign-up), falls im Team noch nicht erledigt

## ✅ Vorbereitet: 1-Minuten-Pitch-Skript (Room 23, 10:00 Uhr, keine Folien)

Unverändert aus dem 10.09.-Entwurf übernommen (weiterhin inhaltlich passend, ~130 Wörter ≈ 55–60 Sek.):

> "Hi, we're Team 13. Every 'For You' feed is optimised for engagement, not balance — and that quietly builds filter bubbles. We met two people while designing this: Mia, 20, who doesn't realise she's in a bubble, and Tom, 22, who knows it and can't get out. So we built **Perspective Compass** — one feed, two switchable modes. Standard mode behaves like your real feed: it reads your like history and reinforces your dominant view a little more each time, on purpose, so the mechanism becomes visible instead of hidden. Diversity-aware mode uses the same signal to do the opposite: it deliberately mixes in relevant counter-perspectives, clearly marked, and shows a diversity score so the difference is measurable, not just claimed. No black-box ML, no algorithm guessing your politics — you label your own posts. Come find our stand and see your own bubble from the outside."

> [!tip] Für die Live-Probe
> - Name "Perspective Compass" ist Arbeitstitel ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)) – bei finaler Entscheidung im Skript ersetzen.
> - Termin ist heute **10:00 Uhr, Room 23** (nicht mehr Mittag wie im 10.09.-Entwurf angenommen) – entsprechend früh am Morgen einplanen, nicht erst kurz vorher.
> - Wer vorträgt, ist offen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)).

## ✅ Erledigt heute Nacht: Team-13-Status-Karte auf dem Team-Board

Folgende Karte wurde live im Teams-Übersicht-Board in der Team-13-Spalte ergänzt (unterhalb der drei bestehenden PDF-Karten, per Spalten-"+"):

> **Status – Friday 11/09**
> Prototype ("Perspective Compass", name still tentative) is live: standard vs. diversity-aware feed ranking (TF-IDF + cosine similarity), real Supabase accounts, likes/comments, live diversity score. Today: final stand setup + t-shirts + group photo, 10:00 pitch (Room 23, 1 min, no slides), 10:30 Innovation Fair, 13:00-13:30 Closing Session. Open: final product name/logo, roles, retro.

Nach dem Speichern erneut geladen und bestätigt: Karte liegt korrekt in der Team-13-Spalte, keine leere/doppelte Karte in Team 13 oder den Nachbar-Spalten (Team 12, Team 14).

## Was noch fehlt

- [ ] Prüfen, ob der 10.09.-Blogpost tatsächlich bis 12:00 Uhr veröffentlicht wurde (offener Punkt aus [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]])
- [ ] Pitch-Skript laut üben, Zeit stoppen (10:00 Uhr Room 23!), Vortragende(n) festlegen
- [ ] Marktstand aufbauen (gedrucktes Poster/Flyer vom 09.09. muss vorliegen), Live-Demo-URL/VM-Adresse vor Ort besorgen
- [ ] Produktname final entscheiden ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)), Logo gestalten ([#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96))
- [ ] Rollen (Scrum Master/Product Owner) festlegen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- [ ] Retrospektive durchführen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))
- [ ] Supabase-Token widerrufen ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92)) – Sicherheitsvorfall, seit 04.09. offen
- [ ] Team-13-Karte auf dem Team-Board morgens früh gegenchecken (heute Nacht ergänzt, s.o.) und klären, ob `board-sync.sh` auf der VM parallel/unabhängig ebenfalls läuft
- [ ] Donnerstag (03.09.) rückwirkend dokumentieren ([#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97))
- [ ] Farewell-Party-Voting/Buffet-Sign-up, falls noch offen
- [ ] Übrige offene Punkte siehe [Kanban-Board](https://47felix.github.io/RasberryPI-Team-13/DTEW-Workshop/kanban-board/) bzw. [Issues #92–#102](https://github.com/47Felix/RasberryPI-Team-13/issues?q=is%3Aissue+92..102+in%3Anumber)

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]]
- [[DTEW 0909 - Stand-Vorbereitung, Blogpost und Website-Eintrag]]
- [[DTEW - Strategie-Praesentation]]
- [[Team 13 - Digitale Demokratie]]
- [`DTEW-Workshop/strategy-presentation/`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/strategy-presentation/strategy-presentation.md)
- [`Code/feed-diversity-prototype/README.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/README.md)
- [[Feed-Diversity-Prototyp - Deployment]]
- [[TaskCards Board]]
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
