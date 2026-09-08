# Feed-Diversity-Prototyp (DTEW Case 3)

Kleine Testumgebung für die Kernfrage aus Case 3 (digi&demo e.V.): *"Design of
feeds / 'For You': instead of algorithms that can reinforce bubbles, and
bubbles that form through self-selection, how can recommenders be designed to
inform users in a way that is varied but still topically relevant?"*

Kein selbst trainiertes ML-Modell (siehe [`ObsidianGehirn/10 DTEW
Workshop/Team 13 - Digitale Demokratie.md`](../../ObsidianGehirn/10%20DTEW%20Workshop/Team%2013%20-%20Digitale%20Demokratie.md)),
sondern klassisches Content-Based Filtering über TF-IDF + Cosine Similarity
(`scikit-learn`).

## Zwei Feed-Modi (`ranking.py`)

- **Standard** (`standard_feed`): gleiche Perspektive wie der Ausgangs-Post
  zuerst (Ähnlichkeit nur zum Sortieren innerhalb dieser Gruppe) – bubble-
  verstärkend, wie ein typischer "For You"-Feed. Reine globale Ähnlichkeit
  reicht dafür nicht: auf dem kleinen Datensatz teilen Gegenperspektiven-Posts
  zum selben Thema oft genauso viel Vokabular wie Posts mit gleicher
  Perspektive, sodass eine reine Similarity-Rangfolge die Bubble gar nicht
  zuverlässig zeigt (siehe Docstring in `ranking.py`).
- **Diversity-aware** (`diversity_aware_feed`): gleiche Ähnlichkeitsbasis,
  mischt aber alle `diversity_every` Plätze bewusst den ähnlichsten Post mit
  **gleichem Thema, aber Gegenperspektive** ein und kennzeichnet ihn.

**Account-Bias aus der Like-Historie:** Für eingeloggte Accounts entscheidet
nicht mehr nur der gerade gewählte Ausgangs-Post, welche Perspektive
"gewinnt" – `ranking.dominant_perspective()` wertet aus, ob ein Account über
alle bisherigen Likes hinweg mehrheitlich "pro" oder "contra" geliket hat,
und dieser `preferred_perspective`-Wert übersteuert dann in `standard_feed`/
`diversity_aware_feed` die Perspektive des Ausgangs-Posts. Ergebnis: der
Standard-Feed verstärkt sich mit jedem weiteren Like in eine Richtung selbst
und reinforct das *über jeden beliebigen Ausgangs-Post hinweg*, nicht nur
für den einen, der gerade geliket wurde – ganz bewusst ohne eingebauten
Ausweg (das ist der Punkt der Demo). Der Diversity-aware-Feed nutzt denselben
`preferred_perspective`-Wert, um gezielt die *tatsächliche* Account-Neigung
zu durchbrechen statt nur die des aktuellen Ausgangs-Posts. Ohne Account
oder ohne bisherige Likes (bzw. bei einem exakten Unentschieden) bleibt das
alte Verhalten erhalten: Perspektive des Ausgangs-Posts entscheidet.

## Politische Einordnung (links/mitte/rechts) als zweite, unabhängige Dimension

Bisher gab es pro Post nur eine Achse: `perspective` (pro/contra zum jeweiligen
Thema). Seit dieser Erweiterung gibt es eine zweite, davon unabhängige Achse:
`political_label` (`links`/`mitte`/`rechts`), z.B. ein Post kann gleichzeitig
"pro Windkraft-Ausbau" **und** "links" sein, oder "pro Windkraft-Ausbau"
**und** "rechts" – die beiden Achsen sind orthogonal, nicht dasselbe Feld
zweimal.

**Bewusst kein automatischer Links/Rechts-Klassifikator.** Kritischer Punkt 6
aus der DTEW-0209-Notiz (`ObsidianGehirn/10 DTEW Workshop/DTEW 0209 -
Kritische Punkte, Problem Statements und Ideation.md`) benennt es direkt:
"Wie misst/zeigt man 'Perspektivenvielfalt' überhaupt messbar, statt nur
subjektiv zu behaupten das ist jetzt vielfältiger?" Eine zuverlässige
automatische Erkennung der politischen Ausrichtung aus Freitext ist ein
ungelöstes, in der NLP-Forschung selbst umstrittenes Problem (uneinheitliche
Trainingsdaten, kulturell/zeitlich verschobene Definitionen von "links" und
"rechts", hohe Fehlerquote gerade bei kurzen Posts ohne viel Kontext) und für
ein zweiwöchiges Prototyping ohne ML-Vorerfahrung im Team nicht seriös
machbar (dieselbe Einschätzung wie schon bei Lasses Fake-News-Detektor-
Vorschlägen, siehe `ObsidianGehirn/10 DTEW Workshop/Team 13 - Digitale
Demokratie.md`). Ein Prototyp, der intern behauptet "das hier ist objektiv
links", würde eine Genauigkeit vortäuschen, die es nicht gibt, und selbst
genau die Art von unsichtbarer, unüberprüfbarer algorithmischer Bewertung
reproduzieren, die der ganze Case eigentlich sichtbar machen soll.

