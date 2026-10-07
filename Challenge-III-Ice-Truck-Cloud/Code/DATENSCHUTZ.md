# Datensicherheit und DSGVO-Einschätzung

Bewertet wird die laufende Lösung: Messdaten vom Raspberry Pi im Truck nach **ThingSpeak**
(MathWorks, USA). Technische Einzelheiten zur Absicherung: [`SICHERHEITSKONZEPT.md`](SICHERHEITSKONZEPT.md).

> Keine Rechtsberatung. Es ist die Einschätzung von Schülern auf Grundlage der DSGVO und der
> Anbieterangaben. Punkte mit **[PRÜFEN]** müssen vor der Abgabe nachgesehen und hier
> eingetragen werden.

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

## 2. Ist die DSGVO anwendbar?

- Personenbezogene Daten sind nach Art. 4 Nr. 1 DSGVO alle Informationen über eine
  identifizierte oder identifizierbare Person. Reine Temperaturmesswerte eines Prototyp-Trucks
  gehören nicht dazu.
- **Im Prototyp** sehen wir deshalb keinen Personenbezug. Die DSGVO greift nicht, wir halten die
  Grundsätze aber freiwillig ein (Datenminimierung, Zweckbindung, Sicherheit).
- **Im Realbetrieb** kann sich das ändern: Wird die Truck-ID mit Dienstplänen oder Fahrern
  verknüpft, werden Temperatur- und Zeitdaten indirekt personenbezogen (Beschäftigtendaten).
  Dann brauchen wir eine Rechtsgrundlage (z. B. berechtigtes Interesse nach Art. 6 Abs. 1
  lit. f oder gesetzliche Pflicht für den Nachweis), eine Information der Betroffenen
  (Art. 13) und je nach Fall eine Beteiligung des Betriebsrats. GPS-Daten würden diese
  Pflichten auf jeden Fall auslösen.

## 3. Drittlandübermittlung (USA)

- ThingSpeak wird von MathWorks betrieben. Wir behandeln die Server als **in den USA**
  stehend. Eine Übermittlung dorthin wäre bei personenbezogenen Daten eine Übermittlung
  in ein Drittland (DSGVO Kapitel V, Art. 44 ff.).
- Mögliche Grundlagen: Angemessenheitsbeschluss zum **EU-US Data Privacy Framework**, falls
  der Anbieter zertifiziert ist, sonst **Standardvertragsklauseln** mit Zusatzmaßnahmen.
- **[PRÜFEN]** Steht MathWorks auf der Liste unter https://www.dataprivacyframework.gov
  (Suche „MathWorks“)? Ergebnis: `[ja / nein, Datum eintragen]`
- Für den Prototyp ohne Personenbezug ist die Übermittlung unkritisch. Im Realbetrieb mit
  Personendaten wäre eine **EU-Region** (z. B. Azure Germany West Central) vorzuziehen.

## 4. Auftragsverarbeitung

- Würden personenbezogene Daten verarbeitet, wäre MathWorks **Auftragsverarbeiter**. Dann ist
  ein Vertrag nach Art. 28 DSGVO (Auftragsverarbeitungsvertrag / Data Processing Addendum)
  nötig.
- **[PRÜFEN]** Bietet MathWorks ein DPA für ThingSpeak an, und gilt es auch für den
  Free-Tarif? Ergebnis: `[ja / nein, Fundstelle eintragen]`
- Zusätzlich: Datenschutzerklärung und Nutzungsbedingungen von MathWorks/ThingSpeak lesen.
  Wichtig sind Speicherort, Speicherdauer, Weitergabe an Dritte und ob der Free-Tarif für
  gewerbliche Nutzung erlaubt ist (er ist laut Anbieter nur für nicht-kommerzielle Nutzung
  gedacht). **[PRÜFEN]**

## 5. Datensicherheit: technische und organisatorische Maßnahmen (Art. 32 DSGVO)

| Schutzziel | Maßnahme |
|---|---|
| **Vertraulichkeit** | HTTPS/TLS auf dem Transportweg; Kanal ist privat; getrennte Schlüssel für Schreiben und Lesen; Schlüssel nur in `.env` mit `chmod 600`, nicht im Git; nur das Team hat Zugriff auf das ThingSpeak-Konto |
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

- Die Nachweispflicht verlangt längere Aufbewahrung der Temperaturaufzeichnungen. Die
  genaue Frist hängt vom Produkt ab **[PRÜFEN: Frist in der Aufgabenstellung bzw. im Merkblatt
  nachlesen]**.
- Originaldaten bleiben in der lokalen Datenbank. Die Speicherdauer in ThingSpeak richtet
  sich nach den Bedingungen des Anbieters **[PRÜFEN]**. Deshalb zusätzlich regelmäßig als
  CSV exportieren und sicher ablegen.
- Betroffenenrechte (Auskunft, Löschung) greifen nur, wenn Personenbezug entsteht. Löschen
  geht im Kanal (*Channel → Clear Channel Data* bzw. Kanal löschen).

## 7. Ergebnis der Einschätzung

| Frage | Einschätzung |
|---|---|
| Personenbezogene Daten im Prototyp? | **Nein.** Nur Fahrzeug-ID, Temperaturen, Aktorwerte, Zeit |
| DSGVO-Risiko durch USA-Server? | **Gering**, solange kein Personenbezug besteht |
| Technische Absicherung ausreichend? | **Für den Prototyp ja**, mit den benannten Restrisiken |
| Reicht das für den Flottenbetrieb? | **Nein, nicht unverändert.** Vorher: EU-Region (Azure IoT Hub), Auftragsverarbeitungsvertrag, unveränderliches Archiv, Schlüssel pro Truck |

## 8. Prüfliste vor der Abgabe (bitte abhaken)

- [ ] MathWorks im Data Privacy Framework nachgeschlagen und Ergebnis in Abschnitt 3 eingetragen
- [ ] DPA / Datenschutzerklärung von MathWorks gelesen, Ergebnis in Abschnitt 4 eingetragen
- [ ] Nutzungsbedingungen des Free-Tarifs gelesen (nicht-kommerziell, Limits, Speicherdauer)
- [ ] Aufbewahrungsfrist aus der Aufgabe / dem Merkblatt in Abschnitt 6 eingetragen
- [ ] Im ThingSpeak-Kanal: *Sharing* steht auf „Keep channel view private“
- [ ] Write und Read Key neu erzeugt (beide standen im Chat), neuen Write Key in `.env` eingetragen
- [ ] Screenshots für die Folien: TLS-Nachweis (`curl -sv`), `ls -l .env`, Kanal-Einstellung „privat“
