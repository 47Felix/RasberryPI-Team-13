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
Login). Fließt aktuell **nicht** ins Ranking ein (bewusst nicht gemacht, um
die getestete Diversity-Logik nicht anzufassen) – reine Anzeige/Interaktion
bisher.

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
- [ ] Likes als Ranking-Signal berücksichtigen (aktuell nur Anzeige, siehe oben)
- [ ] Metrik für "Perspektivenvielfalt" sichtbar machen (siehe kritischer
      Punkt 6 in der DTEW-0209-Notiz)
