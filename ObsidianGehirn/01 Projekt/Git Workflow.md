---
tags: [projekt, git, workflow]
---

# Git Workflow – Regeln für Commits

> [!important] Verbindliche Regel (aktualisiert 25.08.2026, nach einem Vorfall – bitte GENAU befolgen)
> **Signieren ist "nice to have", aber NIEMALS auf Verdacht.** Ein Commit wird nur mit `-S` signiert, wenn VORHER zweifelsfrei geprüft wurde, dass der passende, bei GitHub hinterlegte Key im aktuellen Environment importiert ist (siehe Checkliste unten). Ist das nicht der Fall: **ganz normal unsigniert committen, ohne `-S`.** Ein unsignierter Commit zeigt bei GitHub gar kein Badge (unauffällig) – ein signierter Commit mit falschem/unbekanntem Key zeigt dagegen ein rotes **"Unverified"**-Badge, was schlimmer aussieht als kein Badge. Anton hat das ausdrücklich so gewünscht: "es soll alles bitte verified oder gar nicht verified sein" – niemals das rote "Unverified".
>
> **🚫 NIEMALS einen neuen GPG-Key erzeugen, wenn schon einer existiert!** Es gibt für beide Accounts bereits fertige, bei GitHub hinterlegte Keys (siehe Tabelle unten), die dauerhaft auf Antons Mac liegen. Ein neuer Chat, der stattdessen einen frischen Key erzeugt und signiert, OHNE ihn bei GitHub zu hinterlegen, verursacht genau das Problem, das wir loswerden wollen ("Unverified", `unknown_key`). Das ist am 25.08.2026 mehrfach passiert (Commits `26fafac`, `9db738c`, `23c5484`) – bitte nicht wiederholen.

## ⚠️ Checkliste VOR jedem `-S`-Commit (immer, ausnahmslos)
1. Ist ein Mac-Ordner mit `.claude-secrets/` verbunden/erreichbar? Wenn nein → **unsigniert committen, fertig, keine weiteren Schritte.**
2. Passenden Key importieren (Datei je nach Autor, siehe Tabelle):
   ```bash
   export GNUPGHOME="$HOME/.gnupg"
   gpg --batch --import "<Repo-Ordner>/.claude-secrets/<name>-signing-key-private.asc"
   ```
3. `gpg --list-secret-keys --keyid-format LONG <exakte-email>` ausführen und **die Key-ID mit der Tabelle unten exakt vergleichen**. Passt sie nicht exakt → unsigniert committen, keinen neuen Key erzeugen.
4. Erst wenn Key-ID UND E-Mail exakt passen: mit `-S` und genau dieser Key-ID + E-Mail committen (Befehle unten).
5. Nach dem Push zur Sicherheit per GitHub-API prüfen (`.commit.verification.verified` muss `true` sein, `reason` muss `valid` sein) – nicht blind vertrauen.

## Aktuelle Keys (Stand 25.08.2026 – beide bei GitHub hinterlegt und getestet, verified: true)

| Account | E-Mail (muss exakt passen, Kleinschreibung!) | Key-ID | Datei in `.claude-secrets/` |
|---|---|---|---|
| `agrimm123` | `agrimm123@users.noreply.github.com` | `9DBC1242E0BA3244` | `agrimm123-signing-key-private.asc` |
| `47Felix` | `47Felix@users.noreply.github.com` | `0DBEA8CC06445AB4` | `47felix-signing-key-private.asc` |

Commit-Befehl agrimm123:
```bash
git -c user.name="Agrimm123" -c user.email="agrimm123@users.noreply.github.com" \
    -c user.signingkey="9DBC1242E0BA3244" -c gpg.program=gpg \
    commit -S -m "Commit-Nachricht"
```

Commit-Befehl 47Felix:
```bash
git -c user.name="47Felix" -c user.email="47Felix@users.noreply.github.com" \
    -c user.signingkey="0DBEA8CC06445AB4" -c gpg.program=gpg \
    commit -S -m "Commit-Nachricht"
```

> [!note] Voraussetzung
> Autor-Name, Autor-E-Mail **und** die im Schlüssel hinterlegte E-Mail müssen exakt übereinstimmen, sonst zeigt GitHub trotz gültiger Signatur "Unverified" statt "Verified".

## Warum überhaupt signieren
- Nachvollziehbarkeit: sichtbar, dass ein Commit tatsächlich von einem autorisierten Teammitglied (bzw. in dessen Auftrag) stammt.
- Best Practice bei Team-Repos, besonders wenn Claude im Auftrag von Teammitgliedern committet.

## Wo die Keys persistent liegen
Beide privaten Keys liegen **dauerhaft auf Antons Mac**, direkt neben dem Repo-Ordner (außerhalb des Git-Repos, per `.gitignore`-Eintrag `.claude-secrets/` ausgeschlossen – wird NIEMALS committet):

```
<Repo-Ordner>/.claude-secrets/agrimm123-signing-key-private.asc
<Repo-Ordner>/.claude-secrets/agrimm123-signing-key-public.asc
<Repo-Ordner>/.claude-secrets/47felix-signing-key-private.asc
<Repo-Ordner>/.claude-secrets/47felix-signing-key-public.asc
<Repo-Ordner>/.claude-secrets/README.md   ← Anleitung zum Importieren
```

Nur falls dieser Mac-Ordner nicht erreichbar ist (Session ohne Device-Bridge, oder Anton hat den Ordner nicht verbunden) → **unsigniert committen**, keinesfalls einen neuen Key erzeugen und ungetestet signieren.

Falls die Keys bei GitHub irgendwann entfernt wurden und wirklich neu aufgesetzt werden muss: neuen Key erzeugen, öffentlichen Teil unter github.com/settings/gpg/new eintragen (Claude darf dieses Formular selbst NICHT ausfüllen – Sicherheitsregel, kein Bug – das muss Anton/Felix manuell im Browser machen, Claude liefert nur Titel + Key-Text zum Reinkopieren), **erst danach** mit `-S` committen und per API verifizieren.

> [!warning] Sicherheitshinweis
> Die privaten Schlüssel liegen unverschlüsselt (kein Passwort) auf der Festplatte. Das ist ein bewusster Kompromiss für ein privates Schulprojekt-Repo – wer Zugriff auf diesen Mac-Ordner hat, könnte damit Commits signieren, die als "verifiziert" erscheinen. Zum tatsächlichen Pushen ins Repo braucht man zusätzlich weiterhin das GitHub-Token, der Signing-Key allein reicht dafür nicht.

## Bekannte, nicht reparierte "Unverified"-Commits in der Historie
`26fafac`, `9db738c`, `23c5484` zeigen dauerhaft "Unverified", weil sie mit einem nie hinterlegten Key signiert wurden. Rückwirkend reparierbar nur per Force-Push/History-Rewrite – bewusst NICHT gemacht, weil das bei einem geteilten Repo riskant ist. Ab 25.08.2026 (nach diesem Fix) sollten keine neuen "Unverified"-Commits mehr entstehen, wenn sich alle Chats an die Checkliste oben halten.

## Verwandte Notizen
- [[⚠️ Zugangsdaten - Hinweis]]
- [[Branch-Strategie]] – wann/wie gebrancht wird, bevor überhaupt committet wird

#projekt #git #workflow
