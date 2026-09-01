---
tags: [projekt, discord, claude-code, infrastruktur]
---

# Claude Discord Bot Setup

> [!info] Stand
> 28.08.2026 – Grundgerüst gebaut und getestet (Nachrichten werden beantwortet, Test-Branch/Commit über den Bot verifiziert). Server-Design per Discord-API getestet (siehe [[Discord Verwaltung]]). Direkter VM-Zugriff für Claude per SSH geprüft und verworfen (Netzwerk-Sandbox lässt kein SSH zu) – bleibt beim Copy-Paste-Workflow. Täglicher Vault-Sync-Cronjob läuft (siehe Abschnitt unten), inkl. Fix für einen 2-tägigen stillen Ausfall durch abgelaufene OAuth-Credentials und neuem ERR-Trap für Fehler-Alarme (siehe Incident unten). Jede Session (User + Vault-Sync) arbeitet in einer eigenen Git-Worktree statt einem geteilten Verzeichnis (siehe "Git-Worktree-Isolation" unten – behebt eine live aufgetretene Race Condition). Noch nicht alle Teammitglieder registriert, siehe [[Offene Punkte]].

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
   cwd: eigene Git-Worktree je Session, siehe "Git-Worktree-Isolation" unten
```

Alle Worktrees teilen sich dieselbe Git-Objekt-Datenbank/Historie (ein Clone als Basis unter `~/RasberryPI-Team-13`), haben aber **unabhängige Arbeitsverzeichnisse und je eigenes HEAD** – siehe unten, warum das wichtig ist.

## Git-Worktree-Isolation (seit 26.08.2026, Incident-Fix)

> [!warning] Was passiert war
> Ursprünglich liefen ALLE Sessions (jeder registrierte User + der Vault-Sync-Cronjob) im selben geklonten Repo-Verzeichnis `~/RasberryPI-Team-13`. Am 26.08.2026 live beobachtet: Eine Session hat mitten in der Arbeit einer anderen den Branch weggeschaltet (`git checkout` einer Session überschreibt den Checkout aller anderen, die dasselbe Verzeichnis nutzen), und uncommittete Dateien einer Session (u.a. ein Arduino-Sketch-Entwurf, der Tresor-Pin-Plan) tauchten in einer anderen Session als "fremde" untracked Files auf und wären beinahe versehentlich in einen automatischen Commit gerutscht.

**Fix:** Jede Session bekommt jetzt eine eigene `git worktree` unter `~/repos/worktrees/<name>/` (Name = registrierter Bot-Username bzw. `vault-sync`):
- `bot.py` legt bei `!register <name>` automatisch eine Worktree an (`ensure_worktree()`), per `git worktree add --detach <pfad> origin/main` ausgehend vom Haupt-Clone `~/RasberryPI-Team-13`.
- `vault-sync.sh` nutzt dauerhaft die Worktree `~/repos/worktrees/vault-sync/`.
- Alle Worktrees arbeiten mit **detached HEAD auf `origin/main`**, nicht mit dem lokalen `main`-Branch – Git verbietet es, denselben Branch in zwei Worktrees gleichzeitig auszuchecken ("already used by worktree"), und der Haupt-Clone hält `main` bereits dauerhaft.
- `~/RasberryPI-Team-13` selbst bleibt als reine Referenz auf `main` stehen und wird von keiner Session mehr für Arbeit genutzt.
- `bot.py`, `vault-sync.sh` und `requirements.txt` sind jetzt im Repo versioniert (`Code/discord-bot/`) statt nur live auf der VM zu liegen – Änderungen daran laufen ab jetzt über normalen Branch+PR.

> [!note] Bekannte Einschränkung
> Der Bot-Prozess läuft selbst *innerhalb* einer dieser Worktrees (cwd wird beim `claude -p`-Aufruf gesetzt) – ein `systemctl restart discord-claude-bot` killt dadurch ggf. auch gerade laufende `claude -p`-Subprozesse (passiert, wenn systemd `KillMode=control-group` nutzt). Sessions überleben das i.d.R. über `--resume <session-id>`, aber mitten in einem Tool-Aufruf kann das zu einem harten Abbruch führen. Vor einem Neustart also idealerweise keine Session mitten in einer laufenden Aktion haben.

## Infrastruktur

- **VM:** Azure, Ubuntu Server 24.04 LTS (bewusst nicht "Pro" – keine Enterprise-Features nötig), Hostname `ClaudeDiscord`, Linux-User `team13`
- **Software:** Node.js LTS (für die Claude-Code-CLI), Python 3.11+, Git
- **Repo-Zugriff:** per HTTPS-Clone mit Fine-Grained-Token (Token liegt **nicht** hier im Vault, sondern nur in den Claude-Projekt-Anweisungen)
- **Bot-Ordner auf der VM:** `~/discord-claude-bot/` mit `bot.py`, `requirements.txt`, `.env` (Bot-Token, Channel-ID, Guild-ID, Repo-Pfad – nie committen), `users.json` (Mapping Discord-User-ID → Config-Verzeichnis + Worktree-Pfad + Session-ID)
- **Repo-Worktrees:** `~/RasberryPI-Team-13` (Haupt-Clone, bleibt auf `main`, wird für keine Session mehr direkt genutzt) + `~/repos/worktrees/<name>/` je Session (siehe "Git-Worktree-Isolation" unten)

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

- **Leere Fehlermeldung im Discord-Kanal (Fix 31.08.2026, PR [#59](https://github.com/47Felix/RasberryPI-Team-13/pull/59)):** Die Claude-Code-CLI schreibt Fehler bei `--output-format json` oft als JSON auf **stdout** statt auf stderr (z. B. abgelaufene OAuth-Session, ungültige `--resume`-Session-ID, kaputter Worktree). Der Bot zeigte bei leerem stderr bisher nur "Fehler von Claude:" mit leerem Codeblock – `run_claude()` in `bot.py` fällt jetzt auf stdout zurück, wenn stderr leer ist.
- `claude login` **nicht** innerhalb einer bereits laufenden interaktiven `claude`-Chat-Sitzung als Nachricht eintippen – das schickt nur Text an Claude, statt den Login auszulösen. Entweder in einer normalen Shell ausführen, oder innerhalb einer Claude-Code-Sitzung mit vorangestelltem `!` als echten Shell-Befehl (`! claude login`).
- Der `CLAUDE_CONFIG_DIR`-Ordnername ist frei wählbar – muss **nicht** mit dem Discord-Usernamen oder Chatnamen übereinstimmen, nur exakt mit dem Argument bei `!register` matchen.
- Discord-Threads haben eigene Channel-IDs, unabhängig vom übergeordneten Kanal – ohne den `parent_id`-Check reagiert der Bot dort nicht.
- Der Bot-Prozess stirbt bei `Strg+C` oder geschlossenem Terminal → für Dauerbetrieb systemd nutzen.

## Direkter VM-Zugriff für Claude (Cowork-Session) – geprüft, verworfen

Versucht: Die Cowork-Session (diese Chat-Umgebung, getrennt von der Discord-Bot-VM) sollte sich direkt per SSH auf die Azure-VM verbinden können, um nicht mehr auf Copy-Paste zwischen Chat und Terminal angewiesen zu sein.

**Ergebnis: nicht möglich.** Sowohl die Cloud-Sandbox der Session als auch die Geräte-Bridge zum verbundenen Mac laufen mit einem restriktiven Netzwerk-Allowlist (nur bestimmte Web-Domains erlaubt), das rohes SSH (Port 22) zu beliebigen Servern grundsätzlich blockiert – unabhängig von der Azure-Firewall/NSG-Konfiguration.

Alternative geprüft: Web-Terminal (`ttyd` + `Caddy` + kostenlose nip.io-Domain für automatisches HTTPS-Zertifikat) auf der VM einrichten, das im Browser erreichbar wäre. **Bewusst nicht umgesetzt** – Team-Entscheidung (26.08.2026): Der Aufwand (öffentlich erreichbares Terminal mit Passwortschutz + Absicherung) lohnt sich für die Häufigkeit der VM-Zugriffe nicht. Es bleibt beim bestehenden Workflow: Befehle werden im Chat vorgeschlagen, ein Teammitglied führt sie per SSH auf der VM aus und gibt die Ausgabe zurück.

## Täglicher Vault-Sync (Cronjob, seit 26.08.2026)

Zusätzlich zum interaktiven Bot läuft auf derselben VM ein **täglicher Cronjob**, der das Vault automatisch aktuell hält, ohne dass jemand explizit danach fragen muss.

- **Skript:** `~/discord-claude-bot/vault-sync.sh`, versioniert im Repo unter [`Code/discord-bot/vault-sync.sh`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/discord-bot/vault-sync.sh) (Kopie – Änderungen am Skript selbst also künftig per normalem Branch+PR wie jeder andere Code, **nicht** nur live auf der VM patchen, sonst laufen VM und Repo auseinander).
- **Cron:** täglich `00:00 UTC` (= 02:00 Sommerzeit/CEST) – `crontab -l` auf der VM zeigt den aktiven Eintrag. War ursprünglich abends (19:30 UTC), dann morgens (04:45 UTC), auf Felix' Wunsch am 01.09.2026 auf nachts 2 Uhr Ortszeit umgestellt.
  > [!warning] CRON_TZ funktioniert NICHT auf dieser VM
  > Erster Versuch war `CRON_TZ=Europe/Berlin` + `45 6 * * *`, damit sich die Zeit automatisch an Sommer-/Winterzeit anpasst. Per Test am 27.08.2026 verifiziert: dieser Cron (`cron 3.0pl1-184ubuntu2`, Ubuntu) **ignoriert `CRON_TZ` und nimmt immer die Systemzeit** (VM läuft in UTC, siehe `timedatectl`). Deshalb fest `0 0 * * *` (UTC) ohne `CRON_TZ`.
  > **Konsequenz:** Wenn Deutschland auf Winterzeit (CET, UTC+1) wechselt (letzter Sonntag im Oktober), muss die Crontab manuell von `0 0` auf `0 1` geändert werden, sonst läuft der Sync ab dann um 01:00 statt 02:00 Uhr Ortszeit – siehe [[Offene Punkte]].
- **Account/Config-Dir:** eigener, von den User-Sessions getrennter Ordner `~/sessions/vault-sync/` (Credentials von `amogus_911` übernommen, mit dessen Zustimmung – kein separates `claude login` nötig). **Seit 28.08.2026:** Das Skript kopiert die Credentials vor **jedem** Lauf frisch von der aktiven `amogus_911`-Session, statt sich auf eine einmalige statische Kopie zu verlassen (siehe Incident unten).
- **Ablauf:** main aktualisieren → State-Datei (`~/discord-claude-bot/.vault-sync-last-sha`) mit letztem Sync-Stand vergleichen → bei Aenderungen Branch `gehirn/auto-vault-sync-<datum>` → nicht-interaktive `claude -p`-Session liest Commits/Issues seit letztem Sync UND prüft README.md-Statushaken auf Drift → aktualisiert `ObsidianGehirn/` (und ggf. README-Haken) → Skript committet unsigniert (kein `.claude-secrets/` auf der VM) → pusht → öffnet PR nach main über die GitHub-API. **Merged nie selbst**, das bleibt manuell bei Anton/Felix (siehe [[Branch-Strategie]]).
- **Sicherheitsnetz:** Bricht komplett ohne Aenderung ab (nur Discord-Warnung im `pi-projekt`-Kanal), wenn das Arbeitsverzeichnis auf der VM beim Start schon nicht sauber ist – verhindert, dass unfertige/uncommittete Arbeit eines Teammitglieds versehentlich in den Auto-Commit gerät (ist am 26.08. genau so passiert und wurde gefixt, siehe Log). **Seit 28.08.2026:** ein ERR-Trap fängt zusätzlich **jeden** unerwarteten Skript-Abbruch ab (nicht nur den bekannten "dirty tree"-Fall) und schickt eine Discord-Warnung inkl. Zeile/Exit-Code (siehe Incident unten); die vorher 3x fast identisch duplizierte Discord-Notify-Logik wurde dafür in eine Helper-Funktion konsolidiert.
- **Bekannte Grenze:** Bleibt ein PR mehrere Tage ungemerged, bauen Folge-PRs **nicht** darauf auf (jeder Tag vergleicht nur zum eigenen Vortag) – bei mehreren offenen Sync-PRs also möglichst in Entstehungsreihenfolge mergen, sonst drohen Konflikte.
- **Log:** `~/discord-claude-bot/vault-sync.log` auf der VM.

### Incident: 2 Tage stiller Ausfall durch abgelaufene OAuth-Credentials (27./28.08.2026)
Root Cause: Die einmalig zu Beginn kopierten OAuth-Credentials des Vault-Sync-Accounts rotierten unabhängig vom Original-Account (`amogus_911`) weiter und liefen irgendwann ab ("OAuth session expired and could not be refreshed"). Weil `set -e` das Skript beim ersten fehlgeschlagenen Befehl sofort beendete und es damals noch keinen generischen ERR-Trap gab, gab es dafür keine Fehlermeldung – im Log stand nur "Starte Claude-Session...", dann zwei Tage lang nichts mehr, unbemerkt. Gefixt in PR [#50](https://github.com/47Felix/RasberryPI-Team-13/pull/50) durch die frische Credential-Kopie vor jedem Lauf (siehe oben) und den neuen ERR-Trap.

## Offene Punkte
Siehe [[Offene Punkte]] – u.a. weitere Teammitglieder registrieren, Discord-Bot-Token rotieren, Entscheidung Session-pro-Thread vs. Session-pro-User, Server-Design-Feature erstmals testen.

## Verwandte Notizen
- [[Pi Zugriff]]
- [[Git Workflow]]
- [[⚠️ Zugangsdaten - Hinweis]]

#projekt #discord #claude-code #infrastruktur
