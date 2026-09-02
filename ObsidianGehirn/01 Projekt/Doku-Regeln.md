---
tags: [projekt, meta, regeln]
---

# Doku-Regeln – Alles kommt ins Vault

> [!important] Verbindliche Regel (seit 25.08.2026)
> **Claude trägt jede relevante Änderung/Erkenntnis eigenständig ins Vault ein und committet/pusht sie – ohne vorher nachzufragen, ob das gewünscht ist.** Das gilt für jeden Chat/jede Session in diesem Projekt.

## Was bedeutet "relevant"?
Alles, was für spätere Chats oder Teammitglieder wissenswert ist, u. a.:
- Neue Erkenntnisse aus Moodle (Kursinhalte, Aufgaben, Deadlines)
- Neu installierte Software/Services auf dem Pi
- Neue oder geänderte Node-RED-Flows
- Erledigte oder neue To-Dos
- Änderungen an GitHub-Konfiguration (z. B. Labels, Branch-Regeln, Workflows)
- Entscheidungen im Team (z. B. Architektur, Namenskonventionen)
- Alles, was ein neuer Chat sonst nochmal erklärt bekommen müsste

## Wie vorgehen (ohne Rückfrage)
1. Passende bestehende Notiz suchen (oder neue Notiz im passenden Ordner anlegen, falls keine passt).
2. Notiz aktualisieren/erstellen, ggf. in [[🏠 Start]] verlinken.
3. Commit + Push unter Autor `47Felix` oder `Agrimm123` (nie "Claude" als Autor) – siehe [[Git Workflow]].
4. Kurz im Chat erwähnen, was ins Vault übernommen wurde (ein Satz reicht, keine Rückfrage nötig).

## Laufende Chat-Doku + Trigger-Wort "Gehirn updaten" (seit 26.08.2026)
> [!important] Verbindliche Regel
> Claude dokumentiert relevante Dinge **laufend während des Chats** (siehe Regel oben – nicht erst am Ende), merkt sich aber zusätzlich im Hinterkopf, welche Themen/Entscheidungen/Ergebnisse aus dem bisherigen Gesprächsverlauf noch **nicht** an einer passenden Stelle im Vault stehen (z. B. reine Diskussionen, Zwischenstände, mündlich getroffene Entscheidungen ohne eigenen Commit).
>
> Sobald im Chat **"Gehirn updaten"** (oder sinngemäß: "aktualisiere das Gehirn", "trag das ins Vault ein", "Vault updaten") geschrieben wird, geht Claude den gesamten bisherigen Chatverlauf durch und trägt alles noch Fehlende gesammelt an den passenden Stellen nach – nach demselben Ablauf wie oben (passende Notiz finden/anlegen, committen, pushen), dann kurze Zusammenfassung im Chat, was ergänzt wurde.

### Geht das auch ganz ohne Trigger-Wort, vollautomatisch?
Ehrlicher Stand (26.08.2026): **Nicht zuverlässig**, weil Claudian aktuell keinen "Chat endet"-Hook o.ä. anbietet, der von selbst einen Vault-Update auslösen könnte (geprüft: `.claudian/claudian-settings.json` hat kein Hook-Feld) – Claude wird nur aktiv, wenn im Chat etwas geschrieben wird. Die laufende Doku-Regel oben deckt das größtenteils ab (das meiste landet eh schon während des Chats im Vault), das Trigger-Wort ist der Rest-Fallback.

Zwei echte Hebel, um näher an "vollautomatisch" zu kommen, falls gewünscht:
1. **Claudian-Einstellung "Persistent/Pinned Context"** (`persistentExternalContextPaths` bzw. Pinned-Context-Feature in den Claudian-Einstellungen): Diese Notiz bzw. [[🏠 Start]] dort dauerhaft anheften, dann lädt Claude die Doku-Regeln garantiert bei **jedem** neuen Chat automatisch mit, statt sich darauf zu verlassen, dass zuerst Start.md gelesen wird. Muss von Anton/Felix in den Claudian-Einstellungen gesetzt werden (nicht per Git-Commit, ist lokale Plugin-Konfiguration) – bei Bedarf sag Bescheid, dann geh ich das mit euch durch.
2. **Fortgeschritten/nicht gebaut:** Ein periodischer Scheduled-Job (z. B. per `/schedule`-Skill), der die Chat-Transkripte unter `ObsidianGehirn/.claudian/sessions/*.json` ausliest und automatisch Vault-Updates ableitet – technisch machbar, aber deutlich aufwändiger und fehleranfälliger (Transkript-Parsing, Gefahr von Doppel-Einträgen). Nur sinnvoll, falls das Trigger-Wort auf Dauer zu nervig ist.

