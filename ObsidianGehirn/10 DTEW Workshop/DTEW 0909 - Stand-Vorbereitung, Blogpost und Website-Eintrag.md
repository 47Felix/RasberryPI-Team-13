---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0909 (Mittwoch, Woche 2) – Input "Final presentation", Stand-Vorbereitung, Blogpost & Website-Eintrag

Vorbereitung für Mittwoch, 09.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Case bleibt **Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung**, Arbeitstitel weiterhin "Perspective Compass" (siehe [[DTEW - Strategie-Praesentation]]). Wie an den Vortagen: Alles mit 📝 markiert **muss vor Ort/live im Team passieren**, kein Schreibtisch-Ersatz möglich. Diese Notiz wurde nachts von der Automation erstellt, **ohne** Zugriff auf das echte Board (siehe Warnkasten unten) – bitte morgens früh gegenprüfen.

> [!danger] Board-Zugriff heute Nacht erneut gescheitert (bekanntes, offenes Problem — [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100))
> Sowohl das Haupt-/Teamboard (`.../board/d71b077a-.../view`) als auch das Gruppenboard (`.../board/a653850b-.../view`) waren heute Nacht **nicht erreichbar**: die Sandbox-Netzwerk-Policy dieser Session blockiert `itech-bs14.taskcards.app` mit `403` auf Proxy-Ebene (organisatorische Policy-Ablehnung, nicht wiederholbar/umgehbar laut Proxy-Doku). Dasselbe Problem trat bereits am 04.09. auf (siehe [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]) und ist als offenes Issue [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100) getrackt – es ist seitdem **nicht behoben**. Konsequenzen für heute Nacht:
> - Die Aufgabenliste unten stammt **ausschließlich aus der `Übersicht`-Notiz** (Stand Board 01.09.), nicht aus der tagesaktuellen Mittwochs-Karte selbst.
> - **Wichtige Unsicherheit:** Die Dienstags-Notiz [[DTEW 0809 - Weiterarbeit am Prototyp und Final-Presentation-Input]] hatte den Punkt "Input: Final presentation" (Foliensatz `Presenting prototypes_DTEW2026HH.pdf`) bereits **für Dienstag** live vom Board übernommen (Stand 07.09. abends). Die (ältere) Übersicht listet denselben Input-Punkt für **Mittwoch**. Es ist unklar, ob die Session sich über beide Tage erstreckt/wiederholt wurde, oder ob der Termin zwischenzeitlich verschoben wurde – **bitte morgens als Erstes am echten Board prüfen, ob der Punkt heute nochmal ansteht oder bereits erledigt ist**, um doppelte Arbeit zu vermeiden.
> - Die Team-13-Karte auf dem Gruppenboard konnte weder gelesen noch aktualisiert werden – **Board-Update von heute Nacht entfällt ersatzlos**, jemand aus dem Team muss das unten vorbereitete Material morgens von Hand eintragen.
> - Der Google-Sheet-Link für den Website-Eintrag (siehe unten) liegt laut Übersicht auf der Mittwochs-Karte selbst und konnte deshalb ebenfalls nicht abgerufen werden.

## Aufgaben von heute (laut Übersicht, Stand Board 01.09. – s. Warnkasten zur Unsicherheit)
- Daily (gestern/heute/Blocker)
- **Input "Final presentation"** (Prototyp präsentieren) – ggf. bereits Dienstag behandelt, siehe Warnkasten
- **Stand/Präsentation vorbereiten**: Poster/Flyer in vernünftiger Menge drucken
- **Name + E-Mail für die Workshop-Website eintragen** (Google-Sheet-Link auf der Mittwochs-Karte)
- **Ersten Blogpost auf designentrepreneurshipworkshop.org erstellen**

## 📝 Nur vor Ort/live möglich
- **Daily** – ehrliche Antworten, Gerüst unten als Vorschlag
- **Echtes Board morgens prüfen** (Board-Zugriff heute Nacht gescheitert, siehe Warnkasten) – insbesondere klären, ob "Final presentation"-Input heute noch aussteht
- **Input-Session "Final presentation"** selbst, falls sie heute (nochmal) stattfindet – Struktur/Inhalte dazu bereits in [[DTEW 0809 - Weiterarbeit am Prototyp und Final-Presentation-Input]] durchgespielt, unten nicht wiederholt
- **Poster/Flyer tatsächlich gestalten und drucken** – unten nur ein Text-/Inhalts-Entwurf als Startpunkt, kein fertiges Layout; Druckmenge/-ort muss das Team vor Ort klären
- **Name + E-Mail ins Google Sheet eintragen** – personenbezogene Daten, Link nur auf dem (heute Nacht nicht erreichbaren) Board, kann/soll die Automation nicht selbst ausfüllen
- **Blogpost tatsächlich veröffentlichen** – unten ein publikationsreifer Entwurf, aber Login/Veröffentlichung auf der Workshop-Website braucht das Team
- **Team-13-Karte auf dem Gruppenboard aktualisieren** – heute Nacht nicht möglich (Warnkasten), Text unten fertig zum Reinkopieren