**Stattdessen: Nutzer wählen das Label selbst**, beim Post-Erstellen über ein
Dropdown, genau wie Thema/Perspektive schon funktionieren (`templates/
index.html`, Feld `political_label`, serverseitig gegen `KNOWN_POLITICAL_LABELS`
geprüft in `app.py:create_post`). Kein automatisches Nachjustieren, kein
verstecktes Scoring – die Autorin/der Autor sieht das eigene Label, alle
anderen sehen es am Post (kleiner Drei-Segment-"Kompass"-Chip, angelehnt an
Felix' Brain-Dump-Idee eines "Perspektiven-Kompass", siehe
`ObsidianGehirn/07 Brain Dump/Felix - Brain Dump.md`).

**Kritisch einzuordnen:** Ein selbst gewähltes Label ist kein objektives Maß
für "tatsächliche" politische Position, sondern eine Selbstauskunft. Das
bringt eigene Verzerrungen mit (Selbstauswahl, sozial erwünschte Antworten,
manche Nutzer:innen labeln strategisch "mitte" um neutral zu wirken, andere
übertreiben absichtlich), ist aber ehrlich darüber, was es ist: eine
Zuschreibung durch die Autorin/den Autor, keine von der App behauptete
Wahrheit. Für einen Demo-Prototyp, der zeigen soll *wie* ein Ranking eine
gewählte Dimension verstärken oder aufbrechen kann, reicht dieses transparente
Label – es ersetzt keine echte, validierte Politikwissenschafts-Metrik und
soll das auch nicht vorgeben.

**Wie es ins Ranking einfließt (`ranking.py`):** `dominant_political_label()`
ist das Pendant zu `dominant_perspective()` – Mehrheitslabel aus der gesamten
Like-Historie eines Accounts (`db.fetch_liked_political_labels()`), `None` bei
fehlendem Signal oder einem Unentschieden zwischen mehreren Labels. In
`standard_feed()` sortiert das Ergebnis (`preferred_political_label` oder
ersatzweise das Label des Ausgangs-Posts) *innerhalb* der bestehenden
Perspektive-Tier zusätzlich danach, ob das politische Label übereinstimmt –
ein Post, der sowohl Perspektive als auch politisches Lager trifft, steht vor
einem, der nur die Perspektive trifft. In `diversity_aware_feed()` bevorzugt
ein Diversity-Slot einen "doppelten Gegenpol" (weicht auf *beiden* Achsen ab)
vor einem, der nur auf einer Achse abweicht. `diversity_score_for_political_label()`
misst denselben Vielfalts-Anteil wie `diversity_score_for_perspective()`, nur
für die politische Achse, und wird in der UI als zweiter Wert neben dem
Perspektive-Score angezeigt (nur wenn ein politisches Signal überhaupt
vorliegt). Beide Achsen sind unabhängig testbar (`tests/test_ranking.py`) und
verändern das bestehende, bereits getestete Perspektive-Ranking nicht, wenn
kein `political_label` gesetzt ist (Rückwärtskompatibilität zu Posts von vor
dieser Erweiterung).

**Schema:** `supabase/migrations/0003_political_label.sql` fügt die Spalte
`posts.political_label` hinzu (nullable, `check` auf die drei erlaubten
Werte). Muss wie 0001/0002 einmalig angewendet werden (SQL-Editor oder
`apply_schema.py`) – siehe "Aktueller Stand" unten, in dieser Nacht-Session
ohne Supabase-Zugriff nicht möglich.

## UI: ein Feed, zwei Modi (`templates/index.html`, `static/style.css`)

