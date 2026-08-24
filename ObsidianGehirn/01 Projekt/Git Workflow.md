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
| `47Felix` | `47Felix@users.noreply.github.com` | `9EFC3BC5E08A2481` |
| `Agrimm123` | `Agrimm123@users.noreply.github.com` | `4245DD5E87E0692C` |

Commit-Befehl (Beispiel für 47Felix):
```bash
git -c user.name="47Felix" -c user.email="47Felix@users.noreply.github.com" \
    -c user.signingkey="9EFC3BC5E08A2481" -c gpg.program=gpg \
    commit -S -m "Commit-Nachricht"
```
Für `Agrimm123` analog mit dessen E-Mail und Key-ID.

> [!note] Voraussetzung
> Autor-Name, Autor-E-Mail **und** die im Schlüssel hinterlegte E-Mail müssen exakt übereinstimmen, sonst zeigt GitHub trotz gültiger Signatur "Unverified" statt "Verified".

## Warum
- Nachvollziehbarkeit: sichtbar, dass ein Commit tatsächlich von einem autorisierten Teammitglied (bzw. in dessen Auftrag) stammt.
- Best Practice bei Team-Repos, besonders wenn Claude im Auftrag von Teammitgliedern committet.

## Für künftige Chats
Falls ein neuer Chat committet und die Schlüssel nicht mehr im Sandbox-Environment vorhanden sind (Environment wird zurückgesetzt), müssen die GPG-Keys neu erzeugt werden – der **öffentliche** Teil ist dann aber neu und muss erneut bei GitHub hinterlegt werden (alter Public Key kann bei GitHub gelöscht werden). Die Key-IDs oben sind dann nicht mehr gültig.

## Verwandte Notizen
- [[Zugangsdaten - Hinweis]]
- [[Branch-Strategie]] – wann/wie gebrancht wird, bevor überhaupt committet wird

#projekt #git #workflow
