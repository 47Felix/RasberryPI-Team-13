# DTEW Hamburg – Digitale Demokratie (Team 13)

Deliverables für den zusätzlichen "2026 International Design Thinking and Entrepreneurship Workshop Hamburg" (31.08.–12.09.2026), separat vom eigentlichen Smart-Systems-Pi-Projekt. Hintergrund und laufende Doku dazu stehen im Vault unter [`ObsidianGehirn/10 DTEW Workshop/`](../ObsidianGehirn/10%20DTEW%20Workshop) ([[DTEW Hamburg - Übersicht]], [[Team 13 - Digitale Demokratie]]).

- **`case-analysis-worksheet.md`** – Quelldatei (Markdown), die bei Änderungen bearbeitet werden sollte. **Auf Englisch**, wie der Workshop (internationales Team, Original-Worksheet ist auch Englisch).
- **`case-analysis-worksheet.html`** – fertig gerenderte Version zum direkten Anzeigen im Browser (eigenständig, kein Marp/Build-Schritt nötig).
- **`case-analysis-worksheet.pdf`** – PDF-Version im Layout des Original-Worksheets vom DTEW-Haupt-Board, ausgefüllt mit unseren 3 Cases – das ist das eigentliche Abgabe-Dokument für den Workshop.
- **`templates/`** – unausgefüllte Original-Vorlagen vom DTEW-Haupt-Board (Empathy Map, Persona-Template, Persona-Empathy-Map, Observation AEIOU, Problem Tree, Fiedler-Disney-Methode, Tutorial-Übersicht Design-Thinking-Methoden). Referenzmaterial, keine eigenen Deliverables – siehe [[Team 13 - Digitale Demokratie]] und [[DTEW 0109 - Teampathy Map und Empathize]] für unsere ausgefüllten Versionen.
- **`critical-issues-and-problem-statements.md`/`.html`/`.pdf`** – Mittwochs-Aufgabe (02.09.): kritische Punkte, Problem Statements, Walt-Disney-Ideation-Entwurf, Pitch-Stichpunkte fürs Peer Feedback. Entwurf zum Reinkopieren/Anpassen im Team, danach ins offizielle `Critical_Issues.pdf` vom Haupt-Board übertragen (liegt uns noch nicht lokal vor) – siehe [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]].
- **`personas-mia-tom.md`/`.html`/`.pdf`** – ausgefülltes `persona-template.pdf` für die beiden Proto-Personas (Mia, Tom) von Case 3, auf Desk-Research + Dienstags-Notizen basierend, **noch nicht durch echte Interviews validiert** – siehe [[DTEW 0109 - Teampathy Map und Empathize]].

## Worum geht's

Ausgefülltes `case_analysis_worksheet.pdf` vom Haupt-Board (Case *"The Internet and Politics – Your Network, Your Rules?"*) für die Montags-Aufgabe "First Brainstorming". Alle 3 Cases (CASE 1/2/3) drehen sich um **digi&demo e.V.** (digiunddemo.de), unsere inhaltliche Richtung, verbunden über den parallel laufenden Aktionstag **"Dein Netz, Deine Regeln!"** im Bürgerhaus Wilhelmsburg (buewi.de/netz-ablauf). digi&demo nennt selbst drei Herausforderungen für offenen digitalen Diskurs – genau die drei sind unsere Cases:

1. **digi&demo – Hate Speech**
2. **digi&demo – Desinformation**
3. **digi&demo – Polarisierung**

## Neu rendern nach Änderungen an der `.md`/`.html`

Die `.html` ist von Hand geschrieben (kein Marp, da Formular-Layout statt Folien) – bei Textänderungen `.md` **und** `.html` beide anpassen. PDF danach neu rendern:

```bash
cd DTEW-Workshop
npx --yes playwright install chromium   # einmalig, falls noch nicht vorhanden
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + process.cwd() + '/case-analysis-worksheet.html', { waitUntil: 'networkidle' });
  await page.pdf({ path: 'case-analysis-worksheet.pdf', format: 'A4', printBackground: true, margin: { top: '0', bottom: '0', left: '0', right: '0' } });
  await browser.close();
})();
"
```

## Nächster Schritt

Case 3 (Feed-/Recommender-Design) ist entschieden (siehe [[Team 13 - Digitale Demokratie]]). Mittwoch 02.09.: kritische Punkte, 1–2 Problem Statements und eine Ideation-Runde (6-3-5 oder Walt-Disney) dazu ausarbeiten. Siehe [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]] im Vault.
