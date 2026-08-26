#!/usr/bin/env bash
# Taeglicher Vault-Sync: laesst eine non-interaktive Claude-Session Commits/Issues seit dem
# letzten Lauf durchgehen, das Obsidian-Vault (ObsidianGehirn/) gemaess Doku-Regeln.md aktualisieren
# UND README.md auf veraltete Status-Haken pruefen/korrigieren (Drift-Check, nicht nur "was ist neu").
# Oeffnet bei Aenderungen einen PR nach main - merged NIE selbst (Branch-Strategie.md).
set -euo pipefail

REPO_PATH="$HOME/RasberryPI-Team-13"
CONFIG_DIR="$HOME/sessions/vault-sync"
STATE_FILE="$HOME/discord-claude-bot/.vault-sync-last-sha"
LOG_FILE="$HOME/discord-claude-bot/vault-sync.log"
ENV_FILE="$HOME/discord-claude-bot/.env"
DATE="$(date +%Y-%m-%d)"
BRANCH="gehirn/auto-vault-sync-$DATE"
NOTIFY_CHANNEL_ID="1542105092596174878"  # pi-projekt (Textkanal im Projekt)

log() { echo "[$(date -Iseconds)] $*" >> "$LOG_FILE"; }

cd "$REPO_PATH"

# GitHub-Token aus der bereits konfigurierten Remote-URL ziehen (gleiches Fine-Grained-Token
# wie fuer den interaktiven Bot/Repo-Clone, liegt nicht separat im Vault - siehe Zugangsdaten-Hinweis)
GH_TOKEN="$(git remote get-url origin | sed -E 's#https://([^:@]+)@github.com.*#\1#')"

log "=== Vault-Sync Start ($DATE) ==="

git checkout main >>"$LOG_FILE" 2>&1
git pull origin main >>"$LOG_FILE" 2>&1

LAST_SHA="$(cat "$STATE_FILE" 2>/dev/null || true)"
if [ -z "$LAST_SHA" ] || ! git cat-file -e "$LAST_SHA" 2>/dev/null; then
  # Erster Lauf oder State verloren: letzte 24h als Fallback-Fenster nehmen
  LAST_SHA="$(git log --since='24 hours ago' --format=%H main | tail -1)"
  [ -z "$LAST_SHA" ] && LAST_SHA="$(git rev-parse main)"
fi
CURRENT_SHA="$(git rev-parse main)"
log "Vergleiche $LAST_SHA..$CURRENT_SHA"

if [ "$LAST_SHA" = "$CURRENT_SHA" ]; then
  log "Keine neuen Commits auf main seit letztem Sync - nichts zu tun."
  exit 0
fi

# Sicherheitscheck: Arbeitsverzeichnis muss sauber sein, BEVOR Claude drangeht.
# Verhindert, dass fremde/unfertige Aenderungen eines Teammitglieds (z.B. eine noch nicht
# committete Notiz) versehentlich per 'git add -A' in den Auto-Sync-Commit mitgezogen werden.
DIRTY="$(git status --porcelain)"
if [ -n "$DIRTY" ]; then
  log "ABBRUCH: Arbeitsverzeichnis auf main ist nicht sauber, moeglicherweise unfertige Arbeit eines Teammitglieds. Ueberspringe diesen Lauf ohne Aenderungen:"
  log "$DIRTY"
  if [ -f "$ENV_FILE" ]; then
    DISCORD_BOT_TOKEN="$(grep -oP '(?<=^DISCORD_BOT_TOKEN=).*' "$ENV_FILE")"
    curl -s -X POST "https://discord.com/api/v10/channels/$NOTIFY_CHANNEL_ID/messages" \
      -H "Authorization: Bot $DISCORD_BOT_TOKEN" -H "Content-Type: application/json" \
      -d "$(python3 -c "import json; print(json.dumps({'content': '⚠️ Vault-Sync uebersprungen: main hat unversionierte/uncommittete Aenderungen im Arbeitsverzeichnis der VM. Bitte pruefen, bevor der naechste Sync laeuft.'}))")" \
      >>"$LOG_FILE" 2>&1
  fi
  exit 0
fi

git checkout -b "$BRANCH" >>"$LOG_FILE" 2>&1

PROMPT="Du bist der taegliche automatische Vault-Sync fuer dieses Repo (nicht-interaktiv, per Cron).

Lies zuerst ObsidianGehirn/01 Projekt/Doku-Regeln.md - das sind deine verbindlichen Regeln fuer WAS ins Vault gehoert und wie.
Lies auch ObsidianGehirn/09 Issues/Issues - Uebersicht.md fuer das erwartete Format dort.

