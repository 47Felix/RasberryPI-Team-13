---
tags: [moodle, challenges]
---

# Challenge III: "Ice Truck in Cloud"

**Schwerpunkt:** IoT in Cloud

## Szenario
Um Prozesse in der Lieferkette transparent zu machen und zu optimieren, sollen die erhobenen Daten in einer Cloud gespeichert und ausgewertet werden.

→ Baut auf [[Challenge II - Ice Truck Extension]] auf, Fokus liegt auf Cloud-Anbindung/Datenauswertung.

## Konkrete Aufgabenstellung (erhalten 30.09.2026)

> **Problem:** Nachweispflicht zur Rückverfolgbarkeit/Qualitätssicherung nach EU-VO 178/2002/EG und 37/2005/EG (Merkblatt Tiefkühl-LM LM-05-MBL-504-PM, Stand 01.04.2020). Temperaturkontrolle nur stichprobenartig, Daten nur lokal auf dem Pi im Truck, manuelles Auslesen bei Ankunft in der Zentrale -> keine sofortige, standortunabhängige Verfügbarkeit. Dazu Störungen: Sensorausfälle, Kühlaggregate, Hardwarefehler trotz Wartung.
>
> **Erweiterung:** Daten automatisiert in die Cloud -> jederzeit/ortsunabhängig abrufbar, zusätzliche Datensicherung bei Pi-Ausfall, kein manuelles Auslesen, kontinuierliche Analyse (Predictive Maintenance).
>
> **Mehrwert:** weniger Ausfallzeiten, effizientere Wartung, geringere Kosten, einfachere Nachweise.
>
> **Ziel:** Sensordaten eines IoT-Geräts in geeigneter Cloud speichern und auswerten.
> 1. Informieren: AWS IoT Core, Azure IoT Hub, Arduino Cloud, oder eigener MQTT-Broker + Zeitreihen-DB (z. B. InfluxDB) auf Cloud-Infrastruktur (VM/Container)
> 2. Auswählen + fachlich begründen: IoT-Protokolle, Speicherung, Visualisierung, Kosten, Datenschutz u. a., Einordnung IaaS/PaaS/SaaS
> 3. Umsetzen: Daten in die Cloud, **alle fünf NIST-Merkmale** erfüllen (SP 800-145: On-demand Self-Service, Broad Network Access, Resource Pooling, Rapid Elasticity, Measured Service). Privater Server im eigenen Netz (Homeserver, Pi zuhause) gilt i. d. R. **nicht** als Cloud; Ausnahme nur nach Absprache mit der Lehrkraft und dann mit Reflexion, welche NIST-Merkmale fehlen.
> 4. Letzter Tag: Lösungen gegenseitig vorstellen, NIST-Erfüllung begründen.

## Entscheidungsvorschlag (Team muss bestätigen)

**Eigene IoT-Serverlösung auf gemieteter Azure-VM (IaaS):** Mosquitto (TLS) -> Telegraf -> InfluxDB -> Grafana, als Docker-Compose. Code: `Challenge-III-Ice-Truck-Cloud/Code/`.

| Kriterium | Eigene Lösung (VM+Docker) | AWS IoT Core / Azure IoT Hub | Arduino Cloud |
|---|---|---|---|
| Einordnung | IaaS (Stack selbst betrieben) | PaaS | SaaS |
| Protokolle | MQTT direkt (bereits im Einsatz, Challenge II), HTTP möglich | MQTT/HTTP, eigene Auth (Zertifikate/SAS) | proprietär/MQTT-ähnlich, an Arduino-Boards gebunden |
| Speicherung | InfluxDB, Retention frei (Nachweispflicht!) | braucht Zusatzdienst (Timestream/S3, ADX) | begrenzte Historie im Free-Tier |
| Visualisierung | Grafana, frei gestaltbar | Zusatzdienst nötig | fertige Dashboards, wenig flexibel |
| Kosten | kleine VM ~10-15 EUR/Monat bzw. Studentenguthaben | pay-per-message, günstig bei kleiner Last | Free-Tier, dann Abo |
| Datenschutz | Region frei wählbar (Azure Germany West Central/EU), volle Kontrolle | EU-Region möglich, US-Anbieter | Anbieter in EU/US, wenig Kontrolle |
| Lerneffekt/Passung | hoch, baut direkt auf Mosquitto/Node-RED/MQTT auf | mittel | gering (Pi/Node-RED-Aufbau passt nicht) |
| Nachteil | Betrieb/Sicherheit/Updates selbst verantwortlich | Vendor-Lock-in | Pi-Anbindung umständlich |

