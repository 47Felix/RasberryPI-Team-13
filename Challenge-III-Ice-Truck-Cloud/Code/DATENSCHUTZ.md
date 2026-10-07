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
- **[PRÜFEN]** Eintrag im offiziellen Verzeichnis: https://www.dataprivacyframework.gov/s/ →
  „Participant Search“ → nach **„The MathWorks“** suchen (so schreibt es die Privacy Policy).
  Ergebnis: `[aktiv / nicht gefunden, Datum eintragen]`

**Bewertung:** Für unsere Messdaten ohne Personenbezug ist die Übermittlung unkritisch. Für die
Kontodaten der Teammitglieder stützt sich MathWorks auf das DPF. Im Realbetrieb mit Personendaten
wäre eine **EU-Region** (z. B. Azure Germany West Central) die sicherere Wahl, weil dort der
Speicherort zugesagt werden kann.

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
| **Vertraulichkeit** | HTTPS/TLS auf dem Transportweg; Kanal ist **privat** (bei öffentlichen Kanälen zeigt MathWorks den Kontonamen und einen Link zum Profil an, Teil 2 Nr. 11); private Daten sind mit API-Keys geschützt, die jederzeit zurückgesetzt werden können; getrennte Keys für Schreiben und Lesen; Keys nur in `.env` mit `chmod 600`, nicht im Git |
| **Integrität** | Messdatenbank wird von der Bridge nur gelesen; jede Messung hat eine ID; Cursor wird atomar geschrieben; Originaldaten bleiben lokal |
| **Verfügbarkeit** | Lokaler Puffer (SQLite) und Nachholen nach Funkloch (Store and Forward); Daten liegen doppelt (Pi und Cloud) |
| **Belastbarkeit** | Dienst startet bei Fehlern neu (`Restart=on-failure`), Netzfehler stoppen die Bridge nicht |
| **Datenminimierung** | Nur Felder, die für Nachweis und Wartung nötig sind; kein GPS, keine Fahrerdaten |
| **Nachvollziehbarkeit** | UTC-Zeitstempel und lokale ID je Messung; Dienst-Log mit `journalctl` |
| **Organisatorisch** | Key-Rotation nach Bekanntwerden (Anleitung im Sicherheitskonzept); Passwörter und Keys nicht in Chats oder Folien |

Bekannte Lücken (ehrlich benannt, mit Plan im Sicherheitskonzept): das Pi-Terminal ohne
Anmeldung, der Klartext-Key in `.env`, kein unveränderliches Archiv bei ThingSpeak, keine
Batterie-Uhr im Pi.

## 6. Speicherdauer und Löschung

- **Speicherlimit im Free-Tarif:** bis zu **10 Millionen Nachrichten** pro Nutzer (Licensing
  FAQ, Frage 23). Ist es voll, können Kanäle keine neuen Daten mehr annehmen. Außerdem nimmt ein Kanal
  nach Ausschöpfen des Jahreskontingents keine Daten mehr an (Frage 12), ThingSpeak versucht
  vorher zu warnen (Fragen 17 und 18). Dann puffert der Pi weiter lokal.
- **Allgemeine Aufbewahrung:** MathWorks bestimmt die Dauer „entsprechend Zweck und Nutzen“, eine
  feste Frist nennt die Privacy Policy nicht (Teil 1 Nr. 3). Langzeitarchivierung bietet
  MathWorks nur Bezahlkunden an (FAQ Frage 23). Deshalb: **Originale bleiben in der lokalen
  Datenbank, zusätzlich regelmäßig als CSV exportieren und sicher ablegen.**
- **[PRÜFEN]** Aufbewahrungsfrist für Temperaturaufzeichnungen aus Aufgabenstellung bzw. Merkblatt
  LM-05-MBL-504-PM nachlesen: `[Frist eintragen]`
- **Löschen und Betroffenenrechte:** Daten im Kanal löschen geht über *Channel → Clear Channel
  Data* bzw. den Kanal löschen. Betroffenenrechte (Auskunft, Löschung, Berichtigung) für die
  Kontodaten bearbeitet MathWorks über privacy@mathworks.com und das
  „Data Subject Access Request“-Formular. Für unsere Messdaten greifen sie nur, wenn
  Personenbezug entsteht.

## 7. Ergebnis der Einschätzung

| Frage | Einschätzung |
|---|---|
| Personenbezogene Daten im Prototyp? | **Messdaten: nein.** Personenbezogen sind nur die Kontodaten der Teammitglieder bei MathWorks |
| DSGVO-Risiko durch USA-Server? | **Gering**, solange kein Personenbezug besteht. MathWorks beruft sich auf das Data Privacy Framework |
| Technische Absicherung ausreichend? | **Für den Prototyp ja**, mit den benannten Restrisiken |
| Free-Tarif für den Betrieb erlaubt? | **Für das Schulprojekt ja** (nicht-kommerziell). Ein Unternehmen braucht die Standard-Lizenz |
| Reicht das für den Flottenbetrieb? | **Nein, nicht unverändert.** Vorher: Standard-Lizenz, EU-Region (z. B. Azure IoT Hub), Auftragsverarbeitungsvertrag, unveränderliches Archiv, Schlüssel pro Truck |

## 8. Prüfliste vor der Abgabe (bitte abhaken)

- [x] Privacy Policy gelesen: Speicherort weltweit, DPF-Erklärung, Datenschutzvertreter in München, kein DPA für Kunden erwähnt
- [x] Licensing FAQ gelesen: Free-Lizenz nicht-kommerziell, 3 Mio. Nachrichten pro Jahr, 4 Kanäle, 15 s, 10 Mio. gespeicherte Nachrichten
- [ ] Im Verzeichnis dataprivacyframework.gov „The MathWorks“ gesucht, Ergebnis in Abschnitt 3 und auf Folie 9 eingetragen
- [ ] Aufbewahrungsfrist aus Aufgabe/Merkblatt in Abschnitt 6 eingetragen
- [ ] Im ThingSpeak-Kanal: *Sharing* steht auf „Keep channel view private“ (Screenshot)
- [ ] Unter *My Account* Restkontingent und Verbrauch fotografiert (Beleg für „Measured Service“)
- [ ] Write und Read Key neu erzeugt (beide standen im Chat), neuen Write Key in `.env` eingetragen
- [ ] Screenshots für die Folien: TLS-Nachweis (`curl -sv`), `ls -l .env`, Kanal-Einstellung „privat“