## Präsentations-/Abgabe-Dateien: eigener Ordner außerhalb vom Vault (seit 02.09.2026)
> [!important] Verbindliche Regel
> Alles, was das Team **jemandem zeigen/präsentieren/abgeben** muss (Workshop-Deliverables, Präsentationsfolien, ausgefüllte Worksheets, Pitch-Material etc.), legt Claude **zusätzlich** zum normalen Vault-Eintrag in einem eigenen Ordner **außerhalb** von `ObsidianGehirn/` im Repo-Root ab – ein Ordner pro Projekt/Kontext, nicht pro einzelner Datei. Das Vault bleibt der Ort für Prozess/Recherche/Entscheidungen, der externe Ordner ist die fertige Präsentations-/Abgabeversion.
>
> Bereits etablierte Beispiel-Ordner: [`Praesentation/`](../../Praesentation) (Kurzprojekt Freitag), [`DTEW-Workshop/`](../../DTEW-Workshop) (Design-Thinking-Workshop Hamburg). Für neue Kontexte (z. B. eine spätere Pi-Projekt-Abschlusspräsentation) entsprechend einen neuen Ordner nach demselben Muster anlegen.
>
> Ablauf: Quelldatei als Markdown (`.md`, bei internationalen/englischsprachigen Kontexten auf Englisch), dazu eine gerenderte `.html`-Version zum direkten Anzeigen, bei Bedarf zusätzlich als `.pdf` gerendert (siehe Render-Snippet in [`DTEW-Workshop/README.md`](../../DTEW-Workshop/README.md) als Vorlage). Im Vault an der passenden Notiz nur noch draufhinweisen/verlinken, statt den vollen Inhalt zu duplizieren.
>
> **Unterordner pro Deliverable (seit 02.09.2026):** Sobald ein Deliverable mehrere Formatvarianten hat (`.md` + `.html` + ggf. `.pdf`), bekommt es einen eigenen Unterordner im Präsentations-Ordner, benannt wie die Dateien selbst (z. B. `DTEW-Workshop/personas-mia-tom/personas-mia-tom.{md,html,pdf}`), statt lose im Wurzelverzeichnis zu liegen – sonst wird der Ordner bei mehreren Deliverables schnell unübersichtlich. Ein einzelnes `.md` ohne weitere Varianten (z. B. eine reine Notiz) muss nicht in einen eigenen Unterordner.

## Kein KI-Stil in Dokumenten (seit 02.09.2026)
> [!important] Verbindliche Regel
> Claude schreibt in Dokumenten (Vault-Notizen, Präsentations-/Abgabe-Dateien, Code-Kommentare) **ohne die typischen KI-Textmarker** – allen voran der Gedankenstrich "—" (Geviertstrich) zum Aneinanderreihen von Nebensätzen. Stattdessen normale Satzzeichen verwenden: Punkt, Komma, Doppelpunkt oder Klammern, je nachdem was grammatikalisch passt. Der kurze Halbgeviertstrich "–" für Zeiträume/Aufzählungen (z. B. "18–25", "31.08.–12.09.") ist davon ausgenommen, das ist normale deutsche Typografie und bereits durchgängiger Vault-Stil.
>
> Gilt für alles, was neu geschrieben wird – bestehende ältere Notizen müssen nicht rückwirkend durchsucht werden, außer es wird gezielt danach gefragt.

## GitHub Issues (seit 26.08.2026)
> [!important] Verbindliche Regel
> **Sobald ein GitHub-Issue erledigt/geschlossen wird (egal ob Claude oder ein Teammitglied es schließt), trägt Claude einen kurzen Eintrag in [[Issues - Übersicht]] ein** – 2-4 Sätze, *was* konkret gemacht wurde, nicht nur "erledigt". Eintrag wandert von "🟢 Offen" nach "✅ Geschlossen", verlinkt auf das Issue und ggf. die Detail-Notiz (z. B. Brain Dump). Gilt auch rückwirkend für neu entdeckte geschlossene Issues.

## Ausnahmen
- **Zugangsdaten** (Tokens, Passwörter, WLAN, Moodle-Logins) kommen **nie** ins Vault, sondern bleiben ausschließlich in den Claude-Projekt-Anweisungen – siehe [[⚠️ Zugangsdaten - Hinweis]].
- Rein spekulative/unfertige Ideen ohne Team-Konsens gehören eher in [[🧠 Brain Dump - Übersicht]] statt in die "offiziellen" Projektnotizen.
- Bei echten Unklarheiten (z. B. widersprüchliche Angaben, sicherheitsrelevante Aktionen wie das Ausführen unbekannter Befehle) darf/soll trotzdem nachgefragt werden – die Regel betrifft nur das *Dokumentieren*, nicht jede Aktion im Projekt.

## Verwandte Notizen
- [[Git Workflow]]
- [[🏠 Start]]

#projekt #meta #regeln