Nach Nutzer-Feedback ("sieht nach Claude Design aus", "kein richtiger Feed")
verworfen: zwei nebeneinanderliegende Spalten mit Segmented Control, Regler
und Score-Pille. Stattdessen ein **einzelner, vertikal scrollender Feed** mit
einem Tab-Umschalter oben ("Standard" / "Diversity-aware", `?mode=`), wie ein
echter Wechsel zwischen zwei Feeds in einer App:

> [!note] Zweites Redesign (Nacht-Session): weg vom generischen SaaS-Look
> Dasselbe Feedback ("sieht nach Claude Design aus") kam ein zweites Mal, diesmal
> zur konkreten Umsetzung (Indigo-Verlauf im Header, durchgehend abgerundete
> weiße Karten, Sans-Serif-UI-Font) – typische Merkmale generischer
> KI-Dashboard-Vorlagen. `static/style.css` wurde daraufhin komplett auf eine
> redaktionelle Optik umgestellt statt nur Farben zu tauschen: warmer
> Papier-Hintergrund statt kühles Grau, Serif-Schrift (Georgia) fürs
> Nameplate/die Post-Titel statt Sans-Serif überall, eine Monospace-Schrift
> für Metadaten (Handle, Zeit, Kategorien-Chips) im Stil einer
> Nachrichtenagentur-Zeile, feine Trennlinien statt schwebender Karten mit
> Schatten, kein Farbverlauf mehr im Header (flache Fläche mit Doppellinie wie
> ein Zeitungs-Impressum). Die neue politische Einordnung (siehe oben) bekommt
> einen eigenen kleinen Drei-Segment-"Kompass"-Chip statt eines weiteren
> generischen Badges, als eigenständiges visuelles Element statt Farbe Nummer
> drei im selben Chip-Stil.

- Jeder Post hat eine feed-typische Kopfzeile (Avatar, Account-Name, Handle,
  relative Zeitangabe) statt einer nackten Karte – Avatar/Name/Handle kommen
  vom echten Account, der den Post erstellt hat.
- Gegenperspektiven-Posts bekommen ein kleines "Vorgeschlagen"-Label statt
  eines auffälligen Badges.
- Eigener Ausgangs-Post und Vielfalt-Regler sind in ein eingeklapptes
  "Feed-Einstellungen"-Element verschoben – sichtbar/bedienbar, aber nicht
  mehr die Hauptfläche der Seite.

## Accounts, Posts, Kommentare, Likes & Kategorie-Vorschlag (Supabase)

Es gibt keinen statischen/hartcodierten Datensatz mehr – **alle** Posts im
Feed kommen aus Supabase, angelegt von echten Accounts über das Formular
"Neuen Post erstellen". Ist Supabase nicht konfiguriert/erreichbar oder die
Tabelle leer, zeigt die Seite einen expliziten leeren Zustand statt
irgendwelcher Platzhalter-Inhalte. Storage ist Supabase Postgres, angebunden
über `db.py`. Posten, Liken und Kommentieren setzt einen **echten,
eingeloggten Account** voraus (Supabase Auth) – keine anonymen Interaktionen.

**Schema** (`supabase/migrations/0001_init.sql` + `0002_accounts.sql`):
`categories`, `authors` (Fallback-Anzeige für Posts von vor der Account-
Einführung, siehe unten), `posts` (verweist auf beide + `user_id`),
`profiles` (Anzeigename/Handle/Avatar pro Supabase-Auth-Account, `id` =
`auth.users.id`), `likes` (Post + `user_id`, Composite Key – ein Like pro
Account und Post), `comments` (Post + `user_id` + Text, per Account
löschbar). `posts.user_id`/`likes.user_id`/`comments.user_id` zeigen bewusst
auf `profiles(id)` statt direkt auf `auth.users(id)` – nur so kann PostgREST
die Relation beim Abfragen einbetten (`auth`-Schema ist für PostgREST nicht
sichtbar). Bei der Einbettung von `profiles` in `fetch_posts()` ist zusätzlich
der explizite Hint `profiles!posts_user_id_fkey` nötig, weil `likes` (mit
`post_id` *und* `user_id`) aus PostgREST-Sicht eine zweite, many-to-many-
Beziehung zwischen `posts` und `profiles` bildet – ohne den Hint verweigert
PostgREST die Anfrage als mehrdeutig.

- `.env` (nicht committet, siehe `.gitignore`) mit `SUPABASE_URL`,
  `SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_SECRET_KEY`
