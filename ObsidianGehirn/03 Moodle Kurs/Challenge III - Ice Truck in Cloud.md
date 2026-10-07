---
tags: [moodle, challenges]
---

# Challenge III: "Ice Truck in Cloud"

**Schwerpunkt:** IoT in Cloud

## Szenario
Um Prozesse in der Lieferkette transparent zu machen und zu optimieren, sollen die erhobenen Daten in einer Cloud gespeichert und ausgewertet werden.

→ Baut auf [[Challenge II - Ice Truck Extension]] auf, Fokus liegt auf Cloud-Anbindung/Datenauswertung.

## Konkrete Aufgabenstellung (erhalten 30.09.2026)

**Problem:** EU-VO 178/2002 + 37/2005 verlangen Rückverfolgbarkeit und Nachweis der Temperaturen (Merkblatt LM-05-MBL-504-PM). Bisher liegen die Daten nur lokal auf dem Pi im Truck und werden erst in der Zentrale manuell ausgelesen. Dazu kommen regelmäßige Hardwareausfälle (Sensoren, Kühlaggregate) trotz Wartung.

**Ziel:** Sensordaten automatisiert in eine Cloud bringen, speichern und auswerten (Predictive Maintenance). Zeitrahmen ca. 1 Woche.

1. IoT-Plattformen recherchieren (AWS IoT Core, Azure IoT Hub, Arduino Cloud, eigener MQTT-Broker + InfluxDB auf gemieteter VM)
2. Auswahl begründen nach: Protokolle, Speicherung, Visualisierung, Kosten, Datenschutz, Einordnung IaaS/PaaS/SaaS
3. Umsetzen – Lösung muss die **5 NIST-Merkmale** (SP 800-145) erfüllen: On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service. Homeserver/Pi zu Hause zählt **nicht** als Cloud.
4. Am letzten Tag Vorstellung inkl. NIST-Begründung

## Unsere Lösung: Azure IoT Hub (PaaS)

Wir haben ein Azure-for-Students-Konto → **Azure IoT Hub F1 (kostenlos)** + Blob Storage (Archiv/Nachweis) + Azure Data Explorer Free Cluster (Dashboard, Anomalie-Erkennung). Begründung + NIST-Tabelle: `Challenge-III-Ice-Truck-Cloud/Code/ENTSCHEIDUNG.md`, Einrichtung: `Challenge-III-Ice-Truck-Cloud/Code/README.md`.

- **Edge:** `cloud-bridge/bridge.py` liest `challenge_i.db` read-only, schickt 1 Batch/Minute im Spaltenformat per MQTT/TLS (Fallback WebSockets 443) → passt ins F1-Kontingent (8.000 × 0,5 KB/Tag)
- **Store & Forward:** Cursor (`bridge_state.json`) rückt erst nach erfolgreichem Senden weiter, Funkloch wird nachgeholt
- **Health-Flags am Edge:** `temp_high`, `sensor_mismatch` (unser KY-028-Wackelkontakt!), `sensor_stuck` → Application Property `alarm` für IoT-Hub-Routing
- **Cloud:** `azure/setup.sh` (Cloud Shell) legt Hub, Device, Storage, Routen an; `azure/adx.kql` enthält Tabelle, Funktion `Readings()` und Dashboard-Abfragen
- Status 30.09.2026: Code + 8 Tests grün, SDK-Aufrufe gegen `azure-iot-device` 2.14 geprüft. **Offen:** `setup.sh` im echten Abo ausführen, Bridge auf dem Pi installieren, Offline-Test, ADX-Dashboard + Screenshots für die Präsentation → [[Offene Punkte]]

## Plan B ohne Azure: ThingSpeak (30.09.2026)
Azure-for-Students war heute nicht erreichbar → zweites Backend `CLOUD_BACKEND=thingspeak` (MathWorks, kostenlos, keine Kreditkarte). HTTPS-Bulk-Update, jede 3. Messung (15-s-Raster wegen Free-Limit 1 Request/15 s + ~3 Mio. Nachrichten/Jahr), Flags im Statusfeld, MATLAB-Auswertung/React-Alarme in ThingSpeak. 12 Tests grün, gegen echtes ThingSpeak noch nicht getestet. Anleitung: README Abschnitt „Plan B“, NIST-Begründung: `ENTSCHEIDUNG.md` Abschnitt 5.

## Alternative: IaaS mit eigener VM (Plan B / Vergleich)
Zusätzlich liegt ein vollständiger Entwurf für eigenen MQTT-Broker + InfluxDB + Grafana auf einer gemieteten VM (Docker Compose, TLS, Mosquitto-Bridge vom Pi) unter `Challenge-III-Ice-Truck-Cloud/Code/alternative-iaas-vm/`. Nicht deployt, nicht die gewählte Lösung – aber gut für die Präsentation als Vergleich IaaS (volle Kontrolle, manuelle Elastizität, Betrieb selbst) vs. PaaS (IoT Hub: verwaltet, Vendor-Bindung). Die Aufgabenstellung nennt diese Variante ausdrücklich als Option.

