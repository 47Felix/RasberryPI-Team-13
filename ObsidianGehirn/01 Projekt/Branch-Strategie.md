---
tags: [projekt, git, workflow]
---

# Branch-Strategie

> [!important] Verbindliche Regel (seit 24.08.2026)
> **`main` bleibt immer stabil.** Änderungen laufen über kurzlebige Branches mit einheitlichem Namensschema, nicht direkt auf `main` (Ausnahme: winzige Tippfehler-Fixes in einer bestehenden Notiz).

## Warum überhaupt Branches, bei nur 2 Leuten + Claude?
- **Saubere Historie:** Man sieht auf einen Blick, ob ein Commit eine Wissens-Änderung (Vault) oder eine Code-Änderung (Pi/Node-RED/Skripte) war – ohne jeden Commit einzeln lesen zu müssen.
- **main bleibt immer funktionsfähig:** Falls mal ein Node-RED-Export kaputt ist oder eine Notiz halbfertig, landet das nicht sofort auf `main`.
- **Parallel arbeiten möglich:** Anton, Felix und Claude (in verschiedenen Chats/Sessions) können gleichzeitig an unterschiedlichen Themen arbeiten, ohne sich gegenseitig Commits zu überschreiben.
- **Aufwand bleibt minimal:** Kein Zwang zu Pull-Request-Reviews o.ä. – für ein Schulprojekt zu zweit wäre das Overkill. Branch → mergen → löschen reicht.

## Namensschema

`<typ>/<kurzbeschreibung-in-kebab-case>`

| Typ | Wofür | Beispiel |
|---|---|---|
| `gehirn/` | Änderungen am Obsidian-Vault (Wissen, Notizen, Doku, To-Dos) | `gehirn/ws-praesentationen` |
| `code/` | Neuer Code (Node-RED-Flow-Exports, Python-/Shell-Skripte, Konfigurationsdateien) | `code/mqtt-integration` |
| `fix/` | Bugfix an bestehendem Code | `fix/node-red-gpio-crash` |
| `pi-setup/` | Änderungen an Pi-Konfiguration, die versioniert werden sollen (z.B. systemd-Unit-Dateien als Referenz) | `pi-setup/ttyd-service-datei` |

> [!tip] Kurzbeschreibung
> Kurz, sprechend, klein geschrieben, Wörter mit `-` getrennt. Kein Datum, keine Namen (steht eh im Commit/Branch selbst) – die Beschreibung soll sagen *was* passiert, nicht *wer* oder *wann*.

## Ablauf (für jede Änderung)

```bash
# 1. Von main branchen
git checkout main
git pull https://<user>:<token>@github.com/47Felix/RasberryPI-Team-13.git main
git checkout -b gehirn/thema-hier

# 2. Änderungen machen, committen (signiert, siehe Git Workflow)
git add -A
git commit -S -m "Kurze, klare Commit-Nachricht"

# 3. Branch pushen
git push -u origin gehirn/thema-hier

# 4. Auf GitHub in main mergen (Pull Request erstellen & mergen)
#    Danach lokal aufräumen:
git checkout main
git pull
git branch -d gehirn/thema-hier
git push origin --delete gehirn/thema-hier
```

> [!note] Merge-Weg
> Mergen am liebsten über einen **Pull Request auf GitHub** (Web-UI) statt lokal – so bleibt für Anton/Felix sichtbar, was reinkommt, auch ohne dass sie die Sandbox-Historie von Claude sehen. Bei ganz kleinen, unkritischen Vault-Änderungen reicht auch ein lokaler `git merge --no-ff` direkt auf `main`.

## Für Claude: wann direkt auf main, wann Branch?
- **Direkt auf `main`:** nur bei trivialen Korrekturen (Tippfehler, kaputter Link) in einer bereits bestehenden Notiz.
- **Immer Branch:** neue Notizen, inhaltliche Änderungen am Vault, jeglicher Code (Node-RED-Exports, Skripte), Änderungen an mehreren Dateien gleichzeitig.
- Branch-Namen wie oben wählen – passt die Änderung zu keinem der vier Typen, lieber kurz nachdenken statt einen fünften Typ zu erfinden (Konsistenz > Vollständigkeit).

## Verwandte Notizen
- [[Git Workflow]] – Regeln zu Commit-Signierung
- [[Offene Punkte]]

#projekt #git #workflow #branches