- Datentabellen laufen weiterhin ausschließlich über den **Secret Key**
  (server-seitig, umgeht Row Level Security) – **neu:** Registrierung/Login
  gehen direkt gegen die Supabase-Auth-API (GoTrue) mit dem
  **Publishable Key**, das ist der dafür vorgesehene Key (siehe
  `db.sign_up`/`db.sign_in`)
- Alle Tabellen haben RLS aktiv **ohne** Policies – nur der Secret Key kommt
  an die Daten-Tabellen ran, direkter Zugriff über den Publishable Key ist
  dort absichtlich blockiert
- Im Supabase-Dashboard unter *Authentication → Providers → Email* die
  Option **"Confirm email" deaktivieren** – sonst kann sich niemand direkt
  nach der Registrierung einloggen, weil erst ein Bestätigungslink in einer
  (in diesem Setup nicht konfigurierten) E-Mail geklickt werden müsste
- Tabellen/Migrationen einmalig anlegen: SQL aus
  `supabase/migrations/*.sql` der Reihe nach im Supabase Dashboard unter
  *SQL Editor* ausführen, **oder** `apply_schema.py` laufen lassen (ohne
  Argument wendet es automatisch alle Migrationen in Dateinamen-Reihenfolge
  an; braucht `SUPABASE_MANAGEMENT_TOKEN`, ein Account-weites Personal
  Access Token aus den Supabase-Kontoeinstellungen – direkter Postgres-Port
  5432 ist aus manchen Sandbox-Umgebungen nicht erreichbar, das Skript geht
  deshalb über die Management-API per HTTPS)
- Likes sind an `(post_id, user_id)` gebunden (durch `0002_accounts.sql`
  bereits umgestellt, angewendet gegen die echte Instanz). Posts von vor der
  Account-Einführung ohne `user_id` zeigen weiterhin den fiktiven
  `authors`-Eintrag als Autor, neue Posts zeigen den echten Account
- Fällt Supabase aus/ist nicht konfiguriert oder sind noch keine Posts
  angelegt, zeigt die Seite einen leeren Zustand ("Keine Posts gefunden")
  statt eines Fehlers oder erfundener Inhalte

**Accounts:** `/register` (E-Mail, Passwort, Anzeigename) legt einen
Supabase-Auth-Account plus `profiles`-Zeile an (Handle wird aus dem
Anzeigenamen abgeleitet, bei Kollision mit Zahlensuffix, siehe
`db.create_unique_profile`). `/login`/`/logout` verwalten die Session
(Flask-Session-Cookie speichert nur `user_id`/Anzeigename/Handle, nicht das
Passwort). Ohne Account: Feed lesen geht weiterhin, Posten/Liken/
Kommentieren verlangt Login (Redirect zu `/login`, bei den fetch()-Aktionen
über einen 401).

**Kommentare:** pro Post über "💬 N Kommentare" aufklappbar (lädt per
`GET /posts/<id>/comments`), neuer Kommentar via Formular
(`POST /posts/<id>/comments`, JSON, verlangt Login). Eigene Kommentare
lassen sich über einen "Löschen"-Link wieder entfernen
(`DELETE /comments/<id>`) – die Berechtigung wird serverseitig geprüft
(`db.delete_comment` filtert zusätzlich auf `user_id`), nicht nur durch das
Verstecken des Buttons in der UI.

**Kategorie-Vorschlag:** `ranking.suggest_category()` (reine, netzwerkfreie
Funktion, per Unit-Test abgedeckt) vergleicht Titel+Text des Entwurfs per
TF-IDF gegen alle vorhandenen Posts und schlägt das Thema des ähnlichsten
Posts vor. Im Formular per "Vorschlagen"-Button (`POST /posts/suggest-category`)
angebunden, überschreibt aber nichts automatisch – Dropdown bleibt änderbar.

**Likes:** Toggle pro Account (`(post_id, user_id)` in der DB, verlangt
Login). Fließt seit `dominant_perspective()`/`dominant_political_label()`
(siehe oben) direkt ins Ranking ein, nicht mehr nur reine Anzeige.

## Lokal starten

```bash
cd Code/feed-diversity-prototype
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Dann `http://localhost:5050` öffnen.

## Tests

```bash
pytest tests/
```

## Beispiel-Accounts für den Standard-Algorithmus (`seed_demo_accounts.py`)

