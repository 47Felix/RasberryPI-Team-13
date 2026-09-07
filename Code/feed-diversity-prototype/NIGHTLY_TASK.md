# Nightly Task Log (selbst weiterentwickelnder Prompt)

Diese Datei hat beim nächsten automatisierten Nacht-Lauf Vorrang vor der
allgemeinen Aufgabenliste im Scheduled-Task-Prompt. Sie beschreibt, was aus
dem letzten Lauf offen ist und was der sinnvollste nächste Schritt wäre,
damit die Arbeit von Nacht zu Nacht fortgesetzt wird statt bei null
anzufangen.

## Stand nach dem Lauf vom 07.09.2026 (Nacht)

Fünf Pull Requests wurden geöffnet, keiner gemergt (Merge bleibt bei
Anton/Felix, siehe Branch-Strategie):

1. **PR #113** (`code/political-label-and-editorial-redesign`): politische
   Einordnung (links/mitte/rechts) als zweite, unabhängige Dimension neben
   pro/contra, plus komplettes visuelles Redesign weg vom generischen
   SaaS-/KI-Look. **Basis für #114 und #115** - sollte zuerst gemergt werden.
2. **PR #114** (`code/demo-account-seed-script`, Basis: #113):
   `seed_demo_accounts.py` für vier Beispiel-Accounts + Admin mit
   gegensätzlicher Like-Historie. **Nicht ausgeführt.**
3. **PR #115** (`code/fediverse-public-posts`, Basis: #113): erster
   risikoarmer Fediverse-Schritt, öffentliche Mastodon-Posts rein lesend im
   Feed. **Nicht live gegen die echte Mastodon-API getestet** (Sandbox-Netzwerk
   blockt externe Domains).
4. **PR #116** (`gehirn/marketing-strategie-update-features`, Basis: `main`):
   Marketing-Strategie-Notiz um die neuen Features ergänzt.
5. **PR #117** (`code/feed-diversity-deploy-prep`, Basis: `main`):
   Gunicorn-systemd-Unit + Caddyfile + Anleitung, nicht angewendet.

Alle Tests grün (`pytest tests/`, zuletzt 31/31 auf dem Stand von #113+#115
zusammen). Keine Zugangsdaten wurden committet.

## Größter Blocker: keine Supabase-Zugangsdaten in dieser Session

`SUPABASE_URL`/`SUPABASE_SECRET_KEY`/`SUPABASE_PUBLISHABLE_KEY`/
`SUPABASE_MANAGEMENT_TOKEN` standen in dieser Session **nicht** als
Umgebungsvariable zur Verfügung (laut Aufgaben-Prompt sollten sie eigentlich
schon hinterlegt sein). Dadurch blieben drei Dinge unerledigt, die inhaltlich
fertig vorbereitet sind:

- `supabase/migrations/0003_political_label.sql` wurde nicht angewendet
- `seed_demo_accounts.py` wurde nicht ausgeführt (zusätzlich fehlen die
  `DEMO_ACCOUNT_A..D_EMAIL`/`_PASSWORD` und `DEMO_ADMIN_EMAIL`/`_PASSWORD`
  Variablen, die derselbe Nacht-Lauf beim ersten Mal noch festlegen müsste)
- Kein End-to-End-Test gegen die echte Instanz möglich

**Falls der nächste Lauf wieder keine Supabase-Zugangsdaten hat:** nicht
raten/Dummy-Werte einsetzen (siehe Doku-Regeln), sondern wie in dieser
Session an der Stelle anhalten und im Chat/in dieser Datei erneut vermerken.

## Nächste Schritte (Priorität absteigend)

1. **Falls Supabase-Zugangsdaten diesmal vorhanden sind:** zuerst
   `0003_political_label.sql` anwenden (`apply_schema.py` oder SQL-Editor),
   danach `seed_demo_accounts.py` mit den `DEMO_*`-Variablen in `.env`
   laufen lassen und das Ergebnis (Standard-Feed mit sichtbarer Bubble pro
   Demo-Account) manuell durchklicken.
2. **Falls PR #113 inzwischen gemergt wurde:** die übrigen offenen PRs
   (#114-#117) gegen den neuen `main`-Stand prüfen/rebasen, falls es
   zwischenzeitlich Konflikte gab.
3. **Fediverse-Anbindung live verifizieren**, falls eine Umgebung mit
   normalem Internetzugriff verfügbar ist (diese Sandbox blockt externe
   Domains) - prüfen, ob `fediverse.py` tatsächlich Posts von
   `mastodon.social` bekommt, Hashtag-Zuordnung in `TOPIC_HASHTAGS` bei
   Bedarf verfeinern (aktuell nur ein erster, ungeprüfter Vorschlag).
4. **Metrik für "Perspektivenvielfalt" über Zeit** (kritischer Punkt 6, seit
   der DTEW-0209-Notiz offen): der Diversity-Score existiert pro
   Feed-Aufruf für beide Achsen (`diversity_score_for_perspective`,
   `diversity_score_for_political_label`), aber es gibt noch keine
   Verlaufsansicht, die zeigt, wie sich das über mehrere Sessions/Likes
   hinweg entwickelt. Könnte z.B. als einfache Tabelle/Sparkline im
   Feed-Einstellungen-Bereich umgesetzt werden.
5. **Fediverse-Fetch cachen statt live pro `/`-Aufruf**, falls die Anbindung
   produktiv genutzt wird (aktuell: jeder Seitenaufruf fragt die externe
   API live an, siehe `fediverse.py` - kein Problem für eine Demo, aber
   unnötige Latenz/Last bei echtem Traffic).
6. **Deployment tatsächlich durchführen**, sobald jemand mit VM-Zugriff Zeit
   hat (`deploy/README.md` durchgehen) - diese Sessions können das nicht
   selbst, siehe Leitplanken im Aufgaben-Prompt.
7. Politisches Label: aktuell ein Pflichtfeld beim Post-Erstellen
   (Standardauswahl "mitte" im Formular). Falls das Team eine echte
   "keine Angabe"-Option möchte statt eines erzwungenen Labels, wäre das
   eine kleine Erweiterung von `KNOWN_POLITICAL_LABELS`/dem Formular -
   bisher nicht umgesetzt, um die Parallele zu `perspective` (auch
   Pflichtfeld) nicht zu brechen, ohne dass das Team das explizit so
   entschieden hat.

## Was in dieser Session NICHT versucht wurde (mit Absicht)

- Kein Login/SSH/Deployment auf die Team-VM (keine Sandbox-Netzwerk-Route
  dorthin, siehe Leitplanken)
- Kein automatischer Links/Rechts-Textklassifikator (siehe README,
  "Politische Einordnung" - bewusste Entscheidung, kein technischer
  Blocker)
- Kein Merge irgendeines PRs nach `main`
