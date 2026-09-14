---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0911 (Freitag, Woche 2) – Offene Punkte vor dem freien Samstag

Vorbereitung für Freitag, 11.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Case bleibt **Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung**, Arbeitstitel weiterhin "Perspective Compass" (Name/Logo-Entscheidung weiterhin offen, [#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)/[#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96)). Wie an den Vortagen: Alles mit 📝 markiert **muss vor Ort/live im Team passieren**. Diese Notiz wurde nachts von der Automation erstellt, **ohne** Zugriff auf das echte Board (siehe Warnkasten) – bitte morgens früh gegenprüfen.

> [!danger] Board-Zugriff erneut geprüft und erneut gescheitert – jetzt 4. Nacht in Folge, kein Beleg dass `board-sync.sh` läuft
> Live getestet (`curl` gegen `itech-bs14.taskcards.app` direkt aus dieser Cloud-Sandbox, Nacht 10.→11.09.): weiterhin `403 Forbidden` / `connect_rejected` auf den CONNECT-Tunnel, identisch zum seit 03.09. dokumentierten Befund (siehe [[TaskCards Board]]). Weder Haupt-/Teams-Board noch das Team-13-Gruppenboard konnten gelesen oder bearbeitet werden.
> **Zur offenen Frage aus der letzten Notiz:** Ich habe die Git-Historie seit dem 07.09. (Issue [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100), "Board-Zugriff repariert durch VM-Cronjob `board-sync.sh`") durchsucht – es gibt **keinen einzigen Commit**, der nach einem VM-Board-Sync aussieht (das letzte `Board-Sync`-Commit ist vom 07.09., manuell von 47Felix). Issue #100 selbst ist trotz Label `kanban:done` noch als **offen** markiert. Das spricht eher für die zweite Hypothese aus der 0910-Notiz: `board-sync.sh` läuft entweder gar nicht oder committet seine Ergebnisse nicht ins Repo – **bitte auf der VM direkt prüfen** (Cronjob-Log, letzte Ausführung), nicht nur auf das "repariert"-Label in #100 verlassen.
> - Aufgabenliste unten stammt deshalb wie an den Vortagen **nur aus der Übersicht** (Stand Board 01.09.), nicht aus einer tagesaktuellen Freitags-Karte.
> - Team-13-Karte auf dem Gruppenboard konnte weder gelesen noch aktualisiert werden.

> [!warning] Wichtige Terminunklarheit – bitte morgens als Erstes klären
> Die Übersicht (Stand Board 01.09.) fasst **Donnerstag 10.09. und Freitag 11.09. in einer einzigen Zeile** zusammen: T-Shirt tragen, finalen Blogpost bis 12:00 hochladen, Marktstände aufbauen, 12:00 Pitches in Raum 23, Innovation Fair, Gruppenfoto, Abschlusssession + Feedback, Farewell Party. Die gestrige Notiz ([[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]]) ist davon ausgegangen, dass **alles davon bereits gestern (10.09.) stattfindet**. Aus der Übersicht allein lässt sich aber **nicht sicher sagen**, ob:
> - (a) der komplette Block bereits gestern gelaufen ist (dann ist heute vor allem Auslaufen/Aufräumen), oder
> - (b) Teile davon – insbesondere Pitch, Innovation Fair, Abschlusssession, Farewell Party – tatsächlich erst **heute (Freitag)** stattfinden, während gestern nur T-Shirt/Blogpost/Standaufbau dran waren.
> **Bitte morgens als Erstes gegenchecken, was von der gestrigen Vorbereitung schon gelaufen ist.** Falls Pitch/Innovation Fair/Farewell Party noch aussteht: das komplette vorbereitete Material (Pitch-Skript, Blogpost-Entwurf, Prozess-Zeitstrahl, Team-Karten-Text) steht unten in [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] weiterhin unverändert bereit und muss nicht neu geschrieben werden – nur Datum/Bezug ("heute" → Freitag) beim Vortragen anpassen.

## Aufgaben von morgen (laut Übersicht, Stand Board 01.09. – s. Warnkasten zur Terminunklarheit)
Dieselbe Zeile wie für Donnerstag (Übersicht behandelt beide Tage gemeinsam):
- Workshop-T-Shirt tragen
- Finalen Blogpost bis 12:00 Uhr hochladen (falls nicht schon gestern erledigt)
- Marktstände: Prototypen zeigen, Prozess dokumentieren
- 12:00 Uhr: Pitches in Raum 23 (max. 1 Minute, keine Slides) – falls nicht schon gestern gehalten
- Innovation Fair / Marktplatz
- Gruppenfoto
- Abschlusssession + Feedback
- Farewell Party (Budget/Buffet im Team klären)

Danach laut Übersicht nur noch **Samstag 12.09.: freier Tag** (optionale Bremen-Exkursion) – d.h. **Freitag ist voraussichtlich der letzte volle Workshop-Arbeitstag.**

## 📝 Nur vor Ort/live möglich
- **Daily** – ehrliche Antworten, Gerüst unten als Vorschlag
- **Terminunklarheit oben klären** – was von gestern ist schon erledigt, was steht heute noch an
- **Echtes Board morgens früh prüfen** – inkl. `board-sync.sh`-Log auf der VM (siehe Warnkasten)
- Falls Pitch/Blogpost/Innovation Fair heute erst stattfinden: Material aus [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] nutzen, Pitch laut üben mit Stoppuhr, Vortragende(n) festlegen (Rollenfrage [#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- **Letzte Chance vor dem freien Samstag, die unten gelistete offene-Punkte-Liste abzuarbeiten** – siehe "Was noch fehlt"
- **Team-13-Karte auf dem Gruppenboard aktualisieren** – heute Nacht nicht möglich, Text in [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] weiterhin zum Reinkopieren vorbereitet (bei Bedarf "Stand Donnerstag" → "Stand Freitag" anpassen)
- **Farewell-Party-Budget/Buffet** – reine Team-/Organisationsentscheidung
- **Live-Demo-URL am Stand bereithalten** (aktuelle VM-IP vor Ort erfragen, siehe [[Feed-Diversity-Prototyp - Deployment]])

## ✅ Vorbereitet: Letzte-Chance-Checkliste vor dem freien Samstag

Da Freitag voraussichtlich der letzte volle Arbeitstag ist, hier die noch offenen Punkte aus den Vortagen gebündelt (alle laut GitHub-Issues #92–#102 Stand heute Nacht noch **offen**), damit das Team sie gezielt vor der Farewell Party abhaken kann:

| Priorität | Punkt | Issue | Warum heute |
|---|---|---|---|
| Hoch | Produktname final entscheiden | [#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93) | Steht noch als Platzhalter im Pitch-Skript und Blogpost-Entwurf – danach nicht mehr korrigierbar |
| Hoch | Rollen (Scrum Master/Product Owner) festlegen | [#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99) | Wird auch für "wer pitcht" gebraucht |
| Mittel | Logo visuell gestalten | [#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96) | Entwurf von dnbk72 (08.09.) existiert bereits, siehe [[DTEW - Strategie-Praesentation]] – nur noch finalisieren |
| Mittel | Retrospektive nachholen (Sprint-Ende 07.09.) | [#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98) | Letzte Gelegenheit vor Workshop-Ende |
| Mittel | Donnerstag 03.09. rückwirkend dokumentieren | [#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97) | Lücke in der Doku-Kette, sonst dauerhaft offen |
| Sicherheit | Supabase-Token widerrufen | [#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92) | Sicherheitsvorfall vom 04.09. seit über einer Woche unbehoben |
| Info | Board-Zugriff der Nacht-Automation (#100) trotz "repariert"-Label noch offen | [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100) | Sollte geschlossen oder korrigiert werden, siehe Warnkasten oben |

> [!tip] Für die Live-Nutzung
> Diese Tabelle ersetzt keine Diskussion – sie ist nur eine sortierte Erinnerung, was seit Tagen liegen geblieben ist. Reihenfolge (Name → Rollen → Logo → Retro → Doku-Lücke → Security) ist ein Vorschlag, kein Zwang.

## ✅ Vorbereitet: Daily-Gerüst

- **Gestern (10.09.):** laut Plan finaler Blogpost, Pitch, Marktstand, Innovation Fair (siehe Terminunklarheit oben – bitte morgens bestätigen, was tatsächlich stattfand).
- **Heute (11.09.):** je nach Klärung entweder Restarbeiten vom Donnerstags-Block (Pitch/Blogpost/Fair/Farewell Party) oder – falls das schon gestern lief – Fokus auf die offenen Punkte (Name, Rollen, Logo, Retro, Doku-Lücke, Security) vor dem freien Samstag.
- **Blocker:** *(vor Ort ausfüllen — Board-Zugriffsproblem der Nacht-Automation weiterhin ungelöst, siehe Warnkasten; alle Punkte aus der Checkliste oben, die noch offen sind)*

## Was noch fehlt

- [ ] **Terminunklarheit klären** – ist der Donnerstag/Freitag-Block aus der Übersicht schon komplett gelaufen, oder steht heute noch Pitch/Fair/Farewell Party an?
- [ ] `board-sync.sh` auf der VM tatsächlich prüfen (Log, letzte Ausführung) statt sich auf Issue [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100) zu verlassen – Issue danach korrekt schließen oder korrigieren
- [ ] Produktname final entscheiden ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)), Logo finalisieren ([#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96))
- [ ] Rollen (Scrum Master/Product Owner) festlegen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- [ ] Retrospektive durchführen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))
- [ ] Supabase-Token widerrufen ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92))
- [ ] Donnerstag (03.09.) rückwirkend dokumentieren ([#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97))
- [ ] Team-13-Karte auf dem Gruppenboard aktualisieren (heute Nacht nicht möglich)
- [ ] Falls noch nicht geschehen: Pitch üben, Blogpost veröffentlichen, Marktstand aufbauen (siehe [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] für fertiges Material)
- [ ] Übrige offene Punkte siehe [Kanban-Board](https://47felix.github.io/RasberryPI-Team-13/DTEW-Workshop/kanban-board/) bzw. [Issues #92–#102](https://github.com/47Felix/RasberryPI-Team-13/issues?q=is%3Aissue+92..102+in%3Anumber)

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] – enthält das noch gültige Pitch-Skript, Blogpost-Entwurf, Prozess-Zeitstrahl und Team-Karten-Text
- [[DTEW - Strategie-Praesentation]]
- [[Team 13 - Digitale Demokratie]]
- [`Code/feed-diversity-prototype/README.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/README.md)
- [[Feed-Diversity-Prototyp - Deployment]]
- [[TaskCards Board]]
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