Für eine überzeugende Demo braucht es Accounts mit einer klar erkennbaren,
gegensätzlichen Like-Historie, damit `ranking.dominant_perspective()`/
`dominant_political_label()` beim Vorführen sichtbar wird. `seed_demo_accounts.py`
legt dafür vier Beispiel-Accounts (unterschiedliche Namen, je zwei liken
konsequent "contra"/"links" bzw. "pro"/"rechts") sowie einen Admin-Account an,
der die Seed-Posts veröffentlicht, und lässt die Beispiel-Accounts passende
Posts liken.

**Zugangsdaten kommen ausschließlich aus der Umgebung/`.env`** (`DEMO_ACCOUNT_A_EMAIL`/
`_PASSWORD` bis `DEMO_ACCOUNT_D_EMAIL`/`_PASSWORD`, `DEMO_ADMIN_EMAIL`/`_PASSWORD`,
zusätzlich zu den bestehenden `SUPABASE_*`-Variablen) - das Skript bricht ohne
diese Variablen ab, statt Platzhalterwerte zu verwenden. Diese Session hatte
keine Supabase-Zugangsdaten zur Verfügung und konnte das Skript deshalb nicht
ausführen (siehe `NIGHTLY_TASK.md`). Eine reine Namens-/Zweck-Übersicht der
Accounts (ohne Zugangsdaten) steht im Vault unter `ObsidianGehirn/06
Zugangsdaten/Feed-Diversity-Beispielaccounts.md`.

```bash
# .env ergänzen (SUPABASE_* + die DEMO_*-Variablen oben), dann einmalig:
python3 seed_demo_accounts.py
```

## Aktueller Stand / offen

- [x] Standard- und Diversity-aware-Ranking mit Tests (`ranking.py`, dataset-
      unabhängig – funktioniert mit beliebigen Posts, egal ob früher aus
      `data/posts.json` oder jetzt aus Supabase)
- [x] Supabase-Anbindung für alle Posts, Kategorien, Autoren
- [x] Kategorie-Vorschlag per TF-IDF beim Post-Erstellen
- [x] Echte Accounts (Supabase Auth: Registrierung/Login/Logout), Profile
      mit Anzeigename/Handle, Likes und Kommentare pro Account statt
      anonymer Session-Cookies (`0002_accounts.sql`, gegen die echte Instanz
      angewendet und end-to-end verifiziert)
- [x] Eigene Kommentare löschbar (`DELETE /comments/<id>`, serverseitig auf
      Eigentümerschaft geprüft)
- [x] Statischer Datensatz (`data/posts.json`) sowie die darauf aufbauende
      Persona-Schnellauswahl ("Mia"/"Tom") entfernt – der Feed zeigt
      ausschließlich echte Supabase-Posts, leerer Zustand statt Platzhalter
      wenn noch keine welche existieren
- [x] Likes als Ranking-Signal: Standard-Feed reinforct jetzt die
      Mehrheits-Perspektive der eigenen Like-Historie statt nur die des
      gerade gewählten Ausgangs-Posts (`dominant_perspective`)
- [ ] Metrik für "Perspektivenvielfalt" sichtbar machen (siehe kritischer
      Punkt 6 in der DTEW-0209-Notiz) – der Diversity-Score existiert schon
      pro Feed-Aufruf, aber es gibt noch keine Verlaufsansicht über die Zeit
- [x] Politische Einordnung (links/mitte/rechts) als zweite, unabhängige
      Dimension neben pro/contra, nutzergewählt statt automatisch erkannt
      (siehe "Politische Einordnung" oben, `0003_political_label.sql`)
- [x] Visuelles Redesign weg vom generischen SaaS-/KI-Dashboard-Look
      (Papier-Optik, Serif/Monospace statt durchgehend Sans-Serif, Kompass-Chip
      statt Verlauf/abgerundete Karten überall, siehe "UI-Redesign" oben)
- [ ] `0003_political_label.sql` gegen die echte Supabase-Instanz anwenden
      (in dieser Nacht-Session ohne `SUPABASE_MANAGEMENT_TOKEN` nicht möglich,
      siehe NIGHTLY_TASK.md)
- [ ] Beispiel-Accounts mit gegensätzlicher Like-Historie für die Demo
      (Skript vorbereitet, noch nicht ausgeführt – siehe `seed_demo_accounts.py`
      und NIGHTLY_TASK.md)
- [ ] Fediverse/ActivityPub-Anbindung (siehe eigene Machbarkeits-Notiz im
      Vault unter "10 DTEW Workshop")
