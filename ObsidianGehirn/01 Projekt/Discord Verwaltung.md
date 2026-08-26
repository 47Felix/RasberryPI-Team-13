---
tags: [projekt, discord, api]
---

# Discord Verwaltung – Server per API bearbeiten

> [!important] Wenn eine Anfrage kommt, den Discord-Server zu bearbeiten (Rollen, Kanäle, Kategorien, Icon, Berechtigungen)
> Es gibt **keine** Discord-MCP-Integration. Der Weg ist die Discord-REST-API per `curl` mit dem Bot-Token – vollständiges Befehls-Cookbook steht in `DISCORD_API.md` im Repo-Root. Diese Notiz hier ist die Kurzreferenz mit den konkreten Werten für unseren Server.

## Zugangsdaten (nicht hier, siehe [[⚠️ Zugangsdaten - Hinweis]])
- `DISCORD_BOT_TOKEN` und `GUILD_ID` sollen laut `DISCORD_API.md` als Umgebungsvariablen im Prozess gesetzt sein – **war in der Praxis nicht zuverlässig der Fall** (bei einer Session zunächst leer, kurz danach gesetzt). **Immer zuerst prüfen**, nicht blind auf die Doku-Aussage "bereits gesetzt" verlassen:
  ```bash
  [ -z "$DISCORD_BOT_TOKEN" ] && echo "MISSING_TOKEN"
  ```
- Bot heißt **ClaudeVM** (hat die `Team-Lead`-Berechtigung/Administrator-Rolle, `managed: true`).

## ⚠️ Stolperfalle: Env-Vars gelten nur pro Bash-Aufruf
`export GUILD_ID=...` in einem Tool-Call ist im **nächsten** Bash-Aufruf wieder weg (jeder Call = neue Shell, nur das Arbeitsverzeichnis bleibt erhalten). Führt sonst zu `404 Not Found`, weil die URL `.../guilds/` ohne ID aufgerufen wird. Deshalb: `export GUILD_ID=1493313312690147421` **in jedem einzelnen curl-Befehl/Bash-Call neu setzen**, nicht nur einmal am Anfang der Session.

## Bekannte Werte – UnigoonServer
- `GUILD_ID`: `1493313312690147421`

### Rollen (bereits vorhanden, Stand 26.08.2026 – vor dem Anlegen immer erst GET prüfen!)
| Rolle | ID | Rechte |
|---|---|---|
| Team-Lead | `1542105052922126407` | Administrator (`8`) |
| Mitglied | `1542105058110349452` | `0` |
| Gast | `1542105061629493348` | `0` |
| ClaudeVM (Bot, managed) | `1542102453858861118` | Administrator (`8`) |

### Kategorien/Kanäle (bereits vorhanden)
- Kategorie `🧊 ICE TRUCK PROJEKT` (id `1542105073344057346`) enthält bereits:
  - `🔊 Allgemein` (Voice, id `1493313314984562873`)
  - `pi-projekt` (Text, id `1542105092596174878`)
- Kategorie `📖 INFO` (id `1493313314984562870`), Kategorie `🤖 CLAUDE` (id `1542106258788847682`)

> [!tip] Wenn jemand "erstelle Rollen X/Y/Z + Kategorie 'PROJEKT' mit Kanälen A/B" verlangt
> Erst GET auf `/guilds/{id}/roles` und `/guilds/{id}/channels` – bei uns existiert das alles schon (nur die Kategorie heißt `🧊 ICE TRUCK PROJEKT`, nicht wörtlich `PROJEKT`). Nicht blind neu anlegen/duplizieren, sondern mit dem Team abgleichen, ob umbenennen statt neu erstellen gewollt ist.

## Server-Icon
Am 26.08.2026 per Nutzeranfrage geändert (Bild von einer vom Nutzer angegebenen URL, per `curl -L` geladen, base64-kodiert, `PATCH /guilds/{id}` mit `{"icon": "data:image/jpeg;base64,..."}`). Base64-Payload **in eine Datei schreiben und mit `--data @datei` senden**, nicht als Inline-Argument – zu lange Strings sprengen `ARG_MAX` (`Argument list too long`).

## Verwandte Notizen
- [[Claude Discord Bot Setup]] – der Bot (`ClaudeVM`), dessen Token hier für die Server-Verwaltung genutzt wird
- [[⚠️ Zugangsdaten - Hinweis]]
- [[Git Workflow]]

#projekt #discord #api