## Bewertungsbogen Challenge III (Stand 07.10.2026)
Quelle: Bewertungsbogen (Screenshot vom 07.10.2026, unterer Teil war abgeschnitten – falls dort weitere Zeilen stehen, hier ergänzen). Punkte stehen als „/x“ im Bogen.

| Kriterium | Punkte | Wo abgedeckt | Stand |
|---|---|---|---|
| Mindestens zwei Clouddienste werden vorgestellt | /5 | `ENTSCHEIDUNG.md` Abschnitt 1 (Azure IoT Hub, AWS IoT Core, Arduino Cloud, eigene VM) + ThingSpeak (Abschnitt 5) | Text fertig, in Präsentation aufnehmen |
| Entscheidung technisch begründet | /5 | `ENTSCHEIDUNG.md` Abschnitt 2 (Protokolle, Speicherung, Kosten, Datenschutz) | Text fertig. **Achtung:** gewählt/umgesetzt ist jetzt ThingSpeak, Begründung in Präsentation entsprechend darstellen (Azure war nicht erreichbar) |
| NIST-Kriterien erfüllt bzw. Abweichungen begründet | /5 | `ENTSCHEIDUNG.md` Abschnitt 3 (Azure) und Abschnitt 5 (ThingSpeak) | Text fertig, für ThingSpeak prüfen, ob Resource Pooling/Elasticity/Measured Service sinnvoll begründet sind |
| Einordnung IaaS / PaaS / SaaS begründet | /5 | ThingSpeak = **SaaS** (fertige Plattform, nur Konfiguration), Azure IoT Hub = PaaS, eigene VM = IaaS | In Präsentation klar benennen |
| Einschätzung Datensicherheit und DSGVO | /5 | `ENTSCHEIDUNG.md` Abschnitt 4 und 5 (ThingSpeak: Server USA, Drittlandübermittlung, Temperaturdaten ohne Personenbezug vertretbar) | Text fertig |
| Konzept sichere Datenübertragung | /10 | HTTPS/TLS zum Cloud-Dienst, Write-API-Key nur in `.env` auf dem Pi, Discord-Webhook-URL nur in ThingSpeak (nicht im Repo), Azure-Variante MQTT über TLS 1.2 mit Device-Schlüssel | Als eigene Folie ausarbeiten (Pi → TLS → Cloud, Schlüssel, nichts im Repo) |
| Messdaten in Cloud protokolliert und visualisierbar | /10 | ThingSpeak-Channel: jeder Messwert mit Original-Zeitstempel (`created_at`), Diagramme in der Private View, CSV-Export als Nachweis | Screenshots machen, CSV-Export zeigen |
| Zusätzliche Funktionen realisiert | /5 | Discord-Alarm bei Temperatur über 30 °C (siehe unten), Store & Forward, Health-Flags, Sensor-Drift-Auswertung | Discord-Alarm läuft |

## Discord-Alarm über ThingSpeak (07.10.2026)
Läuft komplett in der Cloud, der Pi wird nicht gebraucht: **React** (Field 3 > 30, „On Data Insertion“, Option „nur beim ersten Mal ausführen“) → **ThingHTTP** (POST an Discord-Webhook, `application/json`) → Nachricht im Teamkanal.

- Test ohne Pi: `https://api.thingspeak.com/update?api_key=<WRITE_KEY>&field3=35` (Write-Key nie ins Repo/in den Chat). Dazwischen einen Wert unter 30 schicken, sonst löst „nur das erste Mal“ nicht erneut aus. Free-Limit: etwa alle 15 s ein Wert.
- Webhook-URL ist wie ein Passwort: nur in ThingHTTP, nicht ins Repo.
- **Stolperfallen:** (1) Emojis im Body werden zu `????` → weglassen. (2) `%%channel_<ID>_field_3%%` muss die echte Channel-ID enthalten und mit `%%` getippt sein, sonst steht `%25%25…` in der Nachricht. (3) Platzhalter-Wert war bei uns leer, wenn ThingHTTP nicht von React ausgelöst wird; Fallback: Text ohne Wert, oder MATLAB Analysis mit `sprintf`/`webwrite`.
- **Protokollierung:** Discord setzt zu jeder Nachricht selbst Datum und Uhrzeit. Der eigentliche Nachweis ist der ThingSpeak-Channel mit Zeitstempel (CSV-Export des Alarmzeitraums + Discord-Screenshot). Optional: MATLAB Analysis schreibt Alarme in einen zweiten Channel („Alarm-Log“).
- Bot-Profilbild im Discord-Webhook auf neutrales Icon (Thermometer/Warnschild) stellen statt Foto.

## Relevante Kursinhalte
- "Datenbankanbindung und Object-Relational Mapping" (Kurs-ID 564) – **benötigt Einschreibekennwort**, siehe [[Offene Punkte]]

## Prüfungsbezug
Nach dieser Challenge: Fachgespräch (40%), siehe [[Leistungsnachweise]]

#moodle #challenges
