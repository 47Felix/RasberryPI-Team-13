---
tags: [projekt, discord, claude-code, infrastruktur]
---

# Claude Discord Bot Setup

> [!info] Stand
> 26.08.2026 – Grundgerüst gebaut und getestet (Nachrichten werden beantwortet, Test-Branch/Commit über den Bot verifiziert). Server-Design per Discord-API vorbereitet (Referenzdatei + Setup-Schritte), aber noch nicht selbst getestet. Noch nicht alle Teammitglieder registriert, systemd-Dauerbetrieb ggf. noch zu bestätigen (siehe [[Offene Punkte]]).

## Ziel

Eine Azure-VM stellt Claude Code als Discord-Bot bereit, damit das Team über einen privaten Discord-Kanal mit Claude am Projekt-Repo arbeiten kann – **ohne** dass alle Anfragen über die Subscription einer einzelnen Person laufen. Jedes Teammitglied nutzt sein **eigenes** Anthropic-Konto (Pro/Max), der Bot routet nur die Nachrichten.

## Architektur

```
Discord-User A ──┐
Discord-User B ──┼─→ Discord-Bot (Python, discord.py) ──→ Routing nach Discord-User-ID
Discord-User C ──┘
                        │
        ┌───────────────┼───────────────┐
   claude (User A)  claude (User B)  claude (User C)
   CLAUDE_CONFIG_DIR= CLAUDE_CONFIG_DIR= CLAUDE_CONFIG_DIR=
   ~/sessions/userA/  ~/sessions/userB/  ~/sessions/userC/
```

Alle Prozesse arbeiten auf demselben geklonten Repo (`~/RasberryPI-Team-13` auf der VM), sehen also dieselbe Code-/Vault-Basis.

## Infrastruktur

- **VM:** Azure, Ubuntu Server 24.04 LTS (bewusst nicht "Pro" – keine Enterprise-Features nötig), Hostname `ClaudeDiscord`, Linux-User `team13`
- **Software:** Node.js LTS (für die Claude-Code-CLI), Python 3.11+, Git
- **Repo-Zugriff:** per HTTPS-Clone mit Fine-Grained-Token (Token liegt **nicht** hier im Vault, sondern nur in den Claude-Projekt-Anweisungen)
- **Bot-Ordner auf der VM:** `~/discord-claude-bot/` mit `bot.py`, `requirements.txt`, `.env` (Bot-Token, Channel-ID, Guild-ID, Repo-Pfad – nie committen), `users.json` (Mapping Discord-User-ID → Config-Verzeichnis + Session-ID)

## Pro-Nutzer-Login (Kernprinzip)

Jedes Teammitglied bekommt ein eigenes Unterverzeichnis unter `~/sessions/<name>/` und macht dort **einmalig selbst** (per SSH, mit eigenem Anthropic-Account):

```bash
mkdir -p ~/sessions/<name>
CLAUDE_CONFIG_DIR=~/sessions/<name> claude login
```

Wichtig: `claude login` ist ein interaktiver Browser-OAuth-Flow – kann nicht automatisiert/für andere übernommen werden. Jede Person muss das selbst machen.

Danach im Discord-Kanal einmalig:

```
!register <name>
```

`<name>` muss exakt dem Ordnernamen unter `~/sessions/` entsprechen. Der Bot merkt sich danach pro Discord-User-ID eine `session_id`, damit der Gesprächsverlauf über mehrere Nachrichten erhalten bleibt (`claude --resume <session-id>`).

## Discord-Setup

- Bot-Application im Discord Developer Portal angelegt, **MESSAGE CONTENT INTENT** aktiviert (sonst sieht der Bot keine normalen Nachrichten, nur Metadaten)
- Bot reagiert nur im konfigurierten `ALLOWED_CHANNEL_ID`-Kanal **und** in dessen Threads (Threads haben eine eigene Channel-ID, deshalb zusätzlich Check auf `parent_id`)
- Befehle: `!myid` (eigene Discord-ID anzeigen, fürs Debugging), `!register <name>` (Config-Verzeichnis verknüpfen)
- Bot-Account hat **Administrator-Rechte** auf dem Server

## Permissions

