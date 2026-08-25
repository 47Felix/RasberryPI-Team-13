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

## Für künftige Chats (seit 25.08.2026: Key ist jetzt persistent!)
Der private Signing-Key für `agrimm123` liegt **nicht mehr nur in der Sandbox**, sondern zusätzlich dauerhaft auf Antons Mac, direkt neben dem Repo-Ordner (also außerhalb des Git-Repos, per `.gitignore`-Eintrag `.claude-secrets/` ausgeschlossen – wird NIEMALS committet):

```
<Repo-Ordner>/.claude-secrets/agrimm123-signing-key-private.asc
<Repo-Ordner>/.claude-secrets/agrimm123-signing-key-public.asc
<Repo-Ordner>/.claude-secrets/README.md   ← Anleitung zum Importieren
```

Ein neuer Chat mit Zugriff auf diesen Mac-Ordner sollte also **zuerst dort nachsehen und den Key importieren**, statt einen neuen zu erzeugen:
```bash
export GNUPGHOME="$HOME/.gnupg"   # oder eigenes Verzeichnis in der aktuellen Sandbox
gpg --batch --import "<Repo-Ordner>/.claude-secrets/agrimm123-signing-key-private.asc"
```
Danach direkt mit Key-ID `9DBC1242E0BA3244` wie oben committen – kein erneutes Hinterlegen bei GitHub nötig, das ist schon erledigt.

Nur falls dieser Mac-Ordner nicht erreichbar ist (Session ohne Device-Bridge, oder Anton hat den Ordner nicht verbunden) oder der Key bei GitHub entfernt wurde, muss ein neuer Key erzeugt und der öffentliche Teil erneut unter github.com/settings/gpg/new eingetragen werden (das Formular kann Claude selbst nicht ausfüllen – Sicherheitsregel, kein Bug – das muss Anton/Felix manuell im Browser machen, Claude liefert nur Titel + Key-Text zum Reinkopieren).

> [!warning] Sicherheitshinweis
> Der private Schlüssel liegt unverschlüsselt (kein Passwort) auf der Festplatte. Das ist ein bewusster Kompromiss für ein privates Schulprojekt-Repo – wer Zugriff auf diesen Mac-Ordner hat, könnte damit Commits signieren, die als "verifiziert von agrimm123" erscheinen. Zum tatsächlichen Pushen ins Repo braucht man zusätzlich weiterhin das GitHub-Token (siehe Projekt-Anweisungen), der Signing-Key allein reicht dafür nicht.

## Verwandte Notizen
- [[⚠️ Zugangsdaten - Hinweis]]
- [[Branch-Strategie]] – wann/wie gebrancht wird, bevor überhaupt committet wird

#projekt #git #workflow