Begründung: Topic-Schema und Broker existieren schon, Azure-VM ist im Team vorhanden (Discord-Bot, siehe [[Claude Discord Bot Setup]]), und die VM ist eine echte Cloud-Ressource.

## NIST-Nachweis (für die Präsentation)

| Merkmal | Wie erfüllt |
|---|---|
| On-demand Self-Service | VM/Netzwerk/Storage im Azure-Portal bzw. per CLI selbst bereitgestellt, ohne Anbieterkontakt |
| Broad Network Access | Grafana per HTTPS, MQTT per TLS 8883 von jedem Netz/Gerät (Handy, Laptop, Truck über Mobilfunk) |
| Resource Pooling | VM läuft auf geteilter Azure-Hardware (Multi-Tenant), Ressourcen dynamisch zugewiesen |
| Rapid Elasticity | VM-Größe/Disk per Klick ändern; Docker-Services skalierbar; mehrere Trucks = nur weitere Topics/Tags |
| Measured Service | Azure Cost Management / Metrics, Abrechnung nach Nutzung; InfluxDB/Telegraf-Selbstmessung |

Ehrliche Einschränkung für die Reflexion: Elastizität ist bei IaaS **manuell** (kein Autoscaling ohne VMSS/Kubernetes), und Betrieb/Patching liegen beim Team (im Gegensatz zu PaaS/SaaS).

## Architektur
`Arduinos -> pi-backend -> Node-RED -> lokaler Mosquitto -> Bridge (TLS, QoS1, gepuffert) -> Cloud-Mosquitto -> Telegraf -> InfluxDB -> Grafana`
Details und Deployment: `Challenge-III-Ice-Truck-Cloud/Code/README.md`.

## Tracks / Fortschritt
- [ ] **A – Entscheidung:** Cloud-Lösung im Team bestätigen, Azure-Kosten/Guthaben klären, Lehrkraft nur nötig bei Ausnahme (Self-Hosting)
- [ ] **B – Cloud-VM:** VM, DNS-Name, NSG (80/443/8883), Zertifikat (Let's Encrypt)
- [ ] **C – Stack deployen:** `docker compose up`, Broker-Nutzer anlegen (Code fertig entworfen, nicht getestet)
- [ ] **D – Pi-Bridge:** `team13-cloud-bridge.conf` auf dem Pi aktivieren, Daten kommen in InfluxDB an (setzt funktionierenden lokalen Mosquitto/Node-RED aus Challenge II voraus)
- [ ] **E – Visualisierung + Auswertung:** Grafana-Dashboard (provisioniert), Alerts + Predictive-Maintenance-Queries (`analysis/flux-queries.md`)
- [ ] **F – Datenschutz/Sicherheit:** EU-Region, keine Klartext-Ports, Zugangsdaten nur in `.env`, Retention/Löschkonzept schreiben (Temperaturdaten sind nicht personenbezogen, GPS/Fahrer wären es)
- [ ] **G – Präsentation:** NIST-Tabelle + Live-Demo (Handy-Dashboard, Pi trennen -> Nachlieferung)

## Relevante Kursinhalte
- "Datenbankanbindung und Object-Relational Mapping" (Kurs-ID 564) – **benötigt Einschreibekennwort**, siehe [[Offene Punkte]]

## Prüfungsbezug
Nach dieser Challenge: Fachgespräch (40%), siehe [[Leistungsnachweise]]

#moodle #challenges
