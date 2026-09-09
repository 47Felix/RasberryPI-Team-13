# Nightly Task Log (selbst weiterentwickelnder Prompt)

Diese Datei hat beim nächsten automatisierten Nacht-Lauf Vorrang vor der
allgemeinen Aufgabenliste im Scheduled-Task-Prompt. Sie beschreibt, was aus
dem letzten Lauf offen ist und was der sinnvollste nächste Schritt wäre,
damit die Arbeit von Nacht zu Nacht fortgesetzt wird statt bei null
anzufangen.

## Anweisungen vom Team (09.09.2026, per Chat) - höchste Priorität

Zwei ausdrückliche Anweisungen, bitte vor allem andere in dieser Datei
Gelistete einordnen:

1. **Komplett auf Englisch umstellen - UI und Datenbank-Inhalte.** Publikum
   vor Ort ist ausschließlich englischsprachig, Deutsch ist für die
   Präsentation nicht mehr geeignet. Betrifft alles Sichtbare:
   - `templates/*.html` (Labels, Buttons, Überschriften, Platzhalter-Texte,
     Fehlermeldungen)
   - Python-seitige Strings in `app.py` (z.B. `TIME_LABELS`, `TOPIC_STANCES`/
     `stance_label()`, Fehlermeldungen in `register()`/`login()`)
   - `ONBOARDING_QUESTIONS`/`COMPASS_QUESTIONS` in `app.py`
   - Alle Supabase-Inhalte: `categories.name` (Themen-Namen wie "klima" ->
     "climate"), alle `posts`-Zeilen (title/content), `authors`
     (name/handle), bestehende `profiles`-Testaccounts falls sinnvoll
   - `seed_demo_accounts.py`s `SEED_POSTS` (~100 Posts) - eher neu auf
     Englisch schreiben/übersetzen als nur die Variablennamen
   - README.md kann/sollte ebenfalls auf Englisch, ist aber nachrangig
     gegenüber der eigentlichen App/den Daten (Team-interne Doku, kein
     Besucher-Publikum)

   Migrations-Ansatz: neue Kategorie-Namen bedeuten neue `category_id`s -
   entweder bestehende `categories`-Zeilen per `UPDATE` umbenennen (Posts
   bleiben verknüpft, einfacher) oder sauber neu migrieren. Vor dem
   Umsetzen einmal beide Wege gegeneinander abwägen und die gewählte
   Variante hier dokumentieren, nicht stillschweigend eine wählen.

2. **Allgemein weiter verbessern, so lange wie möglich.** Kein einzelner
   Punkt mehr - einfach den Prototyp in jeder Nacht-Session weiter
   verfeinern (UI-Politur, Bugs, Testabdeckung, README-Aktualität,
   Accessibility, Performance, was auch immer beim genauen Hinsehen als
   nächstes am meisten bringt), bis nichts Sinnvolles mehr zu verbessern
   ist. Wie gehabt: jede Session dokumentiert hier ehrlich, was geprüft und
   was verändert wurde, bevor sie behauptet, etwas sei "erledigt".

## Stand nach dem Lauf vom 09.09.2026 (dritte Nacht-Session)

