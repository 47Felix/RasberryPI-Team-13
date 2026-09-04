---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0509 (Samstag) – Freier Tag & Vorbereitung auf Montag (Business Model Canvas, Prototyp-Vorstellung)

Vorbereitung für Samstag, 05.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Laut Zeitplan ist das Wochenende 05.–06.09. **frei** ("optionale Ausflüge"), es gibt für Samstag kein offizielles Workshop-Pflichtprogramm. Case bleibt **Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung**, Personas Mia/Tom, aktueller Prototyp-Stand siehe [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]. Wie an den Vortagen: Alles mit 📝 markiert **muss vor Ort/live im Team passieren**, kein Schreibtisch-Ersatz möglich.

> [!warning] Board-Zugriff diese Nacht wieder nicht möglich
> Dritte Nacht in Folge derselbe Befund (siehe [[TaskCards Board]] für Details): Der Sandbox-Egress-Proxy dieser Cloud-Umgebung lehnt `itech-bs14.taskcards.app` weiterhin mit `403` auf den `CONNECT`-Tunnel ab – laut Proxy-Diagnose eine **Richtlinien-Ablehnung**, kein temporärer Ausfall, und nicht durch Wiederholen lösbar. Weder das Haupt-/Teams-Board (Aufgabenkarte für Samstag, falls es überhaupt eine gibt) noch das Team-13-Gruppenboard konnten gelesen oder bearbeitet werden. Die Aufgabenliste unten stammt deshalb wie an den Vortagen **nur aus der Übersicht** (Stand Board 01.09.), nicht aus einer tagesaktuellen Karte. Damit stehen jetzt **zwei Nächte Rückstand** beim Team-13-Karten-Update (Freitag + Samstag) – bitte morgens als Erstes das echte Board prüfen.

## Aufgaben von heute (laut Übersicht, Stand Board 01.09.)
- Kein Pflichtprogramm – Wochenende 05.–06.09. ist frei
- Optionale Ausflüge zur Auswahl: Lübeck/Travemünde, Lüneburg, Planten un Blomen, Planetarium, Wattwanderung Cuxhaven u. a.
- Nächster offizieller Termin: **Montag 07.09.**, 09:00 Start – Input "From ideas to Business" + Business Model Canvas, **11:00 Peer-Feedback** und **11:00 erste Prototyp-Version + Planung zeigen** (Zielgruppe/Personas, Bedürfnisse, Kernfeatures, was bewusst weggelassen wurde), **Retrospektive – Sprint-Ende**, 14:00 KIXX-Kicker-Turnier

## 📝 Nur vor Ort/live möglich
- **Entscheidung, ob/welcher Ausflug** – reine Team-Präferenz, nicht vorwegnehmbar
- **Echtes Board morgen früh prüfen** – falls Organisatoren doch etwas für Samstag/Sonntag gepostet haben (wegen des Zugriffsausfalls oben unbestätigt)
- **Team-13-Karte auf dem Gruppenboard nachpflegen** – Stand Freitag (siehe [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]) liegt weiterhin nur im Vault, noch nicht auf dem Board
- **Montags-Vorbereitung unten im Team gegenchecken** – die Prototyp-Vorstellung unten ist ein Entwurf, keine fertige Team-Entscheidung

## ✅ Vorbereitet: Prototyp-Vorstellung für Montag 07.09., 11:00 Uhr

Die Übersicht verlangt für Montag konkret vier Punkte (Zielgruppe/Personas, Bedürfnisse, Kernfeatures, bewusst Weggelassenes) – hier als Entwurf, damit am Montagmorgen nur noch der aktuelle Code-Stand gegengecheckt und ggf. gekürzt werden muss.

