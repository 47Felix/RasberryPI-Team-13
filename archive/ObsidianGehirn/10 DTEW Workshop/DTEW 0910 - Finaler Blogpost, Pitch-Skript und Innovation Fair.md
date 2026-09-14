---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0910 (Donnerstag, Woche 2) – Finaler Blogpost, 1-Minuten-Pitch & Innovation Fair

Vorbereitung für Donnerstag, 10.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Case bleibt **Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung**, Arbeitstitel weiterhin "Perspective Compass" (Team-Entscheidung zu Name/Logo weiterhin offen, [#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)/[#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96)). Wie an den Vortagen: Alles mit 📝 markiert **muss vor Ort/live im Team passieren**, kein Schreibtisch-Ersatz möglich. Diese Notiz wurde nachts von der Automation erstellt, **ohne** Zugriff auf das echte Board (siehe Warnkasten) – bitte morgens früh gegenprüfen.

> [!danger] Board-Zugriff heute Nacht erneut geprüft und erneut gescheitert – Widerspruch zu Issue #100 gefunden
> Live getestet (`curl` gegen `itech-bs14.taskcards.app` direkt aus dieser Cloud-Sandbox): weiterhin `403`/`connect_rejected` auf den CONNECT-Tunnel, identisch zum seit 03.09. dokumentierten Befund (siehe [[TaskCards Board]]). Weder Haupt-/Teams-Board noch das Team-13-Gruppenboard konnten gelesen oder bearbeitet werden.
> **Wichtig für morgen:** [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100) ("Board-Zugriff der Nacht-Automation repariert") behauptet, das Problem sei am 07.09. durch Verlagerung auf einen lokalen Cronjob (`board-sync.sh` auf der VM) gelöst worden – das deckt sich aber nicht mit dem Befund der letzten Nacht (09.→10.09.), wo laut [[DTEW 0909 - Stand-Vorbereitung, Blogpost und Website-Eintrag]] derselbe Fehler erneut auftrat. Zwei Möglichkeiten: entweder läuft `board-sync.sh` auf der VM tatsächlich zuverlässig und diese Cloud-Automation ist inzwischen nur noch ein redundanter, erwartungsgemäß scheiternder zweiter Versuch – oder `board-sync.sh` läuft selbst nicht (mehr) zuverlässig und niemand hat es bemerkt, weil alle sich auf die (falsche) "repariert"-Meldung in Issue #100 verlassen. **Bitte morgens prüfen, ob `board-sync.sh` auf der VM tatsächlich läuft/geloggt hat**, sonst könnten seit 07.09. mehrere Nächte Board-Updates ausgefallen sein, ohne dass es auffällt.
> - Aufgabenliste unten stammt deshalb wie an den Vortagen **nur aus der Übersicht** (Stand Board 01.09.), nicht aus einer tagesaktuellen Donnerstags-Karte.
> - Team-13-Karte auf dem Gruppenboard konnte weder gelesen noch aktualisiert werden – Update von heute Nacht entfällt ersatzlos, siehe vorbereiteten Text unten zum Reinkopieren.
> - Unklar, ob es zwischen 07.09. und heute überhaupt ein echtes Board-Update aus der VM-Automation gab; falls nicht, könnte auch die Team-13-Karte insgesamt noch auf dem Stand vom 07./08.09. sein.

## Aufgaben von morgen (laut Übersicht, Stand Board 01.09. – s. Warnkasten zur Unsicherheit)
- Workshop-T-Shirt tragen
- **Finalen Blogpost bis 12:00 Uhr hochladen** (designentrepreneurshipworkshop.org)
- Marktstände aufbauen: Prototypen zeigen, Prozess dokumentieren
- **12:00 Uhr: Pitches in Raum 23** (max. 1 Minute, keine Slides)
- Innovation Fair / Marktplatz
- Gruppenfoto
- Abschlusssession + Feedback
- Farewell Party (Budget/Buffet im Team klären)

## 📝 Nur vor Ort/live möglich
- **Daily** – ehrliche Antworten, Gerüst unten als Vorschlag
- **Echtes Board morgens früh prüfen** – insbesondere klären, ob `board-sync.sh` auf der VM tatsächlich lief (siehe Warnkasten), und ob es für Donnerstag eine eigene Aufgabenkarte mit Details (Uhrzeiten Stand-Aufbau, Ort Innovation Fair) gibt
- **Pitch tatsächlich üben und laut sprechen** – Skript unten ist ein Textentwurf, keine geprobte Performance; 1 Minute ist knapp, unbedingt mit Stoppuhr testen und wer ihn vorträgt festlegen (Rollenfrage [#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99) weiterhin offen)
- **Marktstand tatsächlich aufbauen** – Poster/Flyer aus dem 09.09.-Entwurf (siehe [[DTEW 0909 - Stand-Vorbereitung, Blogpost und Website-Eintrag]]) müssen bereits gedruckt vorliegen; falls nicht, ist das jetzt dringend
- **Finalen Blogpost freigeben und veröffentlichen** – unten ein Entwurf, aber Team-Zusammensetzung/Anton (siehe Warnkasten im 09.09.-Entwurf) und Login/Format der Website prüft die Automation nicht
- **Team-13-Karte auf dem Gruppenboard aktualisieren** – heute Nacht nicht möglich, Text unten fertig zum Reinkopieren
- **Farewell-Party-Budget/Buffet** – reine Team-/Organisationsentscheidung, nicht vorwegnehmbar
- **Live-Demo-URL am Stand bereithalten** (aktuelle VM-IP vor Ort erfragen, siehe [[Feed-Diversity-Prototyp - Deployment]])

## ✅ Vorbereitet: 1-Minuten-Pitch-Skript (Raum 23, keine Slides)

Abgeleitet aus Folie 2 (Problem), Folie 4 (Lösung) und Folie 8 (Business Model, komprimiert) der [[DTEW - Strategie-Praesentation]], wie dort unter "Was noch fehlt" gefordert. Bewusst kurz gehalten (~130 Wörter ≈ 55-60 Sek. bei normalem Sprechtempo) – beim Üben mit Stoppuhr ggf. weiter kürzen:

> "Hi, we're Team 13. Every 'For You' feed is optimised for engagement, not balance — and that quietly builds filter bubbles. We met two people while designing this: Mia, 20, who doesn't realise she's in a bubble, and Tom, 22, who knows it and can't get out. So we built **Perspective Compass** — one feed, two switchable modes. Standard mode behaves like your real feed: it reads your like history and reinforces your dominant view a little more each time, on purpose, so the mechanism becomes visible instead of hidden. Diversity-aware mode uses the same signal to do the opposite: it deliberately mixes in relevant counter-perspectives, clearly marked, and shows a diversity score so the difference is measurable, not just claimed. No black-box ML, no algorithm guessing your politics — you label your own posts. Come find our stand and see your own bubble from the outside."

> [!tip] Für die Live-Probe
> - Name "Perspective Compass" ist noch Arbeitstitel ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)) – falls das Team bis morgen einen finalen Namen entscheidet, im Skript ersetzen.
> - Der letzte Satz ("Come find our stand...") ist der Call-to-Action Richtung Marktstand direkt danach – funktioniert nur, wenn der Stand zu dem Zeitpunkt schon steht.
> - Wer vorträgt, ist offen (Rollenfrage [#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)); laut Folie 11 sollen idealerweise alle im Team an der Gesamtpräsentation/Fair beteiligt sein, auch wenn nur eine Person die 60 Sekunden spricht.

## ✅ Vorbereitet: Finaler Blogpost-Entwurf (designentrepreneurshipworkshop.org)

*(Auf Englisch, Workshop-Sprache. Entwurf – Format/Länge vor Ort ans tatsächliche Blog-Format anpassen. Anders als der erste Blogpost vom 09.09. [Vorstellung des Vorhabens] fasst dieser das fertige Ergebnis zusammen, für die Deadline 12:00 Uhr.)*

---

**Team 13 — Perspective Compass: what we built to make filter bubbles visible**

Two weeks ago we picked Case 3 — feed and recommender design against filter-bubble reinforcement — in cooperation with digi&demo e.V. Today we're showing the finished prototype at the Innovation Fair.

**Perspective Compass** is a small Flask web app built around one idea: a feed with two switchable ranking modes, side by side. **Standard mode** works like a typical "For You" feed — it reads your like history and reinforces your dominant perspective a little more with every like, on purpose, because that mechanism is exactly what we wanted to make visible instead of hiding it. **Diversity-aware mode** uses the same signal to do the opposite: it deliberately mixes in topically relevant counter-perspectives, marked as "Suggested," and shows a diversity score so the difference between the two modes is measurable, not just claimed.

We built this for two people we kept in mind throughout: Mia, 20, who checks her feed constantly and feels informed but has never noticed that everything she sees already agrees with her; and Tom, 22, who has noticed his bubble and actively tries to escape it, but keeps getting pulled back by the algorithm. Two different failure modes, one feed that addresses both.

We deliberately kept the tech simple: classic content-based filtering (TF-IDF and cosine similarity), no self-trained ML model, and no automatic left/right classifier — political labels are chosen by the people who write the posts, not guessed by our app. A tool that silently claims "this is objectively left" would just reproduce the invisible algorithmic judgement our case is about.

The prototype runs on real accounts (Supabase Auth), with likes, comments, a read-only preview of the Fediverse, and a live diversity score. It's a standalone demo, not a replacement for anyone's real feed — but it shows the mechanism clearly enough to start a conversation, which is exactly what digi&demo e.V.'s work on open, constructive digital discourse is about too.

Come find our stand at the Innovation Fair if you want to see your own bubble from the outside for once — and thank you to everyone who gave us feedback along the way.

*Team 13, BHH — Felix, Erik, Dogan (workshop participation of a fourth team member, Anton, still to be confirmed on the official participant list — please correct before publishing if this has been resolved).*

---

> [!warning] Vor der Veröffentlichung prüfen
> - Team-Zusammensetzung im letzten Absatz gegenchecken (dieselbe offene Frage wie beim 09.09.-Entwurf, siehe [[DTEW Hamburg - Übersicht]])
> - Deadline ist laut Übersicht **12:00 Uhr** – vor den Pitches um 12:00 in Raum 23, ggf. zeitlich eng, morgens früh einplanen
> - Arbeitstitel "Perspective Compass" bei Bedarf durch finalen Namen ersetzen (wie beim Pitch-Skript oben)
> - Ob die Website ein bestimmtes Format/eine Zeichenbegrenzung/Bildpflicht vorschreibt, konnte die Automation weiterhin nicht prüfen (Board mit dem Website-Link nicht erreichbar)

## ✅ Vorbereitet: Kurzer Prozess-Zeitstrahl für den Marktstand (Prozessdokumentation)

Für die Aufgabe "Prozess dokumentieren" am Stand – eine knappe Zeitleiste, ergänzend zum Poster/Flyer-Inhalt vom 09.09.:

1. **31.08.–01.09.:** Case-Wahl (Case 3, digi&demo e.V.), erstes Brainstorming, Team Canvas, Personas Mia & Tom.
2. **02.09.:** Kritische Punkte, Problem Statements, Ideation (Walt-Disney-Methode).
3. **03.–04.09.:** Prototyping-Start, Kanban-Board, erste Ranking-Logik (TF-IDF/Cosine Similarity), Social Business Model Canvas, Marketing- und Onboarding-Konzept.
4. **07.–09.09.:** Erste Prototyp-Version präsentiert, echte Accounts (Supabase Auth), Likes/Kommentare, Vielfalts-Score, politische Einordnung als zweite Achse, read-only Fediverse-Vorschau, Live-Deployment.
5. **10.09.:** Finaler Blogpost, 1-Minuten-Pitch, Innovation Fair.

> [!tip] Für die Live-Gestaltung
> Eignet sich als kurze visuelle Zeitleiste neben Poster/Flyer – Details zu Zwischenständen jeweils in den verlinkten Tagesnotizen, falls am Stand nach Details gefragt wird.

## ✅ Vorbereitet: Daily-Gerüst

- **Gestern (09.09.):** Stand/Poster-Flyer-Inhalte vorbereitet, erster Blogpost-Entwurf erstellt (Veröffentlichung/Website-Eintrag laut Warnkasten vom 09.09. noch zu bestätigen).
- **Heute (10.09.):** Finalen Blogpost veröffentlichen (12:00-Deadline), Pitch üben und um 12:00 in Raum 23 halten, Marktstand aufbauen, Innovation Fair, Gruppenfoto, Abschlusssession, Farewell Party.
- **Blocker:** *(vor Ort ausfüllen — z.B. Board-Zugriffsproblem der Nacht-Automation, jetzt mit zusätzlicher Unsicherheit ob `board-sync.sh` überhaupt läuft (Warnkasten oben, [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100)), offene Rollenklärung ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)), fehlende Retro ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98)), Name/Logo weiterhin offen ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)/[#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96)))*

## ✅ Vorbereitet: Team-13-Karte fürs Gruppenboard (zum Reinkopieren, sobald Board erreichbar)

- **Stand Donnerstag, 10.09.:** Prototyp fertig und live (echte Accounts, Likes/Kommentare, Vielfalts-Score, politische Einordnung als zweite Achse, read-only Fediverse-Vorschau). Finaler Blogpost veröffentlicht, 1-Minuten-Pitch gehalten (Raum 23, 12:00), Marktstand bei der Innovation Fair aufgebaut.
- **Nächster Schritt:** Produktname/Logo final entscheiden ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)/[#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96)), Rollen festlegen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)), Retrospektive nachholen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98)).

*Hinweis: Falls die VM-Automation (`board-sync.sh`) seit dem 07./08.09. zuverlässig lief, ist die Karte eventuell schon aktueller als hier angenommen – vor dem Reinkopieren mit dem tatsächlichen Board-Stand abgleichen, nicht blind überschreiben.*

## Was noch fehlt

- [ ] **Klären, ob `board-sync.sh` auf der VM tatsächlich läuft** (siehe Warnkasten – Widerspruch zwischen Issue [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100) "repariert" und dem erneuten Fehlschlag heute Nacht aus der Cloud-Sandbox)
- [ ] Pitch-Skript oben laut üben, Zeit stoppen, Vortragende(n) festlegen
- [ ] Finalen Blogpost prüfen (insb. Team-Zusammensetzung/Anton) und bis 12:00 Uhr veröffentlichen
- [ ] Marktstand aufbauen (gedrucktes Poster/Flyer vom 09.09. muss vorliegen)
- [ ] Team-13-Karte auf dem Gruppenboard aktualisieren (heute Nacht nicht möglich, s.o.)
- [ ] Produktname final entscheiden ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)), Logo gestalten ([#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96)) – Entwurf von dnbk72 vom 08.09. existiert bereits, siehe [[DTEW - Strategie-Praesentation]]
- [ ] Rollen (Scrum Master/Product Owner) festlegen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- [ ] Retrospektive durchführen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))
- [ ] Supabase-Token widerrufen ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92))
- [ ] Donnerstag (03.09.) rückwirkend dokumentieren ([#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97))
- [ ] Farewell-Party-Budget/Buffet im Team klären
- [ ] Übrige offene Punkte siehe [Kanban-Board](https://47felix.github.io/RasberryPI-Team-13/DTEW-Workshop/kanban-board/) bzw. [Issues #92–#102](https://github.com/47Felix/RasberryPI-Team-13/issues?q=is%3Aissue+92..102+in%3Anumber)

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[DTEW 0909 - Stand-Vorbereitung, Blogpost und Website-Eintrag]]
- [[DTEW - Strategie-Praesentation]]
- [[Team 13 - Digitale Demokratie]]
- [`DTEW-Workshop/strategy-presentation/`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/strategy-presentation/strategy-presentation.md)
- [`Code/feed-diversity-prototype/README.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/README.md)
- [[Feed-Diversity-Prototyp - Deployment]]
- [[TaskCards Board]]
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
