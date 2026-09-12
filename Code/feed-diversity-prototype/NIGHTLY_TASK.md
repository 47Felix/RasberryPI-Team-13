# Nightly Task Log (selbst weiterentwickelnder Prompt)

Diese Datei hat beim nächsten automatisierten Nacht-Lauf Vorrang vor der
allgemeinen Aufgabenliste im Scheduled-Task-Prompt. Sie beschreibt, was aus
dem letzten Lauf offen ist und was der sinnvollste nächste Schritt wäre,
damit die Arbeit von Nacht zu Nacht fortgesetzt wird statt bei null
anzufangen.

## Anweisungen vom Team (10.09.2026, per Chat, Felix) - höchste Priorität

Diese Fassung ersetzt die bisherige Top-Priorität (Englisch-Umstellung). Der
Englisch-Umbau gilt als erledigt (PR #140 gemergt, db.py-Fallbacks
nachgezogen in `d53cf37`) - ab jetzt nur noch **beibehalten**: wenn dir neuer
deutscher sichtbarer Text auffällt, mit übersetzen, aber es ist nicht mehr der
Fokus.

**Backup-Punkt vor dieser Neuausrichtung:** Tag
`backup/pre-nightly-overhaul-2026-09-10` und Branch `backup/main-2026-09-10`,
beide auf `main @ 99647db` (Refresh-Rotation-Fix PR #148 + 100 zusätzliche
Seed-Posts PR #147). Falls eine Nacht-Session etwas verschlimmbessert, ist das
der Stand, auf den zurückgesetzt werden kann.

### Auftrag: Algorithmus + Refresh gründlich überarbeiten, dann alles andere

Felix' Wortlaut sinngemäß: den Prototyp über die nächsten Nächte "nochmal
komplett überarbeiten, ausbessern - Algorithmus, Refresh und alles". Konkret,
in dieser Reihenfolge:

1. **Ranking-Algorithmus (`ranking.py`)** - der Kern des Prototyps, hier den
   meisten Wert schaffen. Mit frischem, kritischem Blick durchgehen, u.a.:
   - Taugt die TF-IDF + Cosine-Similarity-Basis noch, oder produziert sie auf
     dem inzwischen ~250-Posts-Datensatz erkennbar schlechte Nachbarschaften?
     (Stopwords, n-grams, Titel-Gewichtung, `min_df`/`max_df` prüfen - aktuell
     alles Default.)
   - `standard_feed()`: der proportionale `preferred_political_ratio`-Mix
     (Largest-Remainder + Interleave) - stimmen die Anteile im echten Feed mit
     der Like-Historie überein? Randfälle: nur ein gelabelter Like, exakte
     Gleichstände, ein Bucket läuft leer.
   - `diversity_aware_feed()`: ist `diversity_every` (2-6) der richtige Hebel?
     Wirkt die Diversity-Einstreuung auf dem größeren Datensatz noch, oder
     verschwindet sie zwischen zu vielen ähnlichen Posts?
   - Cold-Start: neuer Account ohne Likes, nur Onboarding-Antworten - oder
     ganz ohne Signal. Sieht der Feed dann sinnvoll aus?
   - Die Diversity-/Bubble-Scores: messen sie wirklich das, was die
     DTEW-Kritikpunkte gemeint haben, oder sind sie zu grob?
   - Determinismus/Stabilität: gleiche Eingabe -> gleiche Reihenfolge (wichtig
     für die Live-Demo). Keine ungewollte Abhängigkeit von dict-Reihenfolge.

2. **Feed-Refresh / Rotation (`app.py`: `_rotation_plan()` und Umfeld in
   `index()`, `SEEN_HISTORY_CAP`, `MIN_UNSEEN_FOR_ROTATION`, Session-Cookie)** -
   frisch in PR #148 gefixt (Rotation fror ein, sobald fast alles gesehen war),
   aber weiter härten:
   - Verhalten bei kleinem vs. großem Datensatz einmal komplett durchdenken
     und mit Tests festnageln (`tests/test_rotation.py` erweitern).
   - Session-Cookie-Größe: `SEEN_HISTORY_CAP = 60` UUIDs + andere
     Session-Keys - wie groß wird der signierte Cookie real? Nah an den 4 KB
     Browser-Limit? Ggf. auf Hashes/kürzere IDs oder serverseitige Ablage
     ausweichen.
   - Zusammenspiel mit dem "↑ New posts"-Polling und mit explizitem
     `?seed_id=` (Tab-Wechsel, Dropdown) - darf sich nicht gegenseitig
     aushebeln.
   - Fühlt sich "Reload = neue Beiträge" auf dem echten Datensatz flüssig an,
     oder springt der Feed unangenehm?

3. **Danach alles andere** (wie schon bisher, kein Einzelpunkt vorgegeben):
   Korrektheit/Bugs, Testabdeckung, UI-Politur, Accessibility, Performance,
   README-Aktualität, tote Codepfade, Konsistenz zwischen `standard_feed`/
   `diversity_aware_feed`/`/dashboard`. Was beim genauen Hinsehen als nächstes
   am meisten bringt.

Das passt bewusst zu den Dauer-Blockern der Nacht-Sessions (kein
Supabase-Zugang, kein externes Netz): Algorithmus, Rotation, Tests, UI und
Doku lassen sich alle offline mit `pytest` + Flask-Testclient verifizieren.
Supabase-/Fediverse-abhängige Schritte bleiben wie gehabt für eine Session mit
Zugangsdaten liegen (siehe "Nächste Schritte" weiter unten).

### Wann aufhören

Nicht künstlich Nacht für Nacht weiterlaufen, wenn nichts Echtes mehr
ansteht. Sobald du **ehrlich** beurteilst, dass der Prototyp korrekt, sauber
getestet, poliert und ohne sinnvoll verbleibende Verbesserung ist:

- **STOPP.** In diese Datei ganz oben einen Block `## STATUS: FERTIG (<Datum>)`
  schreiben, der begründet, warum nichts Sinnvolles mehr offen ist (was
  geprüft wurde, welche Bereiche als "gut genug" gelten).
- Keinen weiteren PR in dieser Nacht öffnen, keine kosmetischen Diffs
  erzeugen, um beschäftigt auszusehen. Lieber ein kurzer "geprüft, nichts zu
  tun"-Eintrag als erfundene Änderungen.
- Bei echten Zweifeln, ob etwas noch eine Verbesserung ist: nicht machen,
  stattdessen hier als "Kandidat, bewusst nicht umgesetzt, weil unsicher"
  notieren, damit Felix/Anton entscheiden können.

Wie gehabt: jede Session dokumentiert hier ehrlich, was geprüft und was
verändert wurde, bevor sie behauptet, etwas sei "erledigt". Merge nach `main`
bleibt bei Anton/Felix. Den Scheduled-Prompt nicht blind befolgen, wenn er
veraltet wirkt - erst Git-Log / offene PRs / diese Datei prüfen.

## Stand nach dem Lauf vom 12.09.2026 (achte Nacht-Session) - Workshop-Ende, kein neuer Substanzfund

Der scheduled-task-Prompt für diese Session war wieder derselbe massiv
veraltete Text wie in Session 6/7 (03.09.-Feedback zur Zwei-Spalten-UI,
"kein richtiger Feed", geforderter Struktur-Umbau zu Single-Feed+Tabs). Vor
dem Umsetzen wie vorgesehen zuerst Git-Log/`list_pull_requests`/diese Datei
geprüft statt blind zu folgen: exakt dasselbe Feedback ist bereits in PR #86
(04.09.) umgesetzt und seither in mindestens drei weiteren Nächten (dritte,
sechste, siebte Session, siehe oben) per Playwright-Screenshot und/oder
Code-Lesen erneut gegenverifiziert. Diese Session hat das ein weiteres Mal
mit frischem Blick geprüft statt den Notizen blind zu vertrauen (Flask-
Testclient-Smoke-Test aller Routen + Lese-Durchgang durch `ranking.py`s
beide "bewusst nicht umgesetzt"-Kandidaten aus Session 7) - kein neuer Befund,
keine Regression seit der letzten Verifikation.

**Wichtiger neuer Kontext, der in keiner vorherigen Session vorlag:** laut
[[DTEW 0912 - Freier Tag, Bremen-Exkursion und Workshop-Abschluss]] ist
Samstag 12.09. der **letzte Tag des zweiwöchigen DTEW-Zeitraums** (31.08.-
12.09.) - kein weiterer Workshop-Tag folgt. Case 3 (dieser Prototyp) wurde
laut derselben Notiz bereits am 10.09. final vorgestellt (Blogpost,
1-Minuten-Pitch, Innovation Fair, Farewell Party) - die Zielgruppe, für die
"sieht nicht wie ein echter Feed aus" ursprünglich ein Problem war (Peer-
Jury), hat den Prototyp also bereits in genau der seit dem 04.09. bestehenden
Struktur gesehen und bewertet. Ein Struktur-Umbau heute Nacht hätte keine neue
Vorführung mehr, für die er relevant wäre, und hätte nur das Risiko getragen,
sieben Nächte verifizierter Feature-/Bugfix-Arbeit (echte Accounts, Dashboard,
politische Achse, Fediverse-Vorschau, TF-IDF-Fix, Accessibility, Routentests)
grundlos zu gefährden.

**Geprüft und bewusst nicht angefasst (weiterhin "Kandidat für Team-
Entscheidung", nicht neu bewertet, da kein neuer Anlass):**
`ranking.diversity_score()` (Zeile 558, weiterhin nicht von `app.py`
importiert) und die Fallback-Tier-Reihenfolge in
`diversity_aware_feed().pick_reinforcing_post()` (Zeile 500-513, weiterhin
auf dem echten Datensatz praktisch unerreichbar) - beide bereits in Session 7
dokumentiert, keine neuen Erkenntnisse dazu.

**Verifiziert:** `pytest tests/` 88/88 grün (unverändert seit Session 6).
Flask-Testclient gegen `/`, `/?mode=standard`, `/?mode=diversity`,
`/dashboard`, `/login`, `/register` - alle 200 (ohne Supabase-Konfiguration,
leerer Katalog rendert korrekt). Kein Code geändert - reine
Verifikation/Dokumentation, deshalb kein neuer Commit auf `main`, kein
zusätzlicher PR (siehe "Wann aufhören" oben: keine kosmetischen Diffs
erzeugen, um beschäftigt auszusehen).

**Nicht Code-Arbeit, aber wichtiger als jede weitere Ranking-/UI-Politur
heute Nacht:** laut derselben Notiz ist der geleakte Supabase-Token
([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92)) seit dem
04.09. weiterhin nicht widerrufen und der Prototyp weiterhin live deployed -
sicherheitsrelevant und unabhängig vom Workshop-Ende, aber nur von einem
Menschen mit Supabase-Dashboard-Zugriff lösbar, nicht von dieser Sandbox.

**Empfehlung ans Team (keine Automations-Entscheidung, die diese Session
selbst treffen kann):** Da der Case bereits final vorgestellt wurde und keine
weitere Vorführung mehr aussteht, ist unklar, welchen Wert weitere nächtliche
Automations-Läufe an diesem Prototyp noch schaffen - siehe dieselbe
Einschätzung bereits in [[DTEW 0912 - Freier Tag, Bremen-Exkursion und
Workshop-Abschluss]] zur DTEW-Vorbereitungs-Automation. Vorschlag: der
zugehörige Scheduled Task/Trigger sollte überprüft und ggf. deaktiviert oder
zumindest der Prompt-Text aktualisiert werden, statt unverändert weiter jede
Nacht gegen denselben, seit dem 04.09. gelösten Punkt zu laufen.

## Stand nach dem Lauf vom 11.09.2026 (siebte Nacht-Session)

Der scheduled-task-Prompt für diese Session war wieder auf einem massiv
veralteten Stand - er beschrieb als "heutige Top-Priorität" nochmal das
Nutzer-Feedback vom 03.09. zur Zwei-Spalten-UI aus PR #83 ("sieht nach
Claude Design aus", "kein richtiger Feed") und forderte einen kompletten
Struktur-Umbau zu einem einzelnen scrollbaren Feed mit Tab-Umschaltung statt
zwei Spalten. Vor dem Umsetzen wie vorgesehen zuerst diese Datei geprüft:
dieses exakte Feedback ist laut den Sessions vom 03.-04.09. und mehreren
weiteren Nächten seither bereits umgesetzt (PR #86: Single-Feed + Tabs statt
Zwei-Spalten-Vergleich) und mehrfach per Playwright-Screenshot
gegenverifiziert (siehe dritte Session weiter unten) - seitdem sind sieben
weitere Nächte Feature-/Algorithmus-Arbeit auf dieser Struktur aufgebaut.
Zusätzlich hat Felix die Top-Priorität dieser Datei am 10.09. per Chat
explizit auf Algorithmus/Refresh-Überarbeitung umgestellt (`221c122`) - das
hat gegenüber dem veralteten Scheduled-Prompt Vorrang, wie die Datei selbst
verlangt. Auch der Ist-Zustand im Prompt ("main auf PR #81/#83") war
komplett veraltet: main steht inzwischen bei PR #149, mit echten Accounts,
Dashboard, politischer Achse, Fediverse-Vorschau, Bubble-Trend-Sparklines
und (aus der letzten Nacht) einem bereits offenen PR #152 zur
TF-IDF-Nachbarschaftsqualität.

**Kontinuität statt Neuanfang:** `list_pull_requests` zeigte PR #152
(`fix/ranking-tfidf-neighborhood-quality`, sechste Nacht-Session, siehe
Eintrag direkt unten) offen und ungemergt für genau diesen Ordner - laut
Kontinuitätsregel diesen Branch ausgecheckt und fortgesetzt statt neu
anzufangen, statt einen zweiten, konkurrierenden PR zu eröffnen.

**Was diese Session bearbeitet hat:** die sechste Session hatte in ihren
"Nächsten Schritten" (Punkt 6) selbst vorgeschlagen, dass ein Folgelauf sich
stärker auf Priorität 3 der Team-Anweisung ("alles andere") konzentrieren
kann, da 1 (Ranking) und 2 (Rotation) bereits mit konkretem Fund/Fix bzw.
sauberer Verifikation bearbeitet waren. Diesem Vorschlag gefolgt und
`templates/index.html`/`dashboard.html` gezielt auf Accessibility geprüft
(nicht kosmetisch, sondern konkrete fehlende ARIA-Semantik):

- Aktiver Feed-Modus-/Dashboard-Scope-Tab hatte keine `aria-current="page"`
  Markierung - nur visuell per CSS-Klasse unterscheidbar, für
  Screenreader-Nutzer:innen nicht erkennbar, welcher Tab aktiv ist. Ergänzt
  in beiden Templates.
- Like-Button hatte weder `aria-pressed` noch ein beschreibendes
  `aria-label` - nur ein Herz-Icon-Glyph, dessen gefüllt/leer-Zustand für
  Screenreader unsichtbar ist. Ergänzt (`aria-pressed`, `aria-label` inkl.
  aktueller Like-Zahl), inklusive Client-JS-Sync in `toggleLike()` nach dem
  Fetch-Response.
- `comments-toggle`-Button hatte kein `aria-expanded` - Screenreader können
  den Auf-/Zu-Zustand des Kommentarbereichs nicht ansagen. Ergänzt
  (statisch `false` initial, per JS in `toggleComments()` synchron
  gehalten), plus `aria-live="polite"` auf `.comments-list`, damit
  geladene/gelöschte Kommentare angesagt werden.
- Das "↑ New posts"-Banner wird nur visuell eingeblendet (`hidden`-Attribut
  entfernt) - ohne eigene Live-Region wird das für Screenreader-Nutzer:innen
  nicht angesagt, da `[hidden]`-Elemente beim Laden nicht im Accessibility
  Tree stehen. Neue eigenständige `#live-status`-Region (`sr-only`,
  `role="status"`, `aria-live="polite"`) ergänzt, die `pollForNewPosts()`
  zusätzlich zum sichtbaren Banner befüllt.

**Testabdeckungslücke geschlossen, die über alle bisherigen Sessions
bestand:** kein Testfile deckte `app.py`s eigentliche Flask-Routen ab -
`tests/test_ranking.py`/`test_rotation.py`/`test_fediverse.py` testen nur
die reinen Funktionsbausteine, jede Session vorher hat `/`, `/dashboard`,
`/login`, `/register` etc. nur manuell per Flask-Testclient gegengeprüft
und dann verworfen (siehe "Verifiziert"-Absätze aller bisherigen Sessions
oben). Neue `tests/test_app.py` (13 Tests) mit gemocktem `db`/`fediverse`-
Modul: beide Feed-Modi, leerer Post-Katalog, `/dashboard` gesperrt/nicht
konfiguriert, `/login`/`/register`-Rendering, `/posts/latest-id`, Login-
Pflicht auf Like/Kommentar-Endpunkten (401 ohne Session) - plus gezielte
Assertions auf die oben ergänzten ARIA-Attribute, damit ein künftiger
Regressions-Fund nicht wieder nur manuell auffällt.

**Verifiziert:** `pytest tests/` 83/83 grün (70 vorher + 13 neue Tests in
`test_app.py`). Zusätzlich `python3 app.py` tatsächlich gestartet (nicht nur
Testclient) und alle Kern-Routen mit `curl` gegengeprüft (`/?mode=standard`,
`/?mode=diversity`, `/dashboard`, `/login`, `/register` - alle 200, ohne
Supabase-Konfiguration zeigt der Feed korrekt den leeren Zustand statt
abzustürzen). `code-review`-Skill auf den vollen Diff (Templates + neue
Testdatei) angewendet: keine Befunde. `security-review`-Skill ebenfalls
angewendet (sowohl auf den bereits vorhandenen PR-Diff von der sechsten
Session als auch separat auf die neuen Accessibility-/Test-Änderungen
dieser Session): keine hochsicheren Befunde - reine ARIA-Attribut-Ergänzung
und ein neues, rein lesendes Test-File ohne neuen Nutzereingabe-Pfad, keine
Änderung an Jinja-Autoescaping, kein `| safe`.

**Weiterhin dieselben zwei Blocker** (keine Supabase-Zugangsdaten, kein
Internetzugriff zu externen Domains - erneut geprüft: `env | grep -i
supabase` leer, `curl https://mastodon.social/` liefert `000`/keine
Verbindung). Unverändert offen für eine Session mit Zugangsdaten/
Netzwerkzugriff, siehe "Nächste Schritte" unten.

**Kein STATUS: FERTIG-Block** - `/dashboard`s `political_label_ratio`-Frage
(Kandidat aus der sechsten Session) ist weiterhin eine offene
Team-Entscheidung, und ein AT-Praxistest der heute ergänzten ARIA-Attribute
mit einem echten Screenreader (z.B. NVDA/VoiceOver) steht noch aus - diese
Sandbox kann das nicht selbst verifizieren, nur die Attribute selbst und
ihre JS-Synchronisierung testen.

## Nächste Schritte (Priorität absteigend, ersetzt die Fassung der sechsten Session weiter unten)

1. **Sobald Supabase-Zugangsdaten verfügbar sind:** unverändert offen -
   `0003_political_label.sql`, `0006_more_categories.sql`,
   `0007_english_content.sql`, `0010_political_label_english.sql` in
   Dateinamen-Reihenfolge anwenden (`apply_schema.py`), danach
   `seed_demo_accounts.py` laufen lassen.
2. **Fediverse-Anbindung live verifizieren**, sobald normaler
   Internetzugriff verfügbar ist.
3. **Deployment tatsächlich durchführen** (`deploy/README.md`), sobald
   jemand mit VM-Zugriff Zeit hat.
4. **Die heute ergänzten ARIA-Attribute mit einem echten Screenreader
   gegenprüfen** (NVDA/VoiceOver/JAWS) - diese Sandbox kann nur die
   Attribute selbst und ihre JS-Synchronisierung testen, nicht das
   tatsächliche Vorlese-Erlebnis.
5. **`/dashboard` optional um `political_label_ratio` erweitern** (aus der
   sechsten Session, weiterhin offene Design-/Team-Entscheidung).
6. Politisches Label als optionales statt Pflichtfeld - weiterhin keine
   Team-Entscheidung bekannt, nicht umgesetzt.
7. Falls es noch offene PRs für diesen Ordner gibt, wenn der nächste Lauf
   startet: gegen den dann aktuellen main-Stand prüfen/rebasen, bevor
   inhaltlich weitergearbeitet wird (Merge bleibt bei Anton/Felix). Stand
   dieser Session: PR #152 ist der einzige offene PR für
   `Code/feed-diversity-prototype/` und wurde in dieser Session direkt
   fortgesetzt (siehe oben) statt einen zweiten zu eröffnen.
8. Sollte kein neuer Anhaltspunkt fürs Ranking/Rotation vorliegen, bleibt
   Priorität 3 ("alles andere") der sinnvollste nächste Fokus - z.B.
   weitere Testabdeckung für `create_post`/`toggle_like`/Kommentar-Routen
   mit eingeloggter Session (diese Session hat nur den "nicht eingeloggt"-
   Fall dieser Endpunkte getestet), oder ein zweiter Blick auf
   `register.html`/`login.html` auf dieselbe Art fehlender ARIA-Semantik.

## Was in dieser Session NICHT versucht wurde (mit Absicht)

- Keine Supabase-Migrationen/Seed-Skripte ohne Zugangsdaten ausgeführt
- Kein Login/SSH/Deployment auf die Team-VM
- Kein Merge des PRs nach `main` (bleibt bei Anton/Felix)
- Kein weiterer Struktur-Umbau des Feeds trotz veraltetem Prompt - siehe
  Begründung oben, wäre ein Rückschritt ohne aktuellen Anlass gewesen
- Kein `/dashboard`-Ratio-Feature - weiterhin eine Design-Entscheidung, kein
  klarer Bugfix (siehe sechste Session)
- Keine visuelle/Layout-Änderung an Feed/Karten - nur ARIA-Attribute und
  ihre JS-Synchronisierung, keine CSS-/Struktur-Änderung

## Stand nach dem Lauf vom 10.09.2026 (sechste Nacht-Session)

Der scheduled-task-Prompt für diese Session war wieder auf einem veralteten
Stand (verlangte als Top-Priorität nochmal visuelles Redesign, politische
Einordnung als neue Dimension, Beispiel-Accounts, Fediverse-Recherche,
Marketing und Deployment-Vorbereitung - alles laut Git-Log/dieser Datei
längst umgesetzt: Redesign mehrfach verifiziert, politisches Label mit
proportionalem Ratio-Mix seit dem Team-Feedback vom 10.09. vormittags,
`seed_demo_accounts.py` mit `DEMO_ACCOUNTS`, `fediverse.py` plus
Machbarkeitsnotiz im Vault, `deploy/`-Ordner mit systemd/Caddy). Vor dem
Umsetzen wie vorgesehen zuerst diese Datei geprüft: die Team-Anweisung vom
10.09. (per Chat, direkt von Felix committet in `221c122`, nicht aus einer
Nacht-Session) ersetzt die Top-Priorität explizit durch den
Algorithmus/Refresh-Auftrag oben - dieser Datei-Anweisung Vorrang gegeben,
wie sie selbst verlangt.

**Priorität 1 (`ranking.py`) bearbeitet - konkreter Fund:** den echten
~250-Posts-Datensatz (`seed_demo_accounts.py` + `seed_more_posts.py` +
`seed_more_posts_v2.py`) offline durch `standard_feed()`/
`diversity_aware_feed()` laufen lassen (kein Supabase nötig, reine
Post-Objekte). Ergebnis bestätigt genau den in der Team-Anweisung
vermuteten Verdacht: der bisherige, ungewichtete TF-IDF-Vektorisierer
(Standardeinstellungen, keine Stoppwörter, keine n-Gramme, Titel nur
einmal im Text) lieferte auf diesem Datensatz erkennbar schlechte
Nachbarschaften - für den Seed-Post "Speed up wind power expansion"
(climate) rangierte ein völlig themenfremder Migrations-Post ("Speed up
procedures without cutting legal protection") vor anderen echten
Klima-Posts, einzig weil beide zufällig das Wort "speed" teilen. Behoben in
`ranking.py`: neue `_post_text()` (Titel doppelt gezählt) und
`_tfidf_matrix()` (`stop_words="english"`, `ngram_range=(1, 2)`, mit
Fallback auf einen ungetunten Vektorisierer, falls die Einstellungen bei
nutzergeneriertem Text mal ein leeres Vokabular ergeben sollten - reiner
Stoppwort-Text ist mit echten Post-Titeln unrealistisch, aber die Route
darf trotzdem nie mit 500 abstürzen). Am selben Datensatz vorher/nachher
gegengeprüft: die Top-3-Treffer für den Klima-Seed sind jetzt durchgehend
Klima-Posts statt einer themenfremden Beimischung. Regressionstest
`test_similarity_ranking_prefers_genuine_topic_match_over_a_shared_incidental_word`
in `tests/test_ranking.py` hält das mit einem kleinen, eigenständigen
Fixture fest (nicht abhängig von den Seed-Dateien, damit der Test nicht
zerbricht, sobald jemand den Seed-Datensatz ändert).

**Übrige Punkte aus der Prioritätenliste geprüft, nichts Weiteres zu
reparieren gefunden** (jeweils am echten 250-Posts-Datensatz, nicht nur an
den kleinen Test-Fixtures):
- `standard_feed()`s proportionaler `preferred_political_ratio`-Mix: Tests
  für Einzel-Like, exakte Gleichstände (`recent_window=0`-Tests) und
  leerlaufende Buckets (Fallback-Tiers in `standard_feed()`) existieren
  bereits und sind korrekt.
- `diversity_every` wirkt auf dem großen Datensatz weiterhin sichtbar (jede
  n-te Position tatsächlich ein `is_diverse_pick`), keine Verwässerung
  durch die Datensatzgröße.
- Cold-Start (kein Account, kein Like, kein `political_label` am Seed-Post
  selbst) stürzt nicht ab und liefert eine sinnvolle Reihenfolge - neuer
  Test `test_standard_feed_with_zero_signal_and_no_labels_does_not_crash_and_stays_sane`.
- Determinismus: `standard_feed()`/`diversity_aware_feed()` liefern bei
  gleicher Eingabe fünfmal hintereinander exakt dieselbe Reihenfolge (am
  echten Datensatz manuell geprüft, zusätzlich zwei neue Regressionstests
  `test_standard_feed_is_deterministic_across_repeated_calls`/
  `test_diversity_aware_feed_is_deterministic_across_repeated_calls`, da
  vorher kein Test das explizit festgehalten hatte).

**Priorität 2 (`app.py`: `_rotation_plan()`/Refresh) geprüft, ein
Test-Lücke geschlossen, sonst nichts zu reparieren gefunden:**
- Kleiner-Datensatz-Fall (Gesamtkatalog kleiner als
  `MIN_UNSEEN_FOR_ROTATION`) war bisher nicht direkt getestet - neuer Test
  `test_small_catalogue_below_the_rotation_floor_disables_rotation_gracefully`
  bestätigt: Rotation schaltet sauber ab (`rotation_active=False`,
  `exclude_ids=None`) statt versehentlich den gesamten Kandidatenpool
  auszuschließen.
- Session-Cookie-Größe nachgerechnet (nicht nur geschätzt): ein signierter
  Cookie mit `SEEN_HISTORY_CAP=60` UUIDs plus den übrigen Session-Keys
  (user_id, display_name, handle) liegt bei ca. 2 KB - deutlich unter dem
  4-KB-Browser-Limit, aktuell kein Handlungsbedarf.
- "↑ New posts"-Banner (`templates/index.html`, `pollForNewPosts()`) nutzt
  `window.location.reload()` - das erhält ein eventuell in der URL
  stehendes `?seed_id=` automatisch, kann also nicht mit einem expliziten
  Seed-Pin kollidieren. Kein Bug gefunden.
- `tests/test_rotation.py` deckte den Großdatensatz-/Wrap-around-Fall
  bereits ausführlich ab (`test_repeated_reloads_keep_advancing...`).

**Priorität 3 (alles andere) - zwei kleinere Prüfungen, nichts Konkretes
gefunden:**
- Performance: `standard_feed()` auf dem vollen 250-Posts-Datensatz braucht
  im Schnitt ~12 ms pro Aufruf (20 Wiederholungen gemessen) - kein Problem.
- Toter Code: Sub-Agent-Durchlauf über `app.py`/`ranking.py`/`db.py`/
  `fediverse.py` (jede Funktion/Konstante gegen Referenzen im ganzen
  Ordner geprüft, inkl. Templates/Tests) - nichts Totes gefunden, jede
  Funktion hat mindestens eine echte Aufrufstelle außerhalb ihrer eigenen
  Definition.
- `/dashboard` nutzt für die Account-Übersicht weiterhin nur
  `political_label` (Sieger-Label), nicht `political_label_ratio` - anders
  als der Standard-Feed, der seit heute Vormittag proportional mischt.
  **Bewusst nicht umgesetzt:** eine UI-Änderung an `dashboard.html`, um
  auch dort den Ratio anzuzeigen, wäre selbst eine Design-Entscheidung
  (wie soll ein 60/40-Split in der Tabelle aussehen?) und war nicht
  Teil des heutigen Auftrags - als Kandidat für einen künftigen Lauf oder
  eine Team-Entscheidung hier vermerkt statt eigenmächtig entschieden.

**Verifiziert:** `pytest tests/` 70/70 grün (65 vorher + 5 neue Tests).
Zusätzlich Flask-Testclient mit dem kompletten echten 250-Posts-Datensatz
(nicht nur gemockten Test-Fixtures) gegen `/`, `/?mode=diversity`,
`/?mode=standard&mix=2`, `/login`, `/register` - alle 200, Feed rendert
mit echten Posts. Diff ist rein auf `ranking.py`/Tests/README beschränkt
(keine neuen Nutzereingabe-Pfade, kein `| safe`, keine SQL-Änderung) -
kein separater `security-review`-Sub-Agent-Lauf für diese eng begrenzte
Änderung als nötig eingeschätzt, manuell gegengeprüft.

**Weiterhin dieselben zwei Blocker wie in allen bisherigen Sessions**
(keine Supabase-Zugangsdaten, kein Internetzugriff zu externen Domains) -
unverändert geprüft (`env | grep -i supabase` leer). Priorität 1
(Migrationen/Seed-Skript gegen die echte Instanz) und die
Fediverse-Live-Verifikation aus früheren Läufen bleiben deshalb weiterhin
offen für eine Session mit Zugangsdaten/Netzwerkzugriff - siehe "Nächste
Schritte" unten, unverändert gegenüber der letzten Fassung.

**Kein STATUS: FERTIG-Block** - es gibt weiterhin sinnvolle offene Punkte
(siehe "Nächste Schritte"), auch wenn diese Session die beiden
Top-Prioritäten aus der Team-Anweisung ernsthaft bearbeitet und dabei
einen echten, demo-relevanten Bug gefunden und behoben hat, statt nur
oberflächlich "geprüft" zu haben.

## Nächste Schritte (Priorität absteigend, ersetzt die Fassung der fünften Session weiter unten)

1. **Sobald Supabase-Zugangsdaten verfügbar sind:** unverändert offen -
   `0003_political_label.sql`, `0006_more_categories.sql`,
   `0007_english_content.sql`, `0010_political_label_english.sql` in
   Dateinamen-Reihenfolge anwenden (`apply_schema.py`), danach
   `seed_demo_accounts.py` laufen lassen. Siehe README "Current status"
   für den genauen Stand, welche Migrationen laut Git-Historie schon gegen
   die echte Instanz gelaufen sind.
2. **Fediverse-Anbindung live verifizieren**, sobald normaler
   Internetzugriff verfügbar ist - weiterhin nie gegen die echte
   Mastodon-API getestet.
3. **Deployment tatsächlich durchführen** (`deploy/README.md`), sobald
   jemand mit VM-Zugriff Zeit hat.
4. **`/dashboard` optional um `political_label_ratio` erweitern** (siehe
   oben, "bewusst nicht umgesetzt") - nur falls das Team eine
   Ratio-Anzeige in der Account-Übersicht tatsächlich will, sonst
   überflüssige UI-Änderung.
5. Politisches Label als optionales statt Pflichtfeld - weiterhin keine
   Team-Entscheidung bekannt, nicht umgesetzt.
6. Sollte der Algorithmus-/Refresh-Auftrag aus der Team-Anweisung oben nach
   dieser Session als "gründlich genug durchgesehen" gelten (diese Session
   hat beide Punkte 1 und 2 der Anweisung mit konkretem Fund/Fix bzw.
   sauberer Verifikation bearbeitet): der nächste Lauf kann sich stärker
   auf Punkt 3 der Team-Anweisung ("alles andere") konzentrieren -
   Accessibility/UX-Feinschliff, weitere Testabdeckung abseits von
   Ranking/Rotation, README-Aktualität an anderen Stellen. Falls Felix/
   Anton das anders sehen (z.B. noch mehr am Algorithmus vermuten): bitte
   hier oder per Chat präzisieren, wonach genau noch gesucht werden soll -
   ein weiterer "nochmal alles kritisch durchgehen"-Durchlauf ohne neuen
   Anhaltspunkt würde vermutlich nur denselben Stand wie heute
   reproduzieren.
7. Falls es noch offene PRs für diesen Ordner gibt, wenn der nächste Lauf
   startet: gegen den dann aktuellen main-Stand prüfen/rebasen, bevor
   inhaltlich weitergearbeitet wird (Merge bleibt bei Anton/Felix). Stand
   dieser Session: kein offener PR für `Code/feed-diversity-prototype/`
   (per `list_pull_requests` geprüft, die beiden offenen PRs #150/#151
   betreffen nur Vault-Notizen zum DTEW-Workshop).

## Was in dieser Session NICHT versucht wurde (mit Absicht)

- Keine Supabase-Migrationen/Seed-Skripte ohne Zugangsdaten ausgeführt
- Kein Login/SSH/Deployment auf die Team-VM
- Kein Merge irgendeines PRs nach `main`
- Keine UI-Änderung an `dashboard.html` für die Ratio-Anzeige (siehe oben,
  Design-Entscheidung statt klarer Bugfix)
- Kein erneuter kompletter Struktur-Umbau des Feeds trotz Prompt-Forderung
  ("visuelles Redesign") - laut Git-Log/dieser Datei mehrfach bereits
  umgesetzt und verifiziert, siehe Begründung oben

## Stand nach dem Lauf vom 11.09.2026 (sechste Nacht-Session, dritte auf PR #152)

**Erst mal ein Lücke in der eigenen Doku-Kette festgestellt, bevor inhaltlich
weitergearbeitet wurde:** diese Datei war stehengeblieben auf dem Stand nach
PR #148 (fünfte Session, siehe Eintrag unten), obwohl `main` seitdem sieben
weitere gemergte Commits hat (#153/#155-160 - Reload-/Rotations-Fixes,
Diversity-Slot-Themenrotation, Ausschluss gelikter Posts, Mobile-Lesbarkeit,
Sign-up-Umfrage sichtbar), alle laut Commit-Botschaften live mit Anton beim
DTEW-Stand entstanden, nicht ueber diese Nacht-Routine - deshalb ohne Eintrag
hier. Zusaetzlich lag bereits ein offener PR #152
(`fix/ranking-tfidf-neighborhood-quality`) mit zwei eigenen, in der PR-
Beschreibung dokumentierten Naechten (10.09. TF-IDF-Nachbarschafts-Fix aus
der Team-Prioritaet-1-Anweisung, 11.09. Accessibility-Pass + erste
Route-Test-Datei `tests/test_app.py`) - laut Kontinuitaets-Regel an dieser
Stelle fortgesetzt statt neu angefangen. Main mit dem PR-Branch verglichen:
keine inhaltliche Ueberschneidung mit den sieben live-Fixes, PR #152 war
laut eigenem Kommentar dort bereits per Merge auf dem aktuellen main-Stand
(nur zwei danach dazugekommene, hier irrelevante Vault-Commits fehlten,
keine Konflikte).

**Frischer, kritischer Blick auf `ranking.py`/`app.py` (Team-Prioritaet 1/2),
zwei konkrete Bugs gefunden und mit Regressionstest behoben:**

1. `standard_feed()`s `preferred_political_ratio`-Zweig (genau der von Felix
   genannte Randfall "ein Bucket laeuft leer"): wenn ein Label laut Ratio
   mehr Slots bekommen sollte als tatsaechlich Kandidaten mit diesem Label
   existieren, brach die Slot-Vergabe vorzeitig ab - die beiden
   Fallback-Stufen danach (`no_signal`/`other_political`) greifen aber nur
   fuer Posts, deren Label *nicht* Teil der Ratio ist, koennen also nicht
   mit ueberschuessigen Posts eines anderen, noch nicht ausgeschoepften
   Ratio-Labels auffuellen. Ergebnis: der Feed kam kuerzer zurueck als
   `limit`, obwohl reichlich passende Kandidaten des anderen Labels
   uebrig waren. Reproduziert (3 "left"-Posts, 20 "right"-Posts, ratio
   60/40, limit 8 -> Feed hatte nur 6 statt 8 Eintraege), gefixt durch
   einen Auffuell-Schritt, der vor den beiden alten Fallback-Stufen aus
   verbleibenden Kandidaten *irgendeines* Ratio-Labels nach Similarity
   auffuellt. Neuer Test
   `test_standard_feed_ratio_tops_up_from_a_surplus_label_when_one_bucket_runs_dry`.
   Auf dem echten ~250-Post-Datensatz mit nur zwei/drei Labels und vielen
   Posts pro Topic vermutlich selten sichtbar, aber genau der Randfall, den
   die Team-Anweisung explizit zum Pruefen nannte - und mit kleinerem
   Datensatz (z.B. neues Thema mit wenigen Posts) real.
2. `app.py:index()` rief `db.fetch_liked_post_ids()` zweimal pro Request auf:
   einmal fuer den gesamten Post-Katalog (um bereits gelikte Posts aus dem
   Kandidatenpool zu nehmen), einmal zusaetzlich nur fuer die im Feed
   gezeigten Posts, nur um `item["liked"]` zu setzen - obwohl die zweite
   Menge immer eine Teilmenge der ersten ist. Ein unnoetiger
   Supabase-Roundtrip bei jedem einzelnen Seitenaufruf fuer eingeloggte
   Accounts. Gefixt: die zweite Abfrage entfernt, `item["liked"]` prueft
   jetzt gegen das bereits vorhandene `liked_post_ids`. Neuer Test
   `test_index_fetches_liked_post_ids_only_once_per_request` (zaehlt Calls
   ueber ein Monkeypatch).

**Zusaetzlich unabhaengig nachgerechnet statt nur der PR-152-Behauptung
vertraut:** Session-Cookie-Groesse (von Felix explizit als Sorge genannt,
`SEEN_HISTORY_CAP=60` UUIDs plus restliche Session-Keys) mit
`itsdangerous`/Flasks eigenem Signing-Serializer nachgebaut - 60 UUIDs plus
realistisch lange Anzeigename/Handle-Werte ergeben rund 2 KB signierten
Cookie-Wert, deutlich unter dem gaengigen 4-KB-Browser-Limit. Kein
Handlungsbedarf, aber jetzt tatsaechlich nachgemessen statt nur behauptet.

**Kandidaten gesehen, bewusst NICHT umgesetzt (Unsicherheit):**
- `ranking.diversity_score()` (die einfache Convenience-Wrapper-Funktion,
  nicht `diversity_score_for_perspective()`/`_for_political_label()`) wird
  von `app.py` nirgends importiert/aufgerufen - toter Code in Produktion,
  nur noch von den eigenen Unit-Tests genutzt. Der Docstring beschreibt sie
  aber ausdruecklich als bewusst behaltene Convenience-API "fuer Aufrufer,
  die keinen Account-weiten bias_perspective mitfuehren" - koennte
  absichtlich fuer einen noch nicht existierenden Aufrufer bereitstehen.
  Nicht geloescht, da unklar ob das eine bewusste API-Entscheidung oder
  schlicht Restcode ist - Felix/Anton koennen das besser einschaetzen.
- `diversity_aware_feed()`s `pick_reinforcing_post()` probiert im
  `bias_political`-Zweig als zweite Fallback-Stufe "irgendein Post aus
  einem anderen Topic" *vor* den spezifischeren Stufen 3-5 (gleiches Topic,
  aber nur teilweise passend). Wirkt auf den ersten Blick rueckwaerts,
  ist aber auf dem echten ~250-Post/12-Topic-Datensatz praktisch nie
  erreichbar bevor Stufe 2 schon einen Treffer liefert (12 Topics geben
  reichlich "anderes Topic"-Auswahl) - vermutlich harmlos in der Praxis.
  Ohne konkret gemeldetes Problem nicht umgebaut, um kein Verhalten ohne
  Anlass zu aendern - als Beobachtung hier notiert statt stillschweigend
  ignoriert.

**Verifiziert:** `pytest tests/` 88/88 gruen (86 vorher + 2 neue Tests).
Kein neuer Nutzereingabe-Pfad (reine Algorithmus-Logik auf bereits
validierten `Post`-Objekten, und eine entfernte statt hinzugefuegte
DB-Abfrage) - keine Security-Review-relevante Aenderung.

**Weiterhin dieselben Blocker wie in jeder bisherigen Session:**
`env | grep -i supabase` liefert nichts, kein Internetzugriff zu externen
Domains. PR #152 bleibt offen, wartet weiterhin auf Anton/Felix (keine
Review-Aktivitaet). Kein Merge (bleibt bei Anton/Felix), kein PR-Split -
die zwei Fixes dieser Nacht auf denselben Branch/PR #152 gepusht, da
inhaltlich zur selben "Algorithmus/Refresh-Ueberarbeitung"-Prioritaet
gehoerend und PR #152 laut Kontinuitaets-Regel weiterhin der richtige Ort
dafuer ist.

## Naechste Schritte (Prioritaet absteigend)

1. **Sobald jemand mit Repo-Schreibrecht Zeit hat:** PR #152 reviewen/mergen
   - inhaltlich jetzt drei Naechte Arbeit (TF-IDF-Fix, Accessibility +
     Routen-Tests, die zwei Bugfixes oben), alles gruen getestet, aber ohne
     jede Review-Aktivitaet seit Erstellung am 10.09.
2. Die zwei oben genannten Kandidaten (`diversity_score()` toter Code,
   `pick_reinforcing_post()`-Stufenreihenfolge) sind bewusst unangetastet -
   falls das Team eine Meinung dazu hat, bitte hier oder im PR vermerken.
3. Sobald Supabase-Zugangsdaten/Netzwerkzugriff verfuegbar sind: die in
   fruaheren Eintraegen genannten Schritte (Migrationen anwenden,
   Seed-Skripte laufen lassen, Fediverse live verifizieren) bleiben
   unveraendert offen - siehe die aelteren Eintraege unten fuer die
   vollstaendige Liste.
4. Falls Prioritaet 1/2 (Algorithmus/Refresh) beim naechsten Blick weiterhin
   sauber wirken: mit Prioritaet 3 ("alles andere") weitermachen, aber mit
   frischem Blick pruefen statt die bereits als erledigt dokumentierten
   Punkte (Redesign, politische Einordnung, Beispiel-Accounts, Fediverse-
   Recherche, Deployment-Vorbereitung - alle laut README bereits umgesetzt)
   nochmal anzufassen ohne neuen Anlass.

## Stand nach dem Lauf vom 09.09.2026 (fünfte Nacht-Session, Nacht auf 10.09.)

Der scheduled-task-Prompt für diese Session war wieder auf einem veralteten
Stand: er beschrieb als "heutige Top-Priorität" nochmal den kompletten
Struktur-Umbau der Zwei-Spalten-UI aus PR #83 ("sieht nach Claude Design
aus"). Wie in der dritten Session dokumentiert ist dieses Feedback längst
mehrfach umgesetzt und per Screenshot verifiziert - vor dem Umsetzen erneut
per Git-Log/`list_pull_requests`/`NIGHTLY_TASK.md` geprüft statt den Prompt
blind zu befolgen. Zusätzlich war die Prompt-Beschreibung des Ist-Zustands
("PR #81/#83 gemergt, zwei Spalten") komplett veraltet: der Prototyp hat
inzwischen echte Accounts (Supabase Auth), Dashboard, Registrierungs-Kompass,
politische Achse, Fediverse-Vorschau, Bubble-Trend-Sparklines - fünf weitere
Nächte Arbeit seit PR #86. Ein erneuter Struktur-Umbau hätte das ohne
aktuellen Anlass riskiert.

**Stattdessen den offenen, ungemergten PR #140 fortgesetzt** (bereits vorhanden,
Branch `code/feed-diversity-english-switch`, Priorität-1-Anweisung "komplett
auf Englisch umstellen" aus diesem Dokument) statt neu anzufangen - wie von
der Kontinuitäts-Regel vorgesehen. Frische Code-Review (`code-review`-Skill,
Diff `origin/main...HEAD`) auf den gesamten PR-Diff angewendet, nicht nur auf
eigene Änderungen, da der PR bisher nur manuell/selbst verifiziert war:

**Ein konkreter, bisher unbemerkter Rest-Bug gefunden und behoben:**
`db.py` enthielt fünf deutsche Fallback-Strings, die die Englisch-Umstellung
übersehen hatte, weil sie nicht in der ursprünglichen Grep-Suche nach
Themen-/Label-Wörtern auffielen: `"Anonym"`/`"@anonym"` (zweimal, Zeilen
269-270 und 275-276, für Posts ohne Profil-Namen/Handle), `"sonstiges"`
(Zeile 285, Fallback-Themenname für Posts ohne Kategorie) und
`"Unbekannt"`/`"@unbekannt"` (Zeile 528, Fallback für Kommentar-Autor:innen
ohne Profil). Diese Codepfade greifen nur, wenn ein Profil/eine Kategorie in
Supabase fehlt - bei den bisherigen `pytest`/Testclient-Verifikationen (die
immer vollständige Mock-Daten mitgeben) nie getriggert, hätten aber auf der
echten Instanz bei unvollständigen Profildaten deutschen Text mitten in der
sonst komplett englischen UI gezeigt. Alle fünf auf Englisch umgestellt
(`"Anonymous"`/`"@anonymous"`, `"other"`, `"Unknown"`/`"@unknown"`). Zusätzlich
zwei kleinere Fundstellen in reinen Dev-Kommentaren behoben (ein
CSS-Beispieltext in `style.css` und eine Docstring-Formulierung in `app.py`,
zweimal), auf die die ursprüngliche Grep-Suche nicht angesetzt hatte (Wörter
ohne Umlaute).

**Verifiziert:** `pytest tests/` weiterhin 48/48 grün nach allen Änderungen.
Zusätzlich neu (bisherige Sessions hatten das nur ad hoc gemacht, nicht als
wiederholbares Skript): Flask-Testclient mit gemockter `db`-Schicht gegen
`/`, `/?mode=standard`, `/?mode=diversity`, `/login`, `/register` - alle 200,
beide Feed-Modi zeigen die gemockten Posts korrekt, kein `lang="de"` mehr in
irgendeiner Antwort. `security-review`-Skill auf denselben Diff angewendet
(Sub-Agent-Analyse): keine neuen Befunde - reine String-Übersetzung ohne
Logik-Änderung, kein `| safe`/`autoescape false` hinzugekommen, neue
SQL-Migration `0007` bleibt statisch ohne Nutzereingaben.

**Weiterhin dieselben zwei Blocker wie in allen bisherigen Sessions** (keine
Supabase-Zugangsdaten, kein Internetzugriff zu externen Domains, beide
erneut per `env | grep -i supabase` und `curl` gegen `mastodon.social`
gegengeprüft: `403`/`CONNECT tunnel failed`) - Priorität 1 (Migrationen
anwenden/Seed-Skript laufen lassen) und Priorität 3 (Fediverse live
verifizieren) aus PR #140 bleiben deshalb offen für eine Session mit
Zugangsdaten/Netzwerkzugriff.

**Nicht in dieser Session gemacht:** der in der Top-Priorität des
scheduled-Prompts geforderte Struktur-Neubau des Feeds - siehe Begründung
oben. Kein Merge von PR #140 (Merge bleibt bei Anton/Felix). PR #139/#138
(DTEW-Vorbereitungsnotiz bzw. Vault-Sync) nicht angefasst, betreffen nicht
diesen Ordner.

## Stand nach dem Lauf vom 09.09.2026 (vierte Nacht-Session)

Diese Session hat die beiden Team-Anweisungen oben zum ersten Mal gesehen
(sie waren am Anfang dieser Datei bereits vorhanden, vermutlich per Chat
nachgetragen) und Priorität 1 (Englisch-Umstellung) bearbeitet, da sie
explizit "vor allem anderen in dieser Datei Gelisteten" einzuordnen ist.

**Migrations-Ansatz-Entscheidung (wie in Punkt 1 oben gefordert, hier
dokumentiert statt stillschweigend gewählt):** UPDATE statt Neu-Migration.
Begründung: `0001_init.sql`s vier Default-Kategorien und acht Autoren sind
laut README/Git-Historie bereits gegen die echte Supabase-Instanz
angewendet. Eine neue Migration mit frischen englischen Zeilen hätte
`categories.id`/`authors.id` geändert (neue UUIDs), was jeden bereits
existierenden Post mit `category_id`/`author_id` auf die alte deutsche Zeile
verwaist hätte (nicht relevant heute, da noch keine echten Posts existieren,
siehe unten - aber relevant, sobald jemand mit Zugangsdaten testet, bevor
diese Migration angewendet wird). Ein einfaches `UPDATE ... SET name = ...`
auf die bestehenden Zeilen behält die IDs und damit alle Verknüpfungen bei
und ist die deutlich simplere Änderung. Umgesetzt in neuer
`supabase/migrations/0007_english_content.sql` (idempotent, mehrfach
anwendbar, siehe Kommentar dort für die volle Begründung). Die 0001/0002
Migrationsdateien selbst wurden NICHT rückwirkend editiert (das würde die
historische Aufzeichnung dessen verfälschen, was beim ersten Lauf tatsächlich
passiert ist) - nur 0007 als additive Korrektur. Die noch unangewendeten
Migrationen 0003 (political_label-Check-Constraint), 0004 (onboarding
political label) und 0006 (acht weitere Kategorien) wurden dagegen direkt
mit den neuen englischen Werten editiert, da sie noch nie gegen die echte
Instanz gelaufen sind - dort war kein Rename-Migrationsschritt nötig.

**Umgesetzt:**
- `app.py`: `DEFAULT_TOPICS`, `KNOWN_POLITICAL_LABELS`, `ONBOARDING_QUESTIONS`,
  `COMPASS_QUESTIONS`, `TOPIC_STANCES`, `TIME_LABELS`, alle Fehlermeldungen
  (`register()`/`login()`/JSON-Endpunkte), `_feed_item_reason()` - komplett
  Englisch. Themen-Keys: `klima→climate`, `verkehr→transport`,
  `wirtschaft→economy`, `digital` unverändert (gleiches Wort), plus die acht
  neuen Themen `education/health/migration/housing/security/welfare/europe/
  foreign_policy`. Politische Labels: `links→left`, `mitte→center`,
  `rechts→right`.
- `templates/index.html`, `register.html`, `login.html`, `dashboard.html`:
  alle sichtbaren Strings, `lang="de"→"en"`, JS-Strings (Kommentar-UI,
  Kompass-Berechnung inkl. `direction`-Werten `rechts/links/konservativ/
  progressiv→right/left/conservative/progressive`), CSS-Klassennamen
  `compass-segment.links/mitte/rechts→left/center/right`.
- `static/style.css`: CSS-Variablen `--links/--mitte/--rechts→--left/--center/
  --right` (plus `-bg`-Varianten), Klassenselektoren, Kommentare.
- `fediverse.py`: `TOPIC_HASHTAGS`-Keys auf die neuen Themen-Keys umgestellt,
  Hashtag-Werte auf Englisch (z.B. `klimapolitik→climatepolicy`), Fallback
  `"unbekannt"→"unknown"`.
- `ranking.py`, `db.py`: keine Logik hing an den deutschen String-Werten
  (bereits werte-agnostisch) - nur Docstrings/Kommentare aktualisiert.
- `seed_demo_accounts.py`: alle 100 `SEED_POSTS` neu auf Englisch geschrieben
  (nicht nur übersetzt, siehe Team-Anweisung), gleiche perspective/
  political_label-Achse pro Post beibehalten wie im deutschen Original.
  Verifiziert: 100 Posts, 12 Themen, jedes Thema hat mindestens einen
  "contra/left"- und einen "pro/right"-Post (Voraussetzung für
  DEMO_ACCOUNTS). `DEMO_ACCOUNTS`/Konsolen-Ausgaben ebenfalls Englisch.
- `tests/test_ranking.py`, `tests/test_fediverse.py`: Fixture-Daten
  (Themen-Keys, politische Labels, Post-Titel/-Text) ebenfalls auf Englisch
  umgestellt, obwohl nicht explizit gefordert (ranking.py ist wertagnostisch,
  die Tests haetten auch mit deutschen Fixtures weiter funktioniert) - fuer
  ein durchgaengig englisches Repo statt halb/halb.
- `supabase/migrations/`: 0003/0004/0006 direkt auf Englisch editiert (siehe
  oben), neue 0007 fuer die Umbenennung der bereits angewendeten 0001-Zeilen.
- `README.md`: komplett neu auf Englisch geschrieben (trotz "nachrangig" in
  der Team-Anweisung mit erledigt, da noch Zeit/Budget übrig war), inkl.
  eines neuen Checklisten-Eintrags fuer die Englisch-Umstellung und der
  Migrations-Entscheidung.
- Vault-Notiz `ObsidianGehirn/06 Zugangsdaten/Feed-Diversity-Beispielaccounts.md`:
  bewusst NICHT komplett übersetzt (Team-interne Doku ohne Besucher-Publikum,
  wie im Vault-Skill/Doku-Regeln vorgesehen) - nur die zitierten Systemwerte
  in der Tabelle (`links/rechts→left/right`) aktualisiert, damit sie nicht der
  echten App widersprechen.

**Bewusst NICHT übersetzt (mit Begründung):**
- `perspective`-Enum (`pro`/`contra`) bleibt unverändert - beide Wörter lesen
  sich bereits als Englisch (vgl. "pro and contra arguments"), die Team-
  Anweisung nennt dieses Feld nicht explizit, und der Wert ist bereits gegen
  die echte Supabase-Instanz angewendet (0001) sowie tief in Ranking-Logik/
  Tests verankert - eine Umbenennung waere ein groesserer, nicht angefragter
  Umbau. Falls das Team das anders sehen sollte: als naechster Schritt
  moeglich, würde aber denselben UPDATE-Ansatz wie bei categories brauchen
  (Wert ist keine ID, aber `check`-Constraints in mehreren Migrationen
  müssten mit).
- `deploy/README.md` bleibt Deutsch - reine Ops-Doku ohne Besucher-Publikum,
  noch klarer team-intern als die Haupt-README, fuer die die Team-Anweisung
  bereits "nachrangig" sagt.
- `NIGHTLY_TASK.md` (diese Datei) und Vault-Notizen bleiben Deutsch - das ist
  der etablierte Stil fuer die Team-interne Nacht-Doku, keine Anweisung dazu
  vorhanden.

**Weiterhin bestehende Blocker (wie in den letzten drei Läufen unverändert):**
`env | grep -i supabase` liefert nichts, `curl` gegen `mastodon.social`
schlägt mit `403` (Sandbox-Proxy) fehl. Deshalb weiterhin nicht möglich:
- `0003`/`0006`/`0007` gegen die echte Supabase-Instanz anwenden
- `seed_demo_accounts.py` tatsächlich ausführen
- Fediverse-Anzeige live gegen Mastodon verifizieren

**Verifiziert ohne Supabase:** `pytest tests/` (48/48 grün, davor 48/48 bereits
vor dieser Session - keine Tests entfernt, aber Fixture-Inhalte aktualisiert).
Flask-Testclient mit gemockter `db`-Schicht für `/`, `/?mode=diversity`,
`/login`, `/register`, `/dashboard` - alle 200, HTML manuell auf die neuen
`left/center/right`-Klassen und Themen-Strings geprüft (Kompass-Chip rendert
korrekt mit `active`-Klasse auf dem richtigen Segment). `grep` über den
gesamten Ordner nach den alten deutschen Themen-/Label-Wörtern in
`*.py`/`*.html`/`*.css`/`*.sql` - nur noch in der historischen 0001-Migration
und in 0007s eigenen `WHERE`-Klauseln (die absichtlich die alten Werte
referenzieren müssen, um sie umzubenennen).

**Priorität 2 (allgemeine Verbesserung) diese Session nicht extra bearbeitet** -
die Englisch-Umstellung allein hat das komplette Zeitbudget der Session
gebraucht (grosse Flaeche: 4 Templates, app.py, seed-Datensatz mit 100
Posts, 5 Migrationsdateien, 2 Testdateien, README). Nichts an "sonstige
Verbesserung" bewusst zurückgestellt, es gab schlicht keine Zeit mehr übrig.

## Nächste Schritte (Priorität absteigend)

1. **Sobald Supabase-Zugangsdaten verfügbar sind:** `0003_political_label.sql`,
   `0006_more_categories.sql` und die neue `0007_english_content.sql` in
   dieser Reihenfolge anwenden (SQL-Editor oder `apply_schema.py`, das
   automatisch alle unangewendeten `*.sql` in Dateinamen-Reihenfolge
   durchläuft). Danach `seed_demo_accounts.py` mit den `DEMO_*`-Variablen
   laufen lassen - jetzt mit komplett englischem Datensatz.
2. **Nach dem Seed-Lauf:** stichprobenartig prüfen, ob irgendwelche Posts
   auf dem Ziel-System schon vor dieser Session (manuell über die UI, nicht
   über das Seed-Skript) mit deutschen Titeln/Texten angelegt wurden - siehe
   README-Hinweis, dass `0007_english_content.sql` bewusst KEINE
   `posts`-Zeilen anfasst. Falls ja: manuell entscheiden (übersetzen oder
   stehen lassen), kein automatisches Find/Replace auf echten Nutzerinhalten.
3. **Fediverse-Anbindung live verifizieren** (inkl. Cache), sobald eine
   Umgebung mit normalem Internetzugriff verfügbar ist - jetzt mit den neuen
   englischen Hashtags (`climatepolicy` statt `klimapolitik` usw.), die noch
   nie gegen die echte Mastodon-API getestet wurden.
4. **Deployment tatsächlich durchführen**, sobald jemand mit VM-Zugriff Zeit
   hat (`deploy/README.md`) - diese Sessions können das nicht selbst.
5. Falls das Team die Priorität-2-Anweisung ("allgemein weiter verbessern")
   für den nächsten Lauf vorziehen möchte, weil Priorität 1 jetzt
   weitgehend erledigt ist: UI/Accessibility/Performance/Testabdeckung mit
   frischem Blick durchgehen - siehe Anweisung oben, kein Einzelpunkt mehr
   vorgegeben.
6. Politisches Label als optionales statt Pflichtfeld - weiterhin keine
   Team-Entscheidung bekannt, nicht umgesetzt.
7. Falls es noch offene PRs für diesen Ordner gibt, wenn der nächste Lauf
   startet: gegen den dann aktuellen main-Stand prüfen/rebasen, bevor
   inhaltlich weitergearbeitet wird (Merge bleibt bei Anton/Felix).

## Was in dieser Session NICHT versucht wurde (mit Absicht)

- Keine Supabase-Migrationen/Seed-Skripte ohne Zugangsdaten ausgeführt
- Kein Login/SSH/Deployment auf die Team-VM
- Kein Merge irgendeines PRs nach `main`
- Kein automatisches Übersetzen von `perspective` (`pro`/`contra`) oder von
  `deploy/README.md`/Vault-Notizen (siehe Begründung oben)

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
