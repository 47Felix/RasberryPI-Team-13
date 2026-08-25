---
tags: [projekt, git, workflow]
---

# Branch-Strategie

> [!important] Verbindliche Regel (seit 24.08.2026)
> **`main` bleibt immer stabil.** Änderungen laufen über kurzlebige Branches mit einheitlichem Namensschema, nicht direkt auf `main` (Ausnahme: winzige Tippfehler-Fixes in einer bestehenden Notiz).

> [!important] Verbindliche Regel (seit 25.08.2026): Merge in `main` nur manuell durch Anton/Felix
> **Claude darf auf Nebenbranches alles machen** – branchen, committen, pushen, Branches auch mehrfach überschreiben/force-pushen. Das **Mergen eines Branches nach `main` ist aber ausschließlich Anton/Felix vorbehalten** und wird stets manuell gemacht (per Pull-Request-Merge-Button auf GitHub oder manuell lokal). Claude merged **niemals** selbst nach `main` – auch nicht bei kleinen/"trivialen" Änderungen, auch nicht per `git merge --no-ff` lokal, auch nicht wenn explizit nach einem schnellen Merge gefragt wird, ohne dass Anton/Felix das aktiv bestätigt haben. Push auf `main` (egal ob direkt oder als Ergebnis eines Merges) macht Claude nicht.

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

# 4. Claude erstellt hier höchstens den Pull Request (z.B. via `gh pr create`)
#    und meldet: "Branch gehirn/thema-hier ist gepusht/PR ist offen, bitte mergen."
#    Das eigentliche Mergen nach main macht danach Anton/Felix manuell auf GitHub.

# 5. Erst NACHDEM Anton/Felix gemerged haben, lokal aufräumen:
git checkout main
git pull
git branch -d gehirn/thema-hier
git push origin --delete gehirn/thema-hier
```

> [!note] Merge-Weg
> Mergen ausschließlich über einen **Pull Request auf GitHub** (Web-UI), den Anton oder Felix selbst mit dem Merge-Button bestätigen. So bleibt für sie sichtbar, was reinkommt, auch ohne die Sandbox-Historie von Claude zu sehen. Es gibt **keine Ausnahme mehr** für kleine/unkritische Änderungen – auch die landen erst nach manueller Freigabe auf `main`.

## Für Claude: wann direkt auf main, wann Branch?
- **Nie direkt auf `main` committen oder pushen** – auch nicht bei Tippfehlern oder kaputten Links. Selbst triviale Korrekturen laufen über einen `fix/`-Branch + PR.
- **Immer Branch:** neue Notizen, inhaltliche Änderungen am Vault, jeglicher Code (Node-RED-Exports, Skripte), Änderungen an mehreren Dateien gleichzeitig.
- **Auf Branches darf Claude frei arbeiten:** committen, pushen, Branch überschreiben/force-pushen, mehrere Commits – alles erlaubt, solange es nicht `main` betrifft.
- **Merge nach `main` macht Claude nie selbst** – weder lokal (`git merge`, `git checkout main && git merge ...`) noch über GitHub (z.B. `gh pr merge`). Claude öffnet höchstens den PR und weist darauf hin, dass er noch gemerged werden muss.
- Branch-Namen wie oben wählen – passt die Änderung zu keinem der vier Typen, lieber kurz nachdenken statt einen fünften Typ zu erfinden (Konsistenz > Vollständigkeit).

## Verwandte Notizen
- [[Git Workflow]] – Regeln zu Commit-Signierung
- [[Offene Punkte]]

#projekt #git #workflow #branches
