# DTEW Hamburg – Digitale Demokratie (Team 13)

Deliverables für den zusätzlichen "2026 International Design Thinking and Entrepreneurship Workshop Hamburg" (31.08.–12.09.2026), separat vom eigentlichen Smart-Systems-Pi-Projekt. Hintergrund und laufende Doku dazu stehen im Vault unter [`ObsidianGehirn/10 DTEW Workshop/`](../ObsidianGehirn/10%20DTEW%20Workshop) ([[DTEW Hamburg - Übersicht]], [[Team 13 - Digitale Demokratie]]).

- **`case-analysis-worksheet.md`** – Quelldatei (Markdown), die bei Änderungen bearbeitet werden sollte. **Auf Englisch**, wie der Workshop (internationales Team, Original-Worksheet ist auch Englisch).
- **`case-analysis-worksheet.html`** – fertig gerenderte Version zum direkten Anzeigen im Browser (eigenständig, kein Marp/Build-Schritt nötig).
- **`case-analysis-worksheet.pdf`** – PDF-Version im Layout des Original-Worksheets vom DTEW-Haupt-Board, ausgefüllt mit unseren 3 Cases – das ist das eigentliche Abgabe-Dokument für den Workshop.

## Worum geht's

Ausgefülltes `case_analysis_worksheet.pdf` vom Haupt-Board (Case *"The Internet and Politics – Your Network, Your Rules?"*) für die Montags-Aufgabe "First Brainstorming". Die 3 Cases (CASE 1/2/3) sind nicht erfunden, sondern aus der echten Ausstellerliste des parallel laufenden Aktionstags **"Dein Netz, Deine Regeln!"** im Bürgerhaus Wilhelmsburg hergeleitet (buewi.de/netz-ablauf):

1. **juuuport** – Cybermobbing/Hate Speech gegen Einzelpersonen
2. **Amadeu Antonio Stiftung / HateShield** – koordinierte Hassangriffe gegen Communities
3. **digi&demo** – Desinformation/manipulierte Inhalte

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

Mittwoch: einen der drei Cases als Fokus wählen und daraus 1–2 Problem Statements bauen (Case 1 und 3 passen am ehesten zu "digitale Demokratie" im engeren Sinn). Siehe [[Team 13 - Digitale Demokratie]] im Vault.