## ✅ Vorbereitet: Poster/Flyer-Inhalts-Entwurf (Text, kein Layout)

Kein fertiges visuelles Design (Layout/Gestaltung ist Teamarbeit vor Ort, siehe [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]] zur Logo-Idee "Perspektiven-Kompass"), sondern die Kerninhalte, kondensiert aus der [[DTEW - Strategie-Praesentation]] auf Poster-/Flyer-Länge:

**Headline:** *Perspective Compass* — *Your feed decides which opinions you see. We show you how.*

**Problem (1-2 Sätze):** "For You"-Feeds optimieren auf Engagement statt auf Ausgewogenheit. Manche merken ihre Bubble nicht (Mia, 20), manche merken sie und kommen trotzdem nicht raus (Tom, 22).

**Lösung (1-2 Sätze):** Ein Feed, zwei Modi im selben Interface: **Standard** (verstärkt die eigene Perspektive mit jedem Like) vs. **Diversity-aware** (mischt gezielt thematisch relevante Gegenperspektiven ein, sichtbar markiert). Ein Vielfalts-Score macht den Unterschied messbar statt nur behauptet.

**Warum es funktioniert (Bulletpoints):**
- Kein Blackbox-Algorithmus: Nutzer:innen sehen, was der Standard-Feed mit ihrer eigenen Like-Historie macht
- Kein erfundenes "objektiv links/rechts"-Label – Nutzer:innen labeln politische Einordnung selbst
- Klassisches Content-Based Filtering (TF-IDF/Cosine Similarity), kein Blackbox-ML

**Call to Action:** QR-Code auf die Demo-URL – **inzwischen live** (Stand 09.09., Vormittag, siehe [[Feed-Diversity-Prototyp - Deployment]] für Hosting/Deploy-Regeln), diese Notiz wurde nachts von der Automation vor dem Deploy erstellt und ist an dieser Stelle veraltet. Aktuelle Live-URL vor Ort erfragen statt aus dieser Notiz übernehmen, falls sich die VM-IP zwischenzeitlich geändert hat.

**Footer:** Team 13, BHH — DTEW Hamburg 2026 — in Zusammenarbeit mit digi&demo e.V.

> [!tip] Für die Live-Gestaltung
> Der Text oben ist bewusst kurz gehalten (Poster-Lesedistanz). Persona-Zitate ("I'm informed, I scroll through the news every day." / "I don't want my feed to just tell me I'm right.") eignen sich als visuelle Zitat-Elemente neben den beiden Feed-Modi, siehe [`personas-mia-tom/`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/personas-mia-tom/personas-mia-tom.md).

## ✅ Vorbereitet: Erster Blogpost-Entwurf (designentrepreneurshipworkshop.org)

*(Auf Englisch, da die Workshop-Website ein internationales Publikum hat. Entwurf – Tonalität/Länge vor Ort ans tatsächliche Blog-Format der Seite anpassen, das die Automation nicht einsehen konnte.)*

---

**Team 13 — Perspective Compass: making filter bubbles visible, one feed at a time**

Every one of us scrolls a "For You" feed that quietly optimises for engagement, not for a balanced picture. For our case (Case 3, in cooperation with digi&demo e.V.), we started with a simple but uncomfortable question: what if a feed showed you *how* it was shaping your view, instead of hiding it?

We met two very different people while building our personas. Mia, 20, checks her feed several times a day and feels well-informed — she has just never noticed that everything she sees already agrees with her. Tom, 22, has noticed his bubble and actively tries to escape it, but the algorithm keeps pulling him back to more of the same. Two failure modes, one root cause.

Our prototype, working title **"Perspective Compass,"** is a small Flask web app with one feed and two switchable modes. **Standard mode** behaves like a typical algorithmic feed: it reads your like history and reinforces your dominant perspective a little more with every like — on purpose, without a built-in way out, because that is exactly the mechanism we want to make visible. **Diversity-aware mode** uses the same signal to do the opposite: it deliberately mixes in topically relevant counter-perspectives, clearly marked as "Suggested," and shows a diversity score so the difference is measurable, not just claimed.

We were careful about what *not* to build. There is no self-trained ML model — classic content-based filtering (TF-IDF and cosine similarity) already answers our core question, and it is realistic to build well in two weeks. There is also no automatic left/right classifier: political labels on posts are chosen by the people who write them, not guessed by our app, because a tool that silently claims "this is objectively left" would reproduce the exact kind of invisible algorithmic judgement our case is about.

This week we are preparing to present the prototype and are looking forward to the Innovation Fair on 10./11.09. — come find our stand if you want to see your own bubble from the outside for once.

