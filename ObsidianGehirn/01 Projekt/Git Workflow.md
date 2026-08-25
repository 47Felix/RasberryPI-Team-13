---
tags: [projekt, git, workflow]
---

# Git Workflow – Regeln für Commits

> [!important] Verbindliche Regel (seit 24.08.2026)
> **Alle Commits sollen signiert sein und bei GitHub als "Verified" angezeigt werden.** Das gilt für jeden Chat/jede Session, die Änderungen ins Repository committet.

## Wie das umgesetzt wird
Für beide bisherigen Commit-Autoren wurde ein GPG-Signing-Key erzeugt und im jeweiligen GitHub-Account unter **Settings → SSH and GPG keys** als *Signing Key* hinterlegt:

| Account | E-Mail (muss exakt passen) | Key-ID |
|---|---|---|
| `47Felix` | `47Felix@users.noreply.github.com` | `9EFC3BC5E08A2481` (alt, evtl. nicht mehr im aktuellen Sandbox-Environment vorhanden) |
| `agrimm123` | `agrimm123@users.noreply.github.com` (Kleinschreibung! GitHub-Konto heißt `agrimm123`, nicht `Agrimm123`) | `9DBC1242E0BA3244` (neu erzeugt am 25.08.2026, bei GitHub hinterlegt) |

Commit-Befehl (aktuell für agrimm123, Stand 25.08.2026):
```bash
git -c user.name="Agrimm123" -c user.email="agrimm123@users.noreply.github.com" \
    -c user.signingkey="9DBC1242E0BA3244" -c gpg.program=gpg \
    commit -S -m "Commit-Nachricht"
```
Für `47Felix` analog, sobald dessen Key in einem aktiven Environment neu erzeugt und bei GitHub hinterlegt wurde (siehe Abschnitt "Für künftige Chats" unten – der alte Key `9EFC3BC5E08A2481` ist vermutlich nicht mehr nutzbar, da Sandbox-Environments zurückgesetzt werden).

> [!note] Voraussetzung
> Autor-Name, Autor-E-Mail **und** die im Schlüssel hinterlegte E-Mail müssen exakt übereinstimmen, sonst zeigt GitHub trotz gültiger Signatur "Unverified" statt "Verified".

## Warum
- Nachvollziehbarkeit: sichtbar, dass ein Commit tatsächlich von einem autorisierten Teammitglied (bzw. in dessen Auftrag) stammt.
- Best Practice bei Team-Repos, besonders wenn Claude im Auftrag von Teammitgliedern committet.

## Für künftige Chats
Falls ein neuer Chat committet und die Schlüssel nicht mehr im Sandbox-Environment vorhanden sind (Environment wird zurückgesetzt), müssen die GPG-Keys neu erzeugt werden – der **öffentliche** Teil ist dann aber neu und muss erneut bei GitHub hinterlegt werden (alter Public Key kann bei GitHub gelöscht werden). Die Key-IDs oben sind dann nicht mehr gültig.

## Verwandte Notizen
- [[⚠️ Zugangsdaten - Hinweis]]
- [[Branch-Strategie]] – wann/wie gebrancht wird, bevor überhaupt committet wird

#projekt #git #workflow
