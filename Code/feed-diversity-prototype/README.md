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

## Personas

Die Startseite hat zwei Schnellauswahl-Links, die direkt auf die
Problem-Statements einzahlen:

- **Mia** (PS1): sieht ausschließlich "pro"-Klimapolitik-Posts, merkt die
  Bubble nicht.
- **Tom** (PS2): steckt in "contra"-Wirtschaftspolitik-Posts fest, will
  bewusst raus.

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
- [ ] Datensatz ggf. um weitere Themen/Posts erweitern, sobald das Team echten
      Beispiel-Content hat
- [ ] Metrik für "Perspektivenvielfalt" sichtbar machen (siehe kritischer
      Punkt 6 in der DTEW-0209-Notiz)
