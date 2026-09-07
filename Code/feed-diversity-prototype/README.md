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

## UI: ein Feed, zwei Modi (`templates/index.html`, `static/style.css`)

Nach Nutzer-Feedback ("sieht nach Claude Design aus", "kein richtiger Feed")
verworfen: zwei nebeneinanderliegende Spalten mit Segmented Control, Regler
und Score-Pille. Stattdessen ein **einzelner, vertikal scrollender Feed** mit
einem Tab-Umschalter oben ("Standard" / "Diversity-aware", `?mode=`), wie ein
echter Wechsel zwischen zwei Feeds in einer App:

- Jeder Post hat eine feed-typische Kopfzeile (Avatar, Account-Name, Handle,
  relative Zeitangabe) statt einer nackten Karte.
- Jedes Thema/Perspektive-Paar ist ein eigener fiktiver Account
  (`app.py:AUTHOR_META`) – im Standard-Feed taucht praktisch nur ein Account
  wieder und wieder auf (die Bubble), im Diversity-aware-Feed unterbrechen
  andere Accounts das Muster. Der Unterschied soll beim Scrollen auffallen,
  nicht nur an einer Prozentzahl.
- Gegenperspektiven-Posts bekommen ein kleines "Vorgeschlagen"-Label statt
  eines auffälligen Badges.
- Eigener Ausgangs-Post und Vielfalt-Regler sind in ein eingeklapptes
  "Feed-Einstellungen"-Element verschoben – sichtbar/bedienbar, aber nicht
  mehr die Hauptfläche der Seite.

## Personas

Die Seite hat zwei Schnellauswahl-Chips ("Ansicht als"), die direkt auf die
Problem-Statements einzahlen:

- **Mia** (PS1): sieht ausschließlich "pro"-Klimapolitik-Posts, merkt die
  Bubble nicht.
- **Tom** (PS2): steckt in "contra"-Wirtschaftspolitik-Posts fest, will
  bewusst raus.

## Accounts, neue Posts, Kommentare, Likes & Kategorie-Vorschlag (Supabase)

Der statische Datensatz (`data/posts.json`) lässt sich zur Laufzeit um
Nutzer-Posts erweitern, die über das Formular "Neuen Post erstellen"
angelegt werden. Storage ist Supabase Postgres, angebunden über `db.py`.
Posten, Liken und Kommentieren setzt einen **echten, eingeloggten Account**
voraus (Supabase Auth) – keine anonymen Interaktionen mehr.

**Schema** (`supabase/migrations/0001_init.sql` + `0002_accounts.sql`):
`categories`, `authors` (fiktive Accounts für den statischen Datensatz),
`posts` (verweist auf beide + optional `user_id`), `profiles` (Anzeigename/
Handle/Avatar pro Supabase-Auth-Account, `id` = `auth.users.id`), `likes`
(Post + `user_id`, Composite Key – ein Like pro Account und Post), `comments`
(Post + `user_id` + Text). `posts.user_id`/`likes.user_id`/`comments.user_id`
zeigen bewusst auf `profiles(id)` statt direkt auf `auth.users(id)` – nur so
kann PostgREST die Relation beim Abfragen einbetten (`auth`-Schema ist für
PostgREST nicht sichtbar).

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
- ⚠️ **Breaking Change durch `0002_accounts.sql`:** Likes waren bisher an
  eine anonyme Session-Cookie-ID gebunden, das lässt sich keinem Account
  zuordnen – die Migration löscht deshalb alle bestehenden Like-Zeilen und
  stellt danach auf `(post_id, user_id)` um. Bestehende Posts ohne
  `user_id` (vor dieser Änderung angelegt) zeigen weiterhin den fiktiven
  `authors`-Eintrag als Autor, neue Posts zeigen den echten Account
- Fällt Supabase aus/ist nicht konfiguriert, degradiert die App sauber auf
  den statischen Datensatz (`db.fetch_posts()` gibt dann `[]` zurück, das
  Formular zeigt einen Hinweis statt eines Fehlers, Like-/Kommentar-UI
  erscheint nur bei Posts mit echten DB-Metadaten)

**Accounts:** `/register` (E-Mail, Passwort, Anzeigename) legt einen
Supabase-Auth-Account plus `profiles`-Zeile an (Handle wird aus dem
Anzeigenamen abgeleitet, bei Kollision mit Zahlensuffix, siehe
`db.create_unique_profile`). `/login`/`/logout` verwalten die Session
(Flask-Session-Cookie speichert nur `user_id`/Anzeigename/Handle, nicht das
Passwort). Ohne Account: Feed lesen geht weiterhin, Posten/Liken/
Kommentieren verlangt Login (Redirect zu `/login`, bei den fetch()-Aktionen
über einen 401).

**Kommentare:** pro DB-Post über "💬 N Kommentare" aufklappbar (lädt per
`GET /posts/<id>/comments`), neuer Kommentar via Formular
(`POST /posts/<id>/comments`, JSON, verlangt Login). Nur für DB-Posts, aus
demselben Grund wie Likes (siehe unten).

**Kategorie-Vorschlag:** `ranking.suggest_category()` (reine, netzwerkfreie
Funktion, per Unit-Test abgedeckt) vergleicht Titel+Text des Entwurfs per
TF-IDF gegen alle vorhandenen Posts und schlägt das Thema des ähnlichsten
Posts vor. Im Formular per "Vorschlagen"-Button (`POST /posts/suggest-category`)
angebunden, überschreibt aber nichts automatisch – Dropdown bleibt änderbar.

**Likes:** Toggle pro Account (`(post_id, user_id)` in der DB, verlangt
Login). Nur für DB-Posts sichtbar, da `likes.post_id` auf `posts.id` (uuid)
verweist und die statischen JSON-Posts keine echten IDs dafür haben. Fließt
aktuell **nicht** ins Ranking ein (bewusst nicht gemacht, um die getestete
Diversity-Logik nicht anzufassen) – reine Anzeige/Interaktion bisher.

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

## Aktueller Stand / offen

- [x] Datensatz mit 15 Posts, 3 Themen, je pro/contra
- [x] Standard- und Diversity-aware-Ranking mit Tests
- [x] Minimale Flask-UI mit Persona-Schnellauswahl
- [x] Supabase-Anbindung für nutzergenerierte Posts, Kategorien, Autoren
      (Code steht, siehe oben)
- [x] Kategorie-Vorschlag per TF-IDF beim Post-Erstellen
- [x] Tabellen in Supabase angelegt (04.09.2026, über die Management-API) und
      end-to-end verifiziert (Post erstellen, Like togglen, beides über die
      echte DB, siehe PR #88)
- [x] Echte Accounts (Supabase Auth: Registrierung/Login/Logout), Profile
      mit Anzeigename/Handle, Likes und Kommentare pro Account statt
      anonymer Session-Cookies (`0002_accounts.sql`)
- [ ] `0002_accounts.sql` muss noch gegen die echte Supabase-Instanz
      angewendet werden (siehe oben, `apply_schema.py` oder SQL Editor) und
      "Confirm email" im Dashboard deaktiviert werden – bis dahin bleiben
      Login/Registrierung ohne Effekt (`db.sign_up`/`db.sign_in` liefern
      dann `None`)
- [ ] Likes als Ranking-Signal berücksichtigen (aktuell nur Anzeige, siehe oben)
- [ ] Datensatz ggf. um weitere Themen/Posts erweitern, sobald das Team echten
      Beispiel-Content hat
- [ ] Metrik für "Perspektivenvielfalt" sichtbar machen (siehe kritischer
      Punkt 6 in der DTEW-0209-Notiz)