*Team 13, BHH — Felix, Erik, Dogan (workshop participation of a fourth team member, Anton, still to be confirmed on the official participant list)*

---

> [!warning] Vor der Veröffentlichung prüfen
> - Team-Zusammensetzung im letzten Absatz gegenchecken (siehe offene Frage zu Anton in [[DTEW Hamburg - Übersicht]])
> - Ob die Seite ein bestimmtes Format/eine Zeichenbegrenzung/Bildpflicht für den ersten Post vorschreibt, konnte heute Nacht nicht geprüft werden (Board mit dem Website-Link nicht erreichbar)
> - Working Title "Perspective Compass" ist noch keine Team-Entscheidung (siehe [#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)) – bei Veröffentlichung ggf. anpassen, falls der Name bis dahin feststeht

## ✅ Vorbereitet: Daily-Gerüst

- **Gestern (08.09.):** Weiterarbeit am Prototyp, Input "Final presentation" durchgespielt (siehe [[DTEW 0809 - Weiterarbeit am Prototyp und Final-Presentation-Input]]), Team-13-Karte auf dem Gruppenboard aktualisiert (Technology-Stack korrigiert, Planning-Board-Karte ergänzt), MiniaturWunderland-Ausflug (16:00).
- **Heute (09.09.):** Stand/Poster-Flyer-Vorbereitung, Website-Eintrag (Name/E-Mail), ersten Blogpost veröffentlichen, ggf. Final-presentation-Input (siehe Warnkasten).
- **Blocker:** *(vor Ort ausfüllen — z.B. Board-Zugriffsproblem der Nacht-Automation (Warnkasten oben, [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100)), offene Rollenklärung ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)), fehlende Retro ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98)))*

## ✅ Vorbereitet: Team-13-Karte fürs Gruppenboard (zum Reinkopieren, sobald Board erreichbar)

- **Stand Mittwoch, 09.09.:** Prototyp läuft mit echten Accounts (Supabase Auth), Likes/Kommentaren, Vielfalts-Score, politischer Einordnung (links/mitte/rechts) als zweiter Achse und einer schreibgeschützten Fediverse-Vorschau. Poster/Flyer-Inhalte und ein erster Blogpost-Entwurf liegen vor (siehe Team-Vault), Feinschliff/Druck/Veröffentlichung heute im Team.
- **Nächster Schritt:** 1-Minuten-Pitch-Skript für den 10./11.09. schreiben, Standmaterial fertigstellen, Produktname final entscheiden ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)).

## Was noch fehlt

- [ ] **Prototyp komplett auf Englisch umstellen** (UI-Templates, `app.py`-Strings, Supabase-Inhalte wie Kategorien/Posts/Autoren) – Team-Entscheidung vom 09.09.2026 per Chat, da das Publikum vor Ort ausschließlich englischsprachig ist. Wird schrittweise von der Nacht-Automation umgesetzt, aktueller Stand/Migrations-Ansatz in [`Code/feed-diversity-prototype/NIGHTLY_TASK.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/NIGHTLY_TASK.md).
- [ ] **Board-Zugriffsproblem der Nacht-Automation beheben** ([#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100)) — seit 04.09. wiederholt aufgetreten, tritt weiterhin auf
- [ ] Morgens klären, ob "Final presentation"-Input heute noch aussteht oder bereits Dienstag erledigt war (siehe Warnkasten)
- [ ] Name + E-Mail ins Website-Google-Sheet eintragen (Link nur auf dem Board)
- [ ] Poster/Flyer aus dem Entwurf oben tatsächlich gestalten und in ausreichender Menge drucken
- [ ] Blogpost-Entwurf oben prüfen (insb. Team-Zusammensetzung/Anton, s. Warnkasten) und auf designentrepreneurshipworkshop.org veröffentlichen
- [ ] Team-13-Karte auf dem Gruppenboard mit dem Stand oben aktualisieren (heute Nacht nicht möglich)
- [ ] Rollen (Scrum Master/Product Owner) im Team festlegen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- [ ] Retrospektive durchführen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))
- [ ] Supabase-Token widerrufen ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92))
- [ ] Donnerstag (03.09.) rückwirkend dokumentieren ([#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97))
- [ ] Übrige offene Punkte siehe [Kanban-Board](https://47felix.github.io/RasberryPI-Team-13/DTEW-Workshop/kanban-board/) bzw. [Issues #92–#102](https://github.com/47Felix/RasberryPI-Team-13/issues?q=is%3Aissue+92..102+in%3Anumber)

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[DTEW 0809 - Weiterarbeit am Prototyp und Final-Presentation-Input]]
- [[DTEW - Strategie-Praesentation]]
- [[Team 13 - Digitale Demokratie]]
- [`DTEW-Workshop/strategy-presentation/`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/strategy-presentation/strategy-presentation.md)
- [`Code/feed-diversity-prototype/README.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/README.md)
- [[TaskCards Board]]
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