Läuft aktuell mit `--dangerously-skip-permissions`, weil es über Discord keine Möglichkeit gibt, eine interaktive Freigabe-Rückfrage zu beantworten. Heißt: Claude führt Aktionen (Dateiänderungen, Git-Befehle, Shell-Kommandos, Discord-API-Aufrufe) im Namen der jeweiligen Person **sofort ohne Rückfrage** aus.

> [!warning] Bewusster Trade-off
> Für ein privates Team-Repo vertretbar, aber es bedeutet: ein unbedachter Prompt im Discord-Thread kann direkt Dateien ändern, Branches erzeugen, Rollen/Kanäle anlegen o.ä. Alternative für mehr Kontrolle wäre eine feinere Tool-Allowlist statt komplettem Skip – siehe [[Offene Punkte]].

## Server-Design per Discord-API

Admin-Rechte des Bot-Accounts allein reichen nicht, damit Claude den Server gestaltet – dafür muss Claude aktiv die Discord-REST-API mit dem Bot-Token aufrufen (per `curl` auf der VM, da Claude Code ohnehin Shell-Zugriff hat).

**Setup:**
1. Server-ID (Guild-ID) über Rechtsklick auf den Servernamen → "Server-ID kopieren" ermitteln
2. In `~/discord-claude-bot/.env` eintragen: `GUILD_ID=<server-id>`
3. Referenzdatei `DISCORD_API.md` im Repo-Ordner (`~/RasberryPI-Team-13/`) ablegen – enthält fertige `curl`-Snippets für Rollen anlegen, Kategorien/Kanäle anlegen, Kanal-Berechtigungen pro Rolle setzen, inkl. Hinweis, immer erst per GET den bestehenden Zustand zu prüfen (Duplikate vermeiden)

**Nutzung:** Im Discord-Thread z.B. "Lies dir `DISCORD_API.md` durch und erstelle die Rollen X, Y, Z sowie die Kategorie ... mit den Kanälen ...". Claude liest die Referenz, prüft den Ist-Zustand per GET, legt Rollen/Kategorien/Kanäle per `curl`-POST an.

> [!warning] Rollen-Hierarchie beachten
> Die Bot-Rolle muss in der Rollen-Reihenfolge **über** allen Rollen stehen, die sie verwalten soll – sonst verweigert Discord die API-Aufrufe.

## Dauerbetrieb (systemd)

Damit der Bot nicht bei jedem `Strg+C` oder Terminal-Schließen stirbt, läuft er idealerweise als systemd-Service (`discord-claude-bot.service`, `Restart=on-failure`, startet automatisch bei VM-Boot). Setup-Anleitung liegt lokal beim Bot-Code; Status auf der VM prüfen mit `systemctl status discord-claude-bot`.

## Gelernte Stolperfallen (für neue Teammitglieder)

- `claude login` **nicht** innerhalb einer bereits laufenden interaktiven `claude`-Chat-Sitzung als Nachricht eintippen – das schickt nur Text an Claude, statt den Login auszulösen. Entweder in einer normalen Shell ausführen, oder innerhalb einer Claude-Code-Sitzung mit vorangestelltem `!` als echten Shell-Befehl (`! claude login`).
- Der `CLAUDE_CONFIG_DIR`-Ordnername ist frei wählbar – muss **nicht** mit dem Discord-Usernamen oder Chatnamen übereinstimmen, nur exakt mit dem Argument bei `!register` matchen.
- Discord-Threads haben eigene Channel-IDs, unabhängig vom übergeordneten Kanal – ohne den `parent_id`-Check reagiert der Bot dort nicht.
- Der Bot-Prozess stirbt bei `Strg+C` oder geschlossenem Terminal → für Dauerbetrieb systemd nutzen.

## Offene Punkte
Siehe [[Offene Punkte]] – u.a. weitere Teammitglieder registrieren, Discord-Bot-Token rotieren, Entscheidung Session-pro-Thread vs. Session-pro-User, Server-Design-Feature erstmals testen.

## Verwandte Notizen
- [[Pi Zugriff]]
- [[Git Workflow]]
- [[⚠️ Zugangsdaten - Hinweis]]

#projekt #discord #claude-code #infrastruktur