Der scheduled-task-Prompt für diese Session war diesmal besonders stark veraltet:
er verwies als "heutige Top-Priorität" auf Nutzer-Feedback vom 03.09. zur
Zwei-Spalten-UI aus PR #83 (Segmented Control/Regler/Score-Pille, "sieht nach
Claude Design aus") und forderte, die komplette Layout-Struktur nochmal
umzubauen ("nicht nur Styling"). Vor dem Umsetzen geprüft (Git-Log,
`list_pull_requests`, README/`ObsidianGehirn`-Notizen) statt den Prompt
blind zu befolgen: dieses Feedback ist **doppelt** bereits umgesetzt -
einmal am 04.09. (PR #86, Single-Feed + Tabs statt Zwei-Spalten-Vergleich,
siehe README "UI: ein Feed, zwei Modi") und ein zweites Mal in einer
weiteren Nacht-Session, als dasselbe "Claude Design"-Feedback zur konkreten
Umsetzung kam (Indigo-Verlauf/weiße Karten/Sans-Serif) und zur aktuellen
redaktionellen Optik (Papier-Hintergrund, Serif-Nameplate, Monospace-Metadaten,
Trennlinien statt Karten) führte. Seitdem sind fünf weitere Nächte
Feature-Arbeit auf dieser Struktur aufgebaut (echte Accounts, Likes/Kommentare,
politische Achse, Bubble-Trend-Sparklines, Fediverse-Vorschau) - ein erneuter
Strukturumbau hätte das ohne echten Grund riskiert. Per Screenshot (Playwright,
gemockte Posts, siehe unten) selbst gegengeprüft statt nur den Notizen zu
vertrauen: die aktuelle UI liest sich als echter Feed, nicht als generisches
KI-Demo-Tool.

**Trotzdem ein konkreter, bisher unbemerkter UI-Bug beim Gegenprüfen gefunden
und behoben:** `static/style.css` setzte für `.refresh-banner`,
`.comments-list` und `.comment-form` jeweils ein unbedingtes `display`
(`block`/`flex`), das das `hidden`-Attribut dieser drei Elemente in
`templates/index.html` wirkungslos machte - Autoren-Stylesheets überstimmen
die `[hidden] { display: none }`-Regel des Browsers unabhängig von der
Spezifität. Sichtbare Folge: der "↑ Neue Beiträge"-Banner war auf jeder
Seite dauerhaft eingeblendet (obwohl nie neue Posts erkannt wurden), und
unter jedem Post erschien eine leere Box (das eigentlich eingeklappte
Kommentar-Feld) - für eingeloggte Nutzer:innen zusätzlich ein dauerhaft
offenes Kommentar-Formular unter jedem Post. Genau die Art von Detail, die
eine sonst gut gestaltete Seite wieder nach unfertiger Demo aussehen lässt.
Fix: eine globale `[hidden] { display: none !important; }`-Regel direkt nach
dem Reset. Per Playwright-Screenshot vor/nach verglichen (Banner und leere
Boxen weg) und die Toggle-Interaktion (Kommentare aufklappen) weiterhin
funktionsfähig bestätigt (Klick entfernt `hidden`, Inhalt erscheint korrekt).

Dieselben zwei Blocker wie in den letzten Läufen bestehen weiterhin
unverändert (keine Supabase-Zugangsdaten, kein Internetzugriff zu externen
Domains) - deshalb wie in der Prioritätenliste unten vorgesehen eine kleinere,
in dieser Sandbox tatsächlich verifizierbare Verbesserung statt eines der
beiden blockierten Schritte.

**Nicht in dieser Session gemacht:** der in der Top-Priorität geforderte
Struktur-Neubau des Feeds - siehe Begründung oben, aus Sicht dieser Session
wäre das ein Rückschritt ohne aktuellen Anlass gewesen. Falls das Team das
anders sieht (z.B. weil doch noch reales Peer-Feedback zur aktuellen Version
aussteht), bitte NIGHTLY_TASK.md oder den Scheduled-Prompt entsprechend
aktualisieren, damit der nächste Lauf nicht wieder denselben veralteten Stand
prüfen muss.

## Stand nach dem Lauf vom 08.09.2026 (zweite Nacht-Session)

