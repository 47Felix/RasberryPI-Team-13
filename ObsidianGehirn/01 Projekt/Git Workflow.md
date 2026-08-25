---
tags: [projekt, git, workflow]
---

# Git Workflow – Regeln für Commits

> [!important] Verbindliche Regel (aktualisiert 25.08.2026, nach einem Vorfall)
> **Signieren ist "nice to have", aber NIEMALS auf Verdacht.** Ein Commit wird nur mit `-S` signiert, wenn VORHER zweifelsfrei geprüft wurde, dass der passende, bei GitHub hinterlegte Key im aktuellen Environment importiert ist (siehe Checkliste unten). Ist das nicht der Fall: **ganz normal unsigniert committen, ohne `-S`.** Ein unsignierter Commit zeigt bei GitHub gar kein Badge (unauffällig) – ein signierter Commit mit falschem/unbekanntem Key zeigt dagegen ein rotes **"Unverified"**-Badge, was schlimmer aussieht als kein Badge. Anton hat das ausdrücklich so gewünscht: "lieber nichts als Unverified".
>
> **Vorfall (25.08.2026):** Ein Chat hat mit `-S` committet, aber mit falscher Identität (`antongrimm@outlook.de` statt `agrimm123@users.noreply.github.com`, bzw. ohne den passenden Key importiert zu haben) → Commit `26fafac` zeigt bei GitHub "Unverified" (`reason: unknown_key`). Das war der Auslöser für diese Regeländerung.

## ⚠️ Checkliste VOR jedem `-S`-Commit
1. Ist ein Mac-Ordner mit `.claude-secrets/` verbunden/erreichbar? Wenn nein → **unsigniert committen, fertig.**
2. `gpg --batch --import "<Repo-Ordner>/.claude-secrets/<name>-signing-key-private.asc"` ausführen.
3. `gpg --list-secret-keys --keyid-format LONG <exakte-email>@users.noreply.github.com` ausführen und **die Key-ID mit der Tabelle unten exakt vergleichen**. Passt sie nicht → unsigniert committen.
4. Erst wenn Key-ID UND E-Mail exakt passen: mit `-S` und genau dieser Key-ID + E-Mail committen.
5. Nach dem Push zur Sicherheit kurz per GitHub-API prüfen (`.commit.verification.verified`), ob's wirklich "Verified" ist – nicht blind vertrauen.

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
