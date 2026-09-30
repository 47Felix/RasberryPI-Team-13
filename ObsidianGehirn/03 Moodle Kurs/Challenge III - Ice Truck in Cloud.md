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

## Relevante Kursinhalte
- "Datenbankanbindung und Object-Relational Mapping" (Kurs-ID 564) – **benötigt Einschreibekennwort**, siehe [[Offene Punkte]]

## Prüfungsbezug
Nach dieser Challenge: Fachgespräch (40%), siehe [[Leistungsnachweise]]

#moodle #challenges
