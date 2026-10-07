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

## Unsere Lösung: ThingSpeak (SaaS), Plan A war Azure IoT Hub

**Entscheidung:** ThingSpeak (MathWorks), eingeordnet als **SaaS**. Plan A war Azure IoT Hub (PaaS); Code und Setup-Skript sind fertig (`azure/`), liefen aber nie, weil der Zugang zum Azure-Schülerkonto am 30.09.2026 nicht funktionierte. Die Übertragung läuft seitdem mit demselben Bridge-Code nach ThingSpeak (Kanal läuft, von Felix bestätigt).

Dokumente im Repo (`Challenge-III-Ice-Truck-Cloud/Code/`):
- `ENTSCHEIDUNG.md`: Vergleich (ThingSpeak, Azure, AWS, Arduino Cloud, eigene VM), Begründung, Einordnung SaaS, NIST-Tabelle mit Einschränkungen
- `SICHERHEITSKONZEPT.md`: sichere Datenübertragung (HTTPS, getrennte Keys, `.env` chmod 600, Cursor, read-only DB), Key-Rotation, Nachweis-Befehle, Restrisiken
- `DATENSCHUTZ.md`: Datensicherheit und DSGVO (kein Personenbezug im Prototyp, USA-Server, Auftragsverarbeitung, Prüfliste)
- `README.md`: Einrichtung, Store and Forward erklärt, Alarme und MATLAB

Technik:
- **Edge:** `cloud-bridge/bridge.py` liest `challenge_i.db` read-only und schickt per HTTPS-Bulk-Update. 5-s-Betrieb mit `THINGSPEAK_DOWNSAMPLE=1`, `SEND_INTERVAL_SECONDS=15` (Free: 1 Request/15 s, ~3 Mio. Nachrichten/Jahr, bei jeder Messung ca. 6 Monate Kontingent)
- **Store & Forward:** DB ist der Puffer, Cursor (`bridge_state.json`) rückt erst nach bestätigtem Senden weiter, verpasste Messungen kommen mit Originalzeit nach
- **Health-Flags am Edge:** `temp_high`, `sensor_mismatch` (unser KY-028-Wackelkontakt), `sensor_stuck` im Statusfeld
- 12 Tests grün (`cloud-bridge/tests/`)
- Präsentation entlang des Bewertungsbogens (13 Folien, Sprecher Anton/Dogan/Erik/Felix, Sprechtext in den Notizen): `Challenge-III-Ice-Truck-Cloud/Praesentation/` (`ice-truck-in-der-cloud.pptx`, `redemanuskript.md`), Live-Version https://claude.ai/artifact/VmjCaHCTtuXDeyr3WgLdfa

**Stand 07.10.2026:** Discord- und Mail-Alarm läuft ([[Challenge III - Alarme (Discord + Mail)]]), Keys sind erneuert, Kanal bewusst **öffentlich** (nur nicht-sensible Messdaten, Begründung in `DATENSCHUTZ.md` 5a), Aufbewahrung auf 12 Monate festgelegt (Annahme, dokumentiert), MathWorks im Data Privacy Framework geprüft (aktiv, nur Non-HR-Daten). **Offen:** Pi läuft ab morgen wieder, Sensor-Drift-Skript (`Challenge-III-Ice-Truck-Cloud/Code/thingspeak/sensor_drift_visualization.m`) in ThingSpeak anlegen und testen, Offline-Demo, Screenshots, neuen Write Key auf dem Pi prüfen → [[Offene Punkte]]

## Bewertungsbogen Challenge III: Zuordnung zu Folien und Dokumenten (50 Punkte sichtbar)
| Kriterium | Punkte | Wo |
|---|---|---|
| Mindestens zwei Clouddienste vorgestellt | 5 | ENTSCHEIDUNG.md §2, Folie 5 |
| Entscheidung technisch begründet | 5 | ENTSCHEIDUNG.md §3, Folie 6 |
| NIST-Kriterien erfüllt bzw. Abweichungen begründet | 5 | ENTSCHEIDUNG.md §5, Folie 7 |
| Einordnung IaaS/PaaS/SaaS | 5 | ENTSCHEIDUNG.md §4, Folie 8 |
| Datensicherheit und DSGVO | 5 | DATENSCHUTZ.md, Folie 9 |
| Konzept sichere Datenübertragung | 10 | SICHERHEITSKONZEPT.md, Folie 10 |
| Messdaten in der Cloud protokolliert und visualisiert | 10 | README.md, Folie 11 |
| Zusätzliche Funktionen | 5 | Store and Forward, Health-Flags, Alarme, Folie 12 |

## Alternative: IaaS mit eigener VM (Plan B / Vergleich)
Zusätzlich liegt ein vollständiger Entwurf für eigenen MQTT-Broker + InfluxDB + Grafana auf einer gemieteten VM (Docker Compose, TLS, Mosquitto-Bridge vom Pi) unter `Challenge-III-Ice-Truck-Cloud/Code/alternative-iaas-vm/`. Nicht deployt, nicht die gewählte Lösung – aber gut für die Präsentation als Vergleich IaaS (volle Kontrolle, manuelle Elastizität, Betrieb selbst) vs. PaaS (IoT Hub: verwaltet, Vendor-Bindung). Die Aufgabenstellung nennt diese Variante ausdrücklich als Option.

## Bewertungsbogen Challenge III (Stand 07.10.2026)
> Hinweis: Die Spalte „Wo abgedeckt“ unten stammt aus der ersten Fassung (noch Azure als Hauptlösung). Maßgeblich ist die Zuordnung zu Folien und Dokumenten weiter oben.
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

## Alarme über ThingSpeak (07.10.2026)
React (Field 3 > 30) → MATLAB Analysis → Discord-Webhook + Alerts-API-Mail. Code, Stolperfallen, Protokoll-Einordnung und Präsentations-Merkliste: [[Challenge III - Alarme (Discord + Mail)]]. Zählt als „Zusätzliche Funktionen“ (/5). Das Protokoll der Messdaten (/10) ist der ThingSpeak-Channel mit Zeitstempel, nicht Discord.

## Relevante Kursinhalte
- "Datenbankanbindung und Object-Relational Mapping" (Kurs-ID 564) – **benötigt Einschreibekennwort**, siehe [[Offene Punkte]]

## Prüfungsbezug
Nach dieser Challenge: Fachgespräch (40%), siehe [[Leistungsnachweise]]

#moodle #challenges
