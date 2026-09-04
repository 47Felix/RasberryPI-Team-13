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

- **Standard** (`standard_feed`): reine Ähnlichkeit zum zuletzt gesehenen
  Post – bubble-verstärkend, wie ein typischer "For You"-Feed.
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

## Neue Posts, Kategorie-Vorschlag & Likes (Supabase)

Der statische Datensatz (`data/posts.json`) lässt sich zur Laufzeit um
Nutzer-Posts erweitern, die über das Formular "Neuen Post erstellen"
angelegt werden. Storage ist Supabase Postgres, angebunden über `db.py`.

**Schema** (`supabase/migrations/0001_init.sql`): `categories`, `authors`,
`posts` (verweist auf beide), `likes` (Post + anonyme Session-Cookie-ID als
Composite Key). `authors`/`categories` sind mit denselben Werten vorbefüllt
wie `app.py:AUTHOR_META`, damit ein Nutzer-Post ins selbe "wirkt wie ein
echter Account pro Thema/Perspektive"-Design passt wie die statischen Posts.

- `.env` (nicht committet, siehe `.gitignore`) mit `SUPABASE_URL`,
  `SUPABASE_PUBLISHABLE_KEY`, `SUPABASE_SECRET_KEY`
- Backend nutzt ausschließlich den **Secret Key** (server-seitig, umgeht
  Row Level Security) – der Publishable Key wird aktuell vom Code gar nicht
  gebraucht, liegt nur für ein mögliches späteres Client-seitiges Feature mit
  in der `.env`
- Alle vier Tabellen haben RLS aktiv **ohne** Policies – nur der Secret Key
  kommt ran, direkter Zugriff über den Publishable Key ist absichtlich
  blockiert
- Tabellen einmalig anlegen: SQL aus `supabase/migrations/0001_init.sql` im
  Supabase Dashboard unter *SQL Editor* ausführen, **oder** `apply_schema.py`
  laufen lassen (braucht `SUPABASE_MANAGEMENT_TOKEN`, ein Account-weites
  Personal Access Token aus den Supabase-Kontoeinstellungen – direkter
  Postgres-Port 5432 ist aus manchen Sandbox-Umgebungen nicht erreichbar,
  das Skript geht deshalb über die Management-API per HTTPS)
- Fällt Supabase aus/ist nicht konfiguriert, degradiert die App sauber auf
  den statischen Datensatz (`db.fetch_posts()` gibt dann `[]` zurück, das
  Formular zeigt einen Hinweis statt eines Fehlers, Like-Buttons erscheinen
  nur bei Posts mit echten DB-Metadaten)

**Kategorie-Vorschlag:** `ranking.suggest_category()` (reine, netzwerkfreie
Funktion, per Unit-Test abgedeckt) vergleicht Titel+Text des Entwurfs per
TF-IDF gegen alle vorhandenen Posts und schlägt das Thema des ähnlichsten
Posts vor. Im Formular per "Vorschlagen"-Button (`POST /posts/suggest-category`)
angebunden, überschreibt aber nichts automatisch – Dropdown bleibt änderbar.

**Likes:** anonymer Toggle pro Browser über einen signierten Flask-Session-
Cookie (`FLASK_SECRET_KEY` in `.env`, Fallback-Wert nur für lokale Demos).
Nur für DB-Posts sichtbar, da `likes.post_id` auf `posts.id` (uuid)
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
- [x] Like-Toggle pro Browser-Session für DB-Posts
- [x] Tabellen in Supabase angelegt (04.09.2026, über die Management-API) und
      end-to-end verifiziert (Post erstellen, Like togglen, beides über die
      echte DB, siehe PR #88)
- [ ] Likes als Ranking-Signal berücksichtigen (aktuell nur Anzeige, siehe oben)
- [ ] Datensatz ggf. um weitere Themen/Posts erweitern, sobald das Team echten
      Beispiel-Content hat
- [ ] Metrik für "Perspektivenvielfalt" sichtbar machen (siehe kritischer
      Punkt 6 in der DTEW-0209-Notiz)
