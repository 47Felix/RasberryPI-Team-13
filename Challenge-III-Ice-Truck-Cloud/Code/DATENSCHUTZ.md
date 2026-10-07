# Datensicherheit und DSGVO-Einschätzung

Bewertet wird die laufende Lösung: Messdaten vom Raspberry Pi im Truck nach **ThingSpeak**
(MathWorks, USA). Technische Einzelheiten zur Absicherung: [`SICHERHEITSKONZEPT.md`](SICHERHEITSKONZEPT.md).

> Keine Rechtsberatung. Es ist die Einschätzung von Schülern auf Grundlage der DSGVO und der
> Anbieterangaben.
> **Quellen (Stand 30.09.2026):**
> [MathWorks Privacy Policy](https://www.mathworks.com/company/trust-center/privacy-policy.html)
> (aktualisiert am 25.03.2026), [ThingSpeak Licensing FAQ](https://thingspeak.mathworks.com/pages/license_faq),
> [ThingSpeak License Options](https://thingspeak.mathworks.com/prices).
> Mit **[PRÜFEN]** sind Punkte markiert, die noch nachgesehen werden müssen.

## 1. Welche Daten werden übertragen?

| Datum | Beispiel | Personenbezug? |
|---|---|---|
| Truck-ID | `icetruck-team13-1` | nein, eine Fahrzeugkennung des Prototyps |
| Temperaturen (2 Sensoren, Mittelwert) | 6,8 °C | nein |
| Rohwerte der Sensoren, Digitalwert | 190 | nein |
| Lüfter- und Ventilstellung | 120 / 0 | nein |
| Zeitstempel (UTC), lokale Messungs-ID | 2026-09-30T08:00:00+00:00, 4711 | nein |
| Statusflags | `temp_high`, `sensor_mismatch` | nein |

**Nicht** übertragen werden: Namen, Fahrer-IDs, Standort/GPS, Kontaktdaten, Kennzeichen,
Kundendaten.

**Aber:** Für ThingSpeak braucht man ein **MathWorks-Konto**. Dort liegen Name, E-Mail-Adresse
und Land der Person, die es angelegt hat. Das sind die einzigen personenbezogenen Daten in
unserer Lösung. Sie verarbeitet MathWorks in eigener Verantwortung (Privacy Policy, Teil 1 Nr. 1
und Teil 2 Nr. 1). Daher: nur Teammitglieder mit eigener, freiwilliger Anmeldung, keine
Angaben Dritter.

## 2. Ist die DSGVO anwendbar?

- Personenbezogene Daten sind nach Art. 4 Nr. 1 DSGVO alle Informationen über eine
  identifizierte oder identifizierbare Person. Reine Temperaturmesswerte eines Prototyp-Trucks
  gehören nicht dazu.
- **Im Prototyp** sehen wir deshalb bei den Messdaten keinen Personenbezug. Wir halten die
  Grundsätze trotzdem freiwillig ein (Datenminimierung, Zweckbindung, Sicherheit).
- **Im Realbetrieb** kann sich das ändern: Wird die Truck-ID mit Dienstplänen oder Fahrern
  verknüpft, werden Temperatur- und Zeitdaten indirekt personenbezogen (Beschäftigtendaten).
  Dann brauchen wir eine Rechtsgrundlage (z. B. berechtigtes Interesse nach Art. 6 Abs. 1
  lit. f), eine Information der Betroffenen (Art. 13) und je nach Fall eine Beteiligung des
  Betriebsrats. GPS-Daten würden diese Pflichten auf jeden Fall auslösen.

## 3. Drittlandübermittlung (USA)

Das sagt MathWorks selbst (Privacy Policy):

- **Speicherort:** „Wir können Ihre Daten außerhalb Ihres Aufenthaltslandes speichern, wo immer
  wir oder unsere Drittserviceanbieter arbeiten“ (Teil 1 Nr. 3). Eine Speicherung in der EU
  wird **nicht** zugesagt. Wir gehen von den USA aus.
- **Rechtsgrundlage für den Transfer:** MathWorks erklärt, die Anforderungen des **EU-US Data
  Privacy Framework (DPF)**, der UK-Erweiterung und des Swiss-US DPF zu erfüllen
  (Teil 1 Nr. 7, „Datenschutzrahmen“). Damit läge für personenbezogene Daten ein
  Angemessenheitsbeschluss zugrunde (DSGVO Kapitel V, Art. 45).
- **Streitbeilegung:** unabhängiger Mechanismus über BBB National Programs; MathWorks
  unterliegt der Aufsicht der US-Behörde FTC.
- **Vertretung in der EU:** The MathWorks GmbH, Weihenstephaner Str. 6, 81673 München.
- **Kontakt für Datenschutzanfragen:** privacy@mathworks.com.
- **Geprüft am 07.10.2026** im offiziellen Verzeichnis ([Data Privacy Framework List](https://dataprivacyframework.gov/list),
  Suche „The MathWorks“): **The MathWorks, Inc., Natick (MA), aktiver Teilnehmer.**

  | Rahmen | Status | Erstzertifizierung | Nächste Zertifizierung fällig |
  |---|---|---|---|
  | EU-U.S. Data Privacy Framework | **Active** | 16.11.2016 | 07.07.2027 |
  | UK-Erweiterung | **Active** | 07.08.2023 | 07.07.2027 |
  | Swiss-U.S. Data Privacy Framework | **Active** | 18.05.2017 | 07.07.2027 |

  Abgedeckte Datenart: **Non-HR Data** (keine Beschäftigtendaten). Prüfmethode:
  Selbstbewertung. Streitbeilegung über BBB National Programs, Aufsicht durch die FTC.
  Verbindliche Datenschutzerklärung im Verzeichnis: Privacy Policy, gültig ab 25.03.2026.

**Bewertung:** Für unsere Messdaten ohne Personenbezug ist die Übermittlung unkritisch. Für die
Kontodaten der Teammitglieder stützt sich MathWorks auf das DPF, und die Zertifizierung ist aktiv.
**Wichtig:** Das DPF-Zertifikat deckt nur Nicht-Beschäftigtendaten („Non-HR Data“) ab. Würden wir
später **Fahrerdaten** übertragen, wären das Beschäftigtendaten, für die die Zertifizierung nicht
gilt. Dann bräuchte es eine andere Grundlage (z. B. Standardvertragsklauseln). Im Realbetrieb mit
Personendaten wäre daher eine **EU-Region** (z. B. Azure Germany West Central) die sicherere
Wahl, weil dort auch der Speicherort zugesagt werden kann.

## 4. Auftragsverarbeitung und Nutzungsbedingungen

- Würden personenbezogene Daten **unserer** Kunden oder Fahrer verarbeitet, wäre MathWorks
  Auftragsverarbeiter. Dann ist ein Vertrag nach Art. 28 DSGVO nötig.
- **Befund:** In der Privacy Policy steht **kein** Auftragsverarbeitungsvertrag (DPA) für
  ThingSpeak-Kunden. Dort steht nur, dass MathWorks Daten an Dienstleister nur unter Verträgen
  weitergibt, die diese zum Datenschutz verpflichten (Teil 1 Nr. 4). Für den Prototyp ist das
  unkritisch, für den Realbetrieb mit Personendaten müsste vorher ein DPA bei
  privacy@mathworks.com angefragt werden.
- **Lizenz (Licensing FAQ, License Options):** Der Free-Tarif gilt für **nicht-kommerzielle
  kleine Projekte**: unter 3 Mio. Nachrichten pro Jahr (ca. 8.200 pro Tag), 4 Kanäle, Update-Intervall
  15 Sekunden, ein Free-Konto pro Person. Das passt zu einem Schulprojekt. Die Lizenzen
  „Academic“ und „Student“ gelten für Einrichtungen, die Abschlüsse vergeben („degree-granting
  institution“), „Home“ nur für Privatnutzung. **Ein Unternehmen mit echten Trucks braucht die
  kostenpflichtige Standard-Lizenz**, der Free-Tarif wäre dort nicht erlaubt.

## 5. Datensicherheit: technische und organisatorische Maßnahmen (Art. 32 DSGVO)

| Schutzziel | Maßnahme |
|---|---|
| **Vertraulichkeit** | HTTPS/TLS auf dem Transportweg; Schreiben nur mit dem geheimen Write Key; getrennte Keys für Schreiben und Lesen, bereits einmal erneuert und jederzeit zurücksetzbar (Privacy Policy, Teil 2 Nr. 11); Keys nur in `.env` mit `chmod 600`, nicht im Git; Alarm-Zugangsdaten (Discord-Webhook, Alerts-Key) nur in ThingSpeak. Der **Kanal ist bewusst öffentlich** (siehe 5a), weil er keine sensiblen Daten enthält |
| **Integrität** | Messdatenbank wird von der Bridge nur gelesen; jede Messung hat eine ID; Cursor wird atomar geschrieben; Originaldaten bleiben lokal |
| **Verfügbarkeit** | Lokaler Puffer (SQLite) und Nachholen nach Funkloch (Store and Forward); Daten liegen doppelt (Pi und Cloud) |
| **Belastbarkeit** | Dienst startet bei Fehlern neu (`Restart=on-failure`), Netzfehler stoppen die Bridge nicht |
| **Datenminimierung** | Nur Felder, die für Nachweis und Wartung nötig sind; kein GPS, keine Fahrerdaten |
| **Nachvollziehbarkeit** | UTC-Zeitstempel und lokale ID je Messung; Dienst-Log mit `journalctl` |
| **Organisatorisch** | Key-Rotation nach Bekanntwerden (Anleitung im Sicherheitskonzept); Passwörter und Keys nicht in Chats oder Folien |

Bekannte Lücken (ehrlich benannt, mit Plan im Sicherheitskonzept): das Pi-Terminal ohne
Anmeldung, der Klartext-Key in `.env`, kein unveränderliches Archiv bei ThingSpeak, keine
Batterie-Uhr im Pi.

## 5a. Warum der Kanal öffentlich ist

**Entscheidung:** Der ThingSpeak-Kanal bleibt für den Prototyp **öffentlich**.

**Gründe:**
1. Er enthält nur **nicht-sensible Messdaten**: Temperaturen, Lüfter- und Ventilwerte, Zeitstempel und
   eine Fahrzeugkennung. Kein Personenbezug, keine Kundendaten, kein GPS (siehe Abschnitt 1).
2. **Transparenz passt zum Ziel der Aufgabe:** Die Temperaturverläufe sollen bei Kontrollen
   „jederzeit und ortsunabhängig“ nachweisbar sein. Prüfer, Lehrkraft und Mitschüler können den
   Verlauf ohne Anmeldung ansehen.
3. **Schreiben bleibt geschützt.** Öffentliches Lesen ändert nichts daran, dass nur mit dem
   geheimen Write Key Daten in den Kanal geschrieben werden können. Fälschungen bleiben damit
   ausgeschlossen, solange der Key geheim ist.

**Folgen und Risiken:**
- Jeder mit dem Link sieht die Verläufe und damit auch die **Betriebszeiten** des Trucks.
- Bei öffentlichen Kanälen zeigt MathWorks Angaben zum Konto und einen Link zum Profil
  (Privacy Policy, Teil 2 Nr. 11). Bei uns erscheint als Autor die MathWorks-Kennung
  (`mwa…`). Im MathWorks-Profil sollten deshalb **keine Klarnamen, Fotos oder E-Mail-Adressen**
  öffentlich stehen.
- Dritte könnten die Daten kopieren. Das ist bei reinen Temperaturdaten vertretbar.

**Im Realbetrieb** wäre der Kanal **privat**: Zugriff für Behörden und Mitarbeiter über *Sharing →
Share channel view only with the following users* (im Free-Tarif für bis zu drei weitere Personen)
oder über den Read Key.

## 6. Speicherdauer und Löschung

- **Speicherlimit im Free-Tarif:** bis zu **10 Millionen Nachrichten** pro Nutzer (Licensing
  FAQ, Frage 23). Ist es voll, können Kanäle keine neuen Daten mehr annehmen. Außerdem nimmt ein Kanal
  nach Ausschöpfen des Jahreskontingents keine Daten mehr an (Frage 12), ThingSpeak versucht
  vorher zu warnen (Fragen 17 und 18). Dann puffert der Pi weiter lokal.
- **Allgemeine Aufbewahrung:** MathWorks bestimmt die Dauer „entsprechend Zweck und Nutzen“, eine
  feste Frist nennt die Privacy Policy nicht (Teil 1 Nr. 3). Langzeitarchivierung bietet
  MathWorks nur Bezahlkunden an (FAQ Frage 23). Deshalb: **Originale bleiben in der lokalen
  Datenbank, zusätzlich regelmäßig als CSV exportieren und sicher ablegen.**
- **Aufbewahrungsfrist (Festlegung des Teams):** Aufgabenstellung und Merkblatt nennen uns keine
  konkrete Frist. Wir legen für unser Konzept fest: **mindestens 12 Monate** lückenlos abrufbar.
  Begründung: Eine Jahresfrist ist eine übliche Dokumentationsdauer für Temperaturaufzeichnungen
  (Annahme, nicht geprüft). Sie passt zur Lizenzlaufzeit der Free-Lizenz (*My Account*: gültig bis
  29.09.2027) und zum Jahreskontingent von 3 Mio. Nachrichten.
  **Umsetzung:** 12 Monate online im ThingSpeak-Kanal, dazu **monatlicher CSV-Export** als zweites
  Archiv. Die lokale Datenbank bleibt das Original und wird erst nach Ablauf der 12 Monate
  archiviert oder gelöscht. Im Realbetrieb muss die gesetzlich geforderte Frist vorher geklärt
  werden (Merkblatt LM-05-MBL-504-PM bzw. zuständige Behörde), z. B. mit längerer Archivierung
  im Azure Blob Storage mit Immutability.
- **Löschen und Betroffenenrechte:** Daten im Kanal löschen geht über *Channel → Clear Channel
  Data* bzw. den Kanal löschen. Betroffenenrechte (Auskunft, Löschung, Berichtigung) für die
  Kontodaten bearbeitet MathWorks über privacy@mathworks.com und das
  „Data Subject Access Request“-Formular. Für unsere Messdaten greifen sie nur, wenn
  Personenbezug entsteht.

## 7. Ergebnis der Einschätzung

| Frage | Einschätzung |
|---|---|
| Personenbezogene Daten im Prototyp? | **Messdaten: nein.** Personenbezogen sind nur die Kontodaten der Teammitglieder bei MathWorks |
| DSGVO-Risiko durch USA-Server? | **Gering**, solange kein Personenbezug besteht. MathWorks ist im Data Privacy Framework aktiv gelistet, das gilt aber nicht für Beschäftigtendaten |
| Ist der öffentliche Kanal vertretbar? | **Für den Prototyp ja**: nur nicht-sensible Messdaten, Schreiben nur mit Write Key. **Im Realbetrieb nein**, dort privat mit Freigabe für Berechtigte |
| Technische Absicherung ausreichend? | **Für den Prototyp ja**, mit den benannten Restrisiken |
| Free-Tarif für den Betrieb erlaubt? | **Für das Schulprojekt ja** (nicht-kommerziell). Ein Unternehmen braucht die Standard-Lizenz |
| Reicht das für den Flottenbetrieb? | **Nein, nicht unverändert.** Vorher: Standard-Lizenz, EU-Region (z. B. Azure IoT Hub), Auftragsverarbeitungsvertrag, unveränderliches Archiv, Schlüssel pro Truck |

## 8. Prüfliste vor der Abgabe (bitte abhaken)

- [x] Privacy Policy gelesen: Speicherort weltweit, DPF-Erklärung, Datenschutzvertreter in München, kein DPA für Kunden erwähnt
- [x] Licensing FAQ gelesen: Free-Lizenz nicht-kommerziell, 3 Mio. Nachrichten pro Jahr, 4 Kanäle, 15 s, 10 Mio. gespeicherte Nachrichten
- [x] Im Verzeichnis dataprivacyframework.gov „The MathWorks“ gesucht (07.10.2026): aktiv, Ergebnis in Abschnitt 3 und auf Folie 9 eingetragen
- [x] Aufbewahrungsfrist festgelegt: 12 Monate (Annahme des Teams, in Abschnitt 6 begründet, im Realbetrieb prüfen)
- [x] Kanal bewusst **öffentlich** und begründet (Abschnitt 5a)
- [ ] Im MathWorks-Profil geprüft, was öffentlich sichtbar ist (kein Klarname, kein Foto, keine E-Mail)
- [x] Unter *My Account* Restkontingent fotografiert (07.10.2026): 2.999.270 von 3.000.000 Nachrichten übrig, 3 von 4 Kanälen frei, 798 von 800 Alarm-Mails übrig
- [x] Write und Read Key (außerdem Alerts-Key und Discord-Webhook) neu erzeugt
- [ ] Neuen Write Key in der `.env` auf dem Pi eingetragen und geprüft (`journalctl -u cloud-bridge -n 20`, keine Fehlermeldung)
- [ ] Screenshots für die Folien: TLS-Nachweis (`curl -sv`), `ls -l .env`, Kanal-Einstellung