Aufgabe:
1. Sieh dir die main-Commits zwischen $LAST_SHA und $CURRENT_SHA an (git log $LAST_SHA..$CURRENT_SHA, inkl. welche Dateien/Pfade jeweils geaendert wurden), sowie ueber die GitHub-API (curl mit dem Token aus 'git remote get-url origin', Repo 47Felix/RasberryPI-Team-13) neu geschlossene Issues und gemergte PRs seit diesem Zeitraum.
2. Aktualisiere Dateien unter ObsidianGehirn/ gemaess Doku-Regeln.md: neue Erkenntnisse, erledigte To-Dos (Offene Punkte.md), neu geschlossene Issues (Issues - Uebersicht.md, mit 2-4 Saetzen was gemacht wurde, siehe Format dort), relevante neue Entscheidungen/Setups.
3. Pruefe zusaetzlich gezielt auf Drift zwischen Repo-Realitaet und Dokumentation (nicht nur 'was ist neu', sondern 'was steht noch falsch/veraltet da'):
   - README.md im Repo-Root: enthaelt eine 'Status / offene Punkte'-Checkliste. Vergleiche deren Haken-Status mit dem tatsaechlichen Issue-Stand (GitHub-API) und mit ObsidianGehirn/09 Issues/Issues - Uebersicht.md. Falsche Haken (offen obwohl Issue laengst zu, oder umgekehrt) darfst du direkt in README.md korrigieren - aber NUR objektiv belegbare Haken-Korrekturen, keine sonstigen README-Umschreibungen.
   - Wenn im Diff-Zeitraum neuer Code unter Code/ (z.B. Code/discord-bot/) hinzukam oder sich geaendert hat: pruefe, ob ObsidianGehirn/01 Projekt/Claude Discord Bot Setup.md das noch akkurat beschreibt (Pfade, Ablauf, Cron-Zeiten etc.) und aktualisiere falls noetig.
   - Wenn ein Branch/PR seit mehreren Tagen offen und ungemerged ist (ueber GitHub-API pruefbar), trage das als Hinweis in Offene Punkte.md ein, statt es zu ignorieren.
4. Fasse dich kurz und praezise, keine Spekulation - nur was aus den Commits/Issues/PRs tatsaechlich hervorgeht.
5. Wenn nach Durchsicht nichts Relevantes dabei ist (z.B. nur Code-Commits ohne dokumentationswuerdige Aenderung und README schon korrekt), aendere NICHTS und sag das explizit in deiner Antwort.
6. Fasse am Ende in 2-3 Saetzen zusammen, was du geaendert hast (oder dass nichts zu tun war).

Wichtig: Committe/pushe/mergen NICHTS selbst - das erledigt das aufrufende Skript. Aendere ausschliesslich Dateien unter ObsidianGehirn/ sowie (nur fuer Checklisten-Korrekturen wie oben beschrieben) README.md - sonst nichts."

log "Starte Claude-Session (CLAUDE_CONFIG_DIR=$CONFIG_DIR)..."
CLAUDE_OUTPUT="$(CLAUDE_CONFIG_DIR="$CONFIG_DIR" claude -p "$PROMPT" --output-format json --dangerously-skip-permissions 2>>"$LOG_FILE")"
echo "$CLAUDE_OUTPUT" >> "$LOG_FILE"

if [ -z "$(git status --porcelain -- ObsidianGehirn/ README.md)" ]; then
  log "Claude hat nichts Vault-relevantes gefunden - kein Commit, Branch wird verworfen."
  git checkout main >>"$LOG_FILE" 2>&1
  git branch -D "$BRANCH" >>"$LOG_FILE" 2>&1
  echo "$CURRENT_SHA" > "$STATE_FILE"
  exit 0
fi

git add ObsidianGehirn/ README.md
# Kein .claude-secrets/ auf dieser VM -> unsigniert committen (siehe Git Workflow.md Checkliste)
git -c user.name="47Felix" -c user.email="47Felix@users.noreply.github.com" \
    commit -m "Automatischer Vault-Sync $DATE" >>"$LOG_FILE" 2>&1
git push -u origin "$BRANCH" >>"$LOG_FILE" 2>&1

PR_JSON="$(curl -s -X POST "https://api.github.com/repos/47Felix/RasberryPI-Team-13/pulls" \
  -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  -d "$(python3 -c "
import json
print(json.dumps({
  'title': 'Automatischer Vault-Sync $DATE',
  'head': '$BRANCH',
  'base': 'main',
  'body': 'Automatisch vom taeglichen Vault-Sync-Cronjob erstellt (vault-sync.sh). Bitte pruefen und manuell mergen - siehe Branch-Strategie.md.'
}))
")")"
PR_URL="$(echo "$PR_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('html_url',''))")"
log "PR erstellt: $PR_URL"

echo "$CURRENT_SHA" > "$STATE_FILE"

git checkout main >>"$LOG_FILE" 2>&1

if [ -n "$PR_URL" ]; then
  DISCORD_BOT_TOKEN="$(grep -oP '(?<=^DISCORD_BOT_TOKEN=).*' "$ENV_FILE")"
  curl -s -X POST "https://discord.com/api/v10/channels/$NOTIFY_CHANNEL_ID/messages" \
    -H "Authorization: Bot $DISCORD_BOT_TOKEN" -H "Content-Type: application/json" \
    -d "$(python3 -c "import json; print(json.dumps({'content': '📚 Taeglicher Vault-Sync: neuer PR $PR_URL (bitte pruefen/mergen)'}))")" \
    >>"$LOG_FILE" 2>&1
fi

log "=== Vault-Sync Ende ==="
