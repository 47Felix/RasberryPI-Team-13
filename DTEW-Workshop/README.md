# DTEW Hamburg – Digitale Demokratie (Team 13)

Deliverables für den zusätzlichen "2026 International Design Thinking and Entrepreneurship Workshop Hamburg" (31.08.–12.09.2026), separat vom eigentlichen Smart-Systems-Pi-Projekt. Hintergrund und laufende Doku dazu stehen im Vault unter [`ObsidianGehirn/10 DTEW Workshop/`](../ObsidianGehirn/10%20DTEW%20Workshop) ([[DTEW Hamburg - Übersicht]], [[Team 13 - Digitale Demokratie]]).

Jedes Deliverable liegt in einem eigenen Unterordner mit `.md` (Quelldatei) + `.html` (gerendert) + ggf. `.pdf` (finale Abgabeversion), damit die vielen Formatvarianten nicht alle lose im Wurzelverzeichnis liegen:

- **[`case-analysis-worksheet/`](case-analysis-worksheet)** – ausgefülltes `case_analysis_worksheet.pdf` vom Haupt-Board (Montags-Aufgabe "First Brainstorming"), unsere 3 Cases rund um digi&demo e.V.
- **[`critical-issues-and-problem-statements/`](critical-issues-and-problem-statements)** – Mittwochs-Aufgabe (02.09.): kritische Punkte, Problem Statements, Walt-Disney-Ideation-Entwurf, Pitch-Stichpunkte fürs Peer Feedback – siehe [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]].
- **[`personas-mia-tom/`](personas-mia-tom)** – ausgefülltes `persona-template.pdf` für die beiden Proto-Personas (Mia, Tom) von Case 3, auf Desk-Research + Dienstags-Notizen basierend, **noch nicht durch echte Interviews validiert** – siehe [[DTEW 0109 - Teampathy Map und Empathize]].
- **`templates/`** – unausgefüllte Original-Vorlagen vom DTEW-Haupt-Board (Empathy Map, Persona-Template, Persona-Empathy-Map, Observation AEIOU, Problem Tree, Fiedler-Disney-Methode, Tutorial-Übersicht Design-Thinking-Methoden). Referenzmaterial, keine eigenen Deliverables.

Innerhalb jedes Deliverable-Ordners heißen die drei Dateien immer gleich wie der Ordner selbst (z. B. `personas-mia-tom/personas-mia-tom.md`), damit man beim Öffnen sofort weiß, wo man ist.

## Worum geht's

Ausgefülltes `case_analysis_worksheet.pdf` vom Haupt-Board (Case *"The Internet and Politics – Your Network, Your Rules?"*) für die Montags-Aufgabe "First Brainstorming". Alle 3 Cases (CASE 1/2/3) drehen sich um **digi&demo e.V.** (digiunddemo.de), unsere inhaltliche Richtung, verbunden über den parallel laufenden Aktionstag **"Dein Netz, Deine Regeln!"** im Bürgerhaus Wilhelmsburg (buewi.de/netz-ablauf). digi&demo nennt selbst drei Herausforderungen für offenen digitalen Diskurs – genau die drei sind unsere Cases:

1. **digi&demo – Hate Speech**
2. **digi&demo – Desinformation**
3. **digi&demo – Polarisierung**

## Neu rendern nach Änderungen an einer `.md`/`.html`

Die `.html`-Dateien sind von Hand geschrieben (kein Marp, da Formular-/Worksheet-Layout statt Folien) – bei Textänderungen `.md` **und** `.html` im jeweiligen Unterordner beide anpassen. PDF danach neu rendern, `<ordner>` durch den jeweiligen Deliverable-Ordner ersetzen:

```bash
cd DTEW-Workshop/<ordner>
npx --yes playwright install chromium   # einmalig, falls noch nicht vorhanden
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + process.cwd() + '/<ordner>.html', { waitUntil: 'networkidle' });
  await page.pdf({ path: '<ordner>.pdf', format: 'A4', printBackground: true, margin: { top: '0', bottom: '0', left: '0', right: '0' } });
  await browser.close();
})();
"
```

Beispiel für `personas-mia-tom`: `<ordner>` → `personas-mia-tom`, zusätzlich `landscape: true` in der `page.pdf(...)`-Option (Querformat, da drei Spalten pro Persona).

## Nächster Schritt

Case 3 (Feed-/Recommender-Design) ist entschieden (siehe [[Team 13 - Digitale Demokratie]]). Mittwoch 02.09.: kritische Punkte, 1–2 Problem Statements und eine Ideation-Runde (6-3-5 oder Walt-Disney) dazu ausarbeiten. Siehe [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]] im Vault.
