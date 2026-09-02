---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0109 (Dienstag) – Teampathy Map, Personas & Ideation

Aufgabenliste für Dienstag, 01.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Case ist final entschieden: **Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung** (siehe [[Team 13 - Digitale Demokratie]] Abschnitt "Finale Case-Entscheidung"). Wie gestern: Alles mit 📝 markiert **muss vor Ort/im Team passieren**, kein Schreibtisch-Ersatz möglich.

## Aufgaben von heute (Original, Workshop-Vorgabe)
- Work on the Teampathy Map (time-boxed to no more than 45 minutes) – share it on the team board
- Add a group photo and a motto
- Add your group working room to the team board
- Find someone on your team who can facilitate the design thinking process today and tomorrow – share this role on the team board
- Describe your target group using personas and employ at least one method to empathise with the user and understand the problem
- Use 1 method for the ideation round (e.g. 6-3-5 method or Walt Disney method)
- Share all results on the team board
- Keep all work timeboxed

## 📝 Nur vor Ort möglich
- **Teampathy Map** (45 Min) – das offizielle Template vom Haupt-Board ist [`team-canvas.pdf`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/templates/team-canvas.pdf) (siehe [[Team 13 - Digitale Demokratie]] für die 5 Spalten Goals/Roles/Purpose/Values/Rules), noch nicht als Entwurf ausgefüllt (📝 muss vor Ort passieren, echtes Gespräch zu dritt). Das generische [`empathy-map-template.pdf`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/templates/empathy-map-template.pdf) (Says/Thinks/Does/Feels) liegt ebenfalls im Repo, falls zusätzlich zur Team Canvas noch eine klassische Empathy-Map-Runde gemacht wird.
- Gruppenfoto + Motto aufs Team-Board
- Arbeitsraum eintragen
- Facilitator für heute+morgen bestimmen (Vorschlag: rotierend, da nur 3 Personen im Team – siehe Walt-Disney-Methode unten, die sich ideal auf 3 Rollen aufteilt)
- Alles aufs Team-Board teilen (siehe [[DTEW Hamburg - Übersicht]] zur Board-Struktur)

## ✅ Vorbereitet: Proto-Personas für Case 3 (Feed-Design)

> [!warning] Ersetzt die alten Case-1-Personas
> Lena/Jamal (siehe [[Team 13 - Digitale Demokratie]]) waren auf Hate Speech zugeschnitten. Diese hier passen zum final gewählten Case 3.

**1. "Mia, 20, merkt nicht, dass sie in einer Bubble steckt"**
- Folgt vor allem Accounts/Themen, die ihre bestehende Meinung bestätigen
- Pain Point: sieht praktisch nie überzeugende Gegenargumente, ist manchmal überrascht/vor den Kopf gestoßen, wenn Freund:innen anders denken
- Bedürfnis: möchte eigentlich informiert und ausgewogen bleiben – merkt aber gar nicht, dass ihr das mit dem aktuellen Feed entgeht (unbewusstes Problem)

**2. "Tom, 22, will aus seiner Bubble raus, findet aber keinen Weg"**
- Hat selbst bemerkt, dass sein Feed einseitig ist, sucht aktiv nach anderen Perspektiven
- Pain Point: Algorithmus zeigt ihm trotzdem immer wieder Ähnliches; aktiv nach Gegenmeinungen suchen fühlt sich mühsam an
- Bedürfnis: ein Feed, der ihm auch mal eine gut aufbereitete Gegenperspektive zeigt, ohne dass er selbst danach suchen muss – aber ohne ihn mit komplett irrelevantem Kram zu fluten (bewusstes Problem, direkt aus der digi&demo-Fragestellung "varied but still topically relevant")

### Empathize-Methode (mind. 1 gefordert)
Vorschlag: **Kurzinterviews mit 2-3 anderen Workshop-Teilnehmenden**, konkrete Frage: *"Zeig mir deinen 'For You'-Feed – findest du den eher vielfältig oder zeigt der dir immer ähnliches?"* Ergänzt die bereits gemachte Sekundärquellen-Recherche (digi&demo-Input) um echte Nutzer:innen-Perspektive – schnell machbar zwischen den Workshop-Sessions.

## ✅ Vorbereitet: Ideation-Methode

**Empfehlung: Walt-Disney-Methode** ([offizielles Template](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/templates/fiedler-disney-method-english.pdf) vom Haupt-Board) statt 6-3-5 – passt besser zu einem 3er-Team:
- **Träumer:in** (eine Person): völlig frei spinnen, keine Machbarkeits-Fragen erlaubt – "Wie sähe der perfekte Feed aus, wenn alles möglich wäre?"
- **Realist:in** (eine Person): wie könnte man die Traum-Ideen tatsächlich technisch umsetzen (Bezug zu Lasses Vorschlag: Recommender-Testumgebung auf existierenden Frameworks)?
- **Kritiker:in** (eine Person): was könnte schiefgehen, was fehlt noch, wo hakt's?

Danach eine Runde rotieren (jede:r übernimmt eine andere Rolle), damit nicht eine Person dauerhaft nur "Kritiker" ist. Zeitlich boxen, z.B. 10 Min pro Rolle + 10 Min Zusammenfassung.

*(6-3-5-Methode ist eher für 6 Personen ausgelegt – mit 3 Leuten entweder mit mehreren Runden pro Person strecken oder eben die Walt-Disney-Methode nehmen, die von Natur aus auf 3 Rollen passt.)*

## ✅ Vorbereitet: Team-Board-Karte (Problem / Solution / Target Group / Tech Stack)

Fertiger Text für die Team-13-Karte im Teams-Übersicht-Board (Workshop-Sprache Englisch, zum Reinkopieren):

**Problem:**
> Social media "For You" feeds are optimized for engagement, which reinforces filter bubbles and self-selected echo chambers. Some users don't even notice they're in a bubble; others notice but can't break out because the algorithm keeps showing similar content. This weakens exposure to diverse, topically relevant perspectives — a core challenge for healthy democratic discourse (digi&demo e.V.'s focus).

**Target Group:**
> Young adults (18–25) who consume political/social content mainly through algorithmic feeds (Instagram, TikTok, X) — both those unaware they're in a bubble ("Mia, 20") and those aware but stuck in it ("Tom, 22").

**Solution ideas:**
> A recommender/feed prototype that deliberately mixes well-curated, topically relevant counter-perspectives into a user's feed — instead of pure engagement-optimization. Built on an existing open-source recommender framework, adapted to demonstrate "varied but still relevant" ranking instead of pure similarity-based ranking.

**Technology stack:**
> Python backend for the recommender logic (on a sample content dataset), simple Flask web frontend to demo two feed versions side-by-side (bubble-reinforcing vs. diversity-aware) — same stack the team already used successfully for the Pi-Dashboard project in the Smart Systems short project.

> [!note] Tech-Stack ist ein Vorschlag
> Basiert auf dem, was im Team schon erfolgreich genutzt wurde (Python/Flask, Tresor-Pi-Dashboard) und passt zu Lasses Empfehlung "basierend auf existierenden Frameworks". Bei Bedarf im Team anpassen/bestätigen.

## Präsentations-/Abgabe-Version
Ausgefülltes `persona-template.pdf` als Markdown+HTML+PDF (Mia & Tom) liegt außerhalb des Vaults unter [`DTEW-Workshop/personas-mia-tom/`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/personas-mia-tom/personas-mia-tom.md) – siehe [[Doku-Regeln]] zur Konvention. Nach echten Interviews dort aktualisieren.

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[Team 13 - Digitale Demokratie]]
- [[TaskCards Board]]
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