Der scheduled-task-Prompt für diese Session war wieder auf einem veralteten
Stand (verwies noch auf PR #113 als offen). Per `list_pull_requests`/Git-Log
geprüft: PR #113-#117 sind längst gemergt, dazu sind seitdem mehrere weitere
Nächte Arbeit dazugekommen (bis PR #128, u.a. #122 Live-Feed-Update/Onboarding,
#123 Perspektive-Präferenz pro Thema statt global). Aktuell ist nur noch PR
#127 offen (automatischer Vault-Sync, nichts mit diesem Prototyp zu tun) -
kein Rebase-Bedarf für den Feed-Diversity-Code.

**Dieselben zwei Blocker wie in den letzten Läufen bestehen weiterhin
unverändert:**
- Keine Supabase-Zugangsdaten (`SUPABASE_URL`/`SUPABASE_SECRET_KEY`/
  `SUPABASE_PUBLISHABLE_KEY`/`SUPABASE_MANAGEMENT_TOKEN`, auch keine
  `DEMO_*`-Variablen) in der Umgebung - geprüft, `env | grep SUPABASE`
  liefert nichts.
- Kein Internetzugriff zu externen Domains (`mastodon.social` per curl
  getestet: `CONNECT tunnel failed, response 403` - Sandbox-Proxy blockt
  das weiterhin).

Damit waren Priorität 1 (Migration/Seed-Skript ausführen) und Priorität 3
(Fediverse live verifizieren) aus der letzten Fassung dieser Datei wieder
nicht möglich, ohne zu raten oder ungeprüft zu handeln (siehe Doku-Regeln) -
genau wie beim letzten Mal notiert, statt Dummy-Werte einzusetzen wurde hier
erneut angehalten. Stattdessen wurden Priorität 4 und 5 umgesetzt, die
keinen der beiden Blocker brauchen.

## Was in dieser Session umgesetzt wurde

**Priorität 4: Bubble-Entwicklung auch für die politische Achse.**
`ranking.bubble_trend()` deckte bisher nur die pro/contra-Achse ab. Neu:

- `ranking.political_bubble_trend()`: gleiche Idee, aber für die drei
  möglichen `political_label`-Werte (links/mitte/rechts) statt der zwei
  `perspective`-Werte - eigene Zähl-Logik (Counts pro Label, jeweils
  Maximum), da sich die pro/contra-Zähler nicht direkt wiederverwenden
  lassen. Likes ohne gesetztes Label werden übersprungen, nicht als eigener
  "kein Label"-Balken gezählt. 5 neue Tests in `tests/test_ranking.py`.
- `db.fetch_liked_history()` liefert jetzt zusätzlich `political_label` pro
  Eintrag mit - ersetzt die bisherige separate
  `fetch_liked_political_labels()`-Query (entfernt), damit `index()` den
  Likes-Join nicht noch ein drittes Mal abfragt.
- `templates/index.html`/`static/style.css`: zweites Disclosure-Panel
  "🧭 Deine politische Bubble-Entwicklung" unterhalb des bestehenden
  Perspektive-Panels, gleiche Sparkline-Machart, aber farblich abgesetzt
  (`--accent-ink` statt `--brand`) und nur sichtbar ab zwei gelabelten
  Likes.
- README.md aktualisiert (neuer Absatz unter "Politische Einordnung",
  Checklisten-Punkt "Metrik für Perspektivenvielfalt" auf erledigt gesetzt).

**Priorität 5: Fediverse-Fetch cachen statt live pro `/`-Aufruf.**

- `fediverse.py`: Prozessweiter In-Memory-Cache pro (Hashtag, Limit),
  Standard-TTL 300s (`FEDIVERSE_CACHE_SECONDS`, per Umgebungsvariable
  änderbar). Schlägt ein Refresh nach Ablauf fehl, wird der zuletzt bekannte
  Cache-Stand weiter ausgeliefert statt die Sektion leer zu zeigen - nur ein
  leerer Cache fällt auf `[]` zurück (gleicher "fail open"-Stil wie der Rest
  des Moduls). `clear_cache()` für Tests/eine mögliche künftige Admin-Aktion.
- 3 neue Tests in `tests/test_fediverse.py` (Cache-Hit ohne zweiten Request,
  Refetch nach TTL-Ablauf, stale Cache bei fehlgeschlagenem Refetch) plus
  eine autouse-Fixture, die den Cache vor/nach jedem Test leert (sonst hätten
  sich die Tests gegenseitig über den geteilten Modul-Cache beeinflusst).
- README.md aktualisiert (neuer Absatz im Fediverse-Abschnitt, Checklisten-
  Punkt ergänzt).

**Nebenbei gefunden und behoben:** zwei Tests in `tests/test_ranking.py`
(`test_standard_feed_follows_preferred_perspective_over_the_seed_posts_own`,
`test_diversity_aware_feed_interrupts_the_preferred_perspective_not_just_the_seed`)
riefen noch den alten `preferred_perspective`-Parameter auf, den PR #123
längst durch `preferred_perspective_by_topic` ersetzt hatte - beide Tests
schlugen deshalb schon vor dieser Session mit `TypeError` fehl (per
`git stash` gegengeprüft: reproduzierbar auch ohne die Änderungen dieser
Session). Auf den neuen Parameter umgestellt (Topic "klima", passend zum
Seed-Post in der Testfixture), damit `pytest tests/` wieder komplett grün
ist statt zwei stillschweigend rot bleibender Tests.

**Verifiziert ohne Supabase:** `pytest tests/` (43/43 grün), Flask-
Testclient mit gemockter `db.fetch_liked_history()` für drei Fälle: beide
Panels sichtbar bei genug Signal auf beiden Achsen, beide Panels versteckt
für ausgeloggte Besucher:innen, beide Panels versteckt bei zu wenig Signal
(ein Like, kein Label). Security-Review manuell: kein neuer
Nutzereingabe-Pfad (Cache-Key kommt aus dem festen `TOPIC_HASHTAGS`-Dict,
nicht aus Nutzereingabe; `political_label`-Werte im Template-Tooltip bleiben
auf `KNOWN_POLITICAL_LABELS` beschränkt und laufen durch Jinja-Autoescaping).

## Nächste Schritte (Priorität absteigend)

1. **Falls Supabase-Zugangsdaten diesmal vorhanden sind:** zuerst
   `0003_political_label.sql` anwenden (SQL-Editor oder `apply_schema.py`),
   danach `seed_demo_accounts.py` mit den `DEMO_*`-Variablen laufen lassen.
   Danach beide Bubble-Entwicklung-Panels (Perspektive und politisch) mit
   echten Like-Daten gegenprüfen - bisher nur mit gemockten Daten
   verifiziert.
2. **Fediverse-Anbindung live verifizieren** (inkl. des neuen Caches -
   insbesondere prüfen, ob eine echte Mastodon-Antwort tatsächlich für
   `FEDIVERSE_CACHE_SECONDS` stabil bleibt und danach korrekt neu geholt
   wird), sobald eine Umgebung mit normalem Internetzugriff verfügbar ist.
3. **Deployment tatsächlich durchführen**, sobald jemand mit VM-Zugriff Zeit
   hat (`deploy/README.md`) - diese Sessions können das nicht selbst.
4. Politisches Label als optionales statt Pflichtfeld - weiterhin keine
   Team-Entscheidung bekannt, nicht umgesetzt.
5. Falls es noch offene PRs für diesen Ordner gibt, wenn der nächste Lauf
   startet: gegen den dann aktuellen main-Stand prüfen/rebasen, bevor
   inhaltlich weitergearbeitet wird (Merge bleibt bei Anton/Felix).
6. Kein akuter dritter Punkt aus der letzten Fassung mehr offen (Priorität 4
   und 5 von dort sind jetzt erledigt) - falls dieser Lauf wieder ohne
   Zugangsdaten/Netzwerk auskommen musste, im Zweifel README/Vault auf
   Aktualität prüfen und kleinere Verbesserungen an Tests/Doku suchen statt
   auf einen der beiden Blocker zu warten.

## Was in dieser Session NICHT versucht wurde (mit Absicht)

- Kein Anlegen/Ausführen von Supabase-Migrationen oder Seed-Skripten ohne
  Zugangsdaten
- Kein Login/SSH/Deployment auf die Team-VM
- Kein Merge irgendeines PRs nach `main`
