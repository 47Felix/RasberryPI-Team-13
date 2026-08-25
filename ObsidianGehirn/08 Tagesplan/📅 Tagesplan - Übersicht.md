---
tags: [tagesplan, workflow]
---

# 📅 Tagesplan – Übersicht

Neuer Bereich (seit 25.08.2026): Wenn jemand morgens einen neuen Tag am Projekt startet (neuer Chat, "guten Morgen", "lass uns starten" o.ä.), soll Claude einen kurzen **Tagesplan** erstellen – eine kompakte Standortbestimmung: Was liegt an, was ist Priorität heute, was hat sich seit gestern geändert.

> [!important] Für Claude: Wann triggern?
> - Der/die Nutzer:in signalisiert den Start eines neuen Arbeitstags am Projekt (z.B. "Guten Morgen", "lass uns heute weitermachen", "was steht heute an", explizite Bitte um Tagesplan).
> - Reine Rückfragen zum Projekt sind **kein** automatischer Trigger – nur bei erkennbarem "neuer Tag beginnt"-Signal von selbst einen Tagesplan vorschlagen/erstellen.

## Ablauf für Claude

1. **Kontext einsammeln**, bevor der Plan geschrieben wird:
   - [[Offene Punkte]] – was ist noch offen
   - [[Technischer Fahrplan]] – wo stehen wir im Gesamtablauf
   - [[🧠 Brain Dump - Übersicht]] (persönliche Dumps) – gibt es neue Einträge seit dem letzten Tagesplan, die noch nicht eingearbeitet sind
   - ggf. aktueller Stand auf dem Pi (Node-RED, Services), falls über `claude-in-chrome`/ttyd erreichbar
2. **Neue Notiz anlegen** unter `08 Tagesplan/Tage/YYYY-MM-DD.md` (Datum des Tages), auf Basis von [[Vorlage - Tagesplan]].
3. **In dieser Notiz verlinken** – nicht duplizieren: Details bleiben in [[Offene Punkte]] / [[Technischer Fahrplan]], der Tagesplan verweist nur darauf und setzt die Priorität für den Tag.
4. **Committen & pushen** nach der Branch-Strategie ([[Branch-Strategie]], [[Git Workflow]]): Branch `gehirn/tagesplan-yyyy-mm-dd`, Commit signiert unter `Agrimm123` oder `47Felix` (nie "Claude"), dann Branch pushen. Bei täglichen Routine-Einträgen reicht danach auch ein lokaler `git merge --no-ff` auf `main` statt eines vollen PRs, wenn Anton/Felix das so wollen – im Zweifel PR auf GitHub anlegen.
5. **Am Ende des Tages (optional)**, falls gewünscht: kurze Ergebnis-Notiz im selben Tageseintrag ergänzen ("Was ist heute liegengeblieben?" → wandert ggf. in [[Offene Punkte]]).

## Wo landen die täglichen Einträge?
Im Unterordner `08 Tagesplan/Tage/`, eine Datei pro Tag (`YYYY-MM-DD.md`). Alte Tagespläne bleiben stehen (Verlauf) – kein Aufräumen nötig, ähnlich wie beim [[🧠 Brain Dump - Übersicht|Brain Dump]].

## Verwandte Notizen
- [[Vorlage - Tagesplan]] – Vorlage für neue Tageseinträge
- [[Offene Punkte]]
- [[Technischer Fahrplan]]
- [[🧠 Brain Dump - Übersicht]]
- [[Branch-Strategie]], [[Git Workflow]]

#tagesplan #workflow