**Zielgruppe/Personas:**
- **Mia (20)**, "The Everyperson" – merkt nicht, dass ihr Feed fast ausschließlich eine Perspektive zeigt; sieht sich selbst als informiert.
- **Tom (22)**, "The Seeker" – merkt die Einseitigkeit, versucht aktiv auszubrechen, wird vom Algorithmus aber immer wieder zurückgezogen.
- Vollständige Steckbriefe: [`DTEW-Workshop/personas-mia-tom/personas-mia-tom.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/DTEW-Workshop/personas-mia-tom/personas-mia-tom.md)

**Bedürfnisse:**
- Mia: Sichtbarmachen des eigenen Bubble-Effekts, ohne dass sie aktiv danach suchen muss (sie würde von selbst nie nachfragen).
- Tom: ein Werkzeug, das ihn zuverlässig mit thematisch relevanten Gegenperspektiven versorgt, statt dass er das manuell und mühsam selbst zusammensuchen muss.
- Gemeinsam: Transparenz – beide sollen nachvollziehen können, *warum* ein Post im Feed erscheint, nicht nur *dass* er erscheint.

**Kernfeatures (aktueller Code-Stand, `Code/feed-diversity-prototype/`):**
- Zwei Ranking-Modi im selben Flask-Frontend (`ranking.py`): **Standard** (reine TF-IDF-Ähnlichkeit zum zuletzt gesehenen Post, bubble-verstärkend) vs. **Diversity-aware** (gleiche Ähnlichkeitsbasis, mischt alle `diversity_every` Plätze bewusst eine thematisch passende Gegenperspektive ein und kennzeichnet sie als "Vorgeschlagen").
- Persona-Schnellauswahl ("Ansicht als Mia/Tom") direkt in der UI, zeigt sofort den für die jeweilige Persona typischen Bubble-Zustand.
- **Diversity-Score** (`ranking.diversity_score`): sichtbare Kennzahl, wie viel Prozent der angezeigten Posts von der Ausgangsperspektive abweichen – direkte Antwort auf den am Mittwoch offen gelassenen kritischen Punkt "Metrik für Perspektivenvielfalt" (siehe [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]]).
- Nutzergenerierte Posts über Supabase (Titel/Text/Kategorie/Perspektive), inkl. TF-IDF-basiertem Kategorie-Vorschlag und anonymem Like-Toggle pro Browser-Session – Tabellen live angelegt und end-to-end getestet (siehe [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]).
- Fällt Supabase aus, degradiert die App sauber auf den statischen 15-Post-Datensatz statt abzustürzen.

**Was bewusst weggelassen wurde (und warum):**
- **Kein selbst trainiertes ML-Modell** – klassisches Content-Based Filtering (TF-IDF + Cosine Similarity) reicht, um die Kernfrage (Bubble sichtbar machen + Gegenperspektive einmischen) zu demonstrieren, spart Trainingsaufwand/Datenmenge, die im Workshop-Zeitrahmen nicht realistisch wären.
- **Likes fließen nicht ins Ranking ein** – bewusst nur Anzeige/Interaktion, um die bereits getestete Diversity-Logik nicht zusätzlich zu verkomplizieren.
- **Keine echte Plattform-Integration** (z. B. Bluesky Custom Feeds) – Prototyp bleibt Standalone-Demo, Integration wäre ein möglicher nächster Schritt, aber kein MVP-Bestandteil (siehe Marketing-Realitätscheck vom Freitag).
- **Kein visuelles Logo, kein fertiger Produktname** – Textkonzept ("Perspektivenkompass") liegt vor, aber bewusst noch offen für die Team-Entscheidung.

> [!tip] Für die Live-Runde
> Der Abschnitt oben ist bewusst so geschrieben, dass er sich fast direkt als 1-Minuten-Vorstellung sprechen lässt (Zielgruppe → Bedürfnis → Feature → Grenze). Vor der eigentlichen Präsentation am Montag unbedingt gegen den dann tatsächlich aktuellen Code-/Datenstand prüfen, falls übers Wochenende noch etwas geändert wurde.

## Was noch fehlt
- [ ] Board-Zugriffsproblem bleibt (3. Nacht in Folge) – siehe [[TaskCards Board]]; Team-13-Karte hat jetzt 2 Tage Rückstand (Freitag + Samstag), sollte am Montagmorgen als Erstes nachgeholt werden
- [ ] Geleakten (ersten) Supabase-Token weiterhin vorsorglich widerrufen (siehe [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]) – noch offen laut letzter Notiz
- [ ] Social Business Model Canvas vom Freitag im Team durchsprechen, kürzen/anpassen (noch nicht als erledigt vermerkt)
- [ ] Prototyp-Arbeitstitel/Namen entscheiden (Vorschlag "Perspektivenkompass" nur Diskussionsgrundlage)
- [ ] Business Model Canvas Vorlage für Montag (`the-society-model-canvas.pdf` / `Business-Model-Canvas-Size-A4_2-2.pdf`) vom Haupt-Board laden und Freitags-Entwurf ins offizielle Formularlayout übertragen
- [ ] Retrospektive (Montag, Sprint-Ende) vorbereiten: kurze Sammlung "was lief gut/schlecht in Woche 1" wäre hilfreich, ist hier aber bewusst nicht vorweggenommen, da es echte Team-Reflexion braucht
- [ ] Vault-Notiz für Donnerstag (03.09., AI-Workshop-Entscheidung/Kanban-Board/Prototyping-Start) weiterhin offen, falls noch nicht nachgetragen
- [ ] Beispiel-Datensatz für die Recommender-Demo ggf. erweitern (offen seit Mittwoch, siehe [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]])

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[Team 13 - Digitale Demokratie]]
- [[DTEW 0409 - Social Business Model Canvas, Marketing und Onboarding]]
- [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]]
- [[TaskCards Board]] – Board-Zugriff & technische Einschränkungen (inkl. drittem Ausfall in Folge)
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
