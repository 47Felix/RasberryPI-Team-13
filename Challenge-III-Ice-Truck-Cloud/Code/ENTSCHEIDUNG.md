# Challenge III – Auswahl der IoT-Cloud-Lösung

**Entscheidung:** **Microsoft Azure IoT Hub (PaaS)** mit Blob Storage als Archiv und
Azure Data Explorer für Auswertung und Visualisierung.

## 1. Vergleich der Optionen

| Kriterium | **Azure IoT Hub** | AWS IoT Core | Arduino Cloud | Eigener Server (VM + Mosquitto + InfluxDB + Grafana) |
|---|---|---|---|---|
| **Einordnung** | **PaaS** | PaaS | SaaS | IaaS |
| **Protokolle** | MQTT 3.1.1, MQTT über WebSockets (443), AMQP, HTTPS | MQTT 3.1.1/5, WebSockets, HTTPS | MQTT intern, eher auf Arduino-/ESP-Boards zugeschnitten, Python-SDK begrenzt | frei wählbar (MQTT 5, HTTP ...) |
| **Speicherung** | Routing ohne Code nach Blob Storage/Data Lake, Cosmos DB, Event Hubs | Rules Engine → S3, DynamoDB, Timestream | eingebaut, Historie je nach Plan nur kurz (Free: 1 Tag) | InfluxDB, selbst betrieben |
| **Visualisierung** | Azure Data Explorer (Free Cluster, KQL-Dashboards), Power BI, Grafana | Grafana (Managed, kostenpflichtig), QuickSight | fertige Dashboards, sehr einfach | Grafana, frei konfigurierbar |
| **Kosten** | **F1 = 0 €** (8.000 Nachr./Tag), Storage < 1 ct/Monat; bezahlt aus dem Azure-for-Students-Guthaben (100 $, ohne Kreditkarte) | Free Tier nur 12 Monate, **Kreditkarte nötig**, kein Schüler-Konto vorhanden | Free: 2 Things, 1 Tag Historie → für den 1-Jahres-Nachweis ungeeignet | VM ab ~8–15 €/Monat, dazu Patchen, Backups und Zertifikate selbst machen |
| **Datenschutz** | EU-Regionen (Germany West Central), EU Data Boundary, TLS 1.2, pro Gerät eigener Schlüssel, RBAC | EU-Region Frankfurt möglich | Anbieter in der EU, aber wenig Kontrolle über Speicherort/-dauer | volle Kontrolle, aber auch volle Verantwortung (Updates, Härtung) |
| **Aufwand für uns** | mittel | mittel | gering | hoch |
| **Skalierung Flotte** | Tarifwechsel F1 → S1/S2/S3 ohne Codeänderung, Device Provisioning Service für tausende Trucks | sehr gut | begrenzt | selbst bauen |

## 2. Begründung

1. **Konto vorhanden:** Wir haben ein **Azure-for-Students-Konto** mit Guthaben und
   ohne Kreditkarte. AWS würde eine Kreditkarte verlangen.
2. **Protokoll passt zu unserem Stack:** Seit Challenge II arbeiten wir mit MQTT. IoT Hub
   spricht MQTT über TLS. Für Netze, die Port 8883 sperren, gibt es MQTT über WebSockets
   auf Port 443. Das offizielle Python-SDK (`azure-iot-device`) läuft direkt auf dem Pi.
3. **Nachweispflicht (VO 178/2002, 37/2005):** Die Aufzeichnungen müssen lückenlos und
   datiert sein und mindestens ein Jahr aufbewahrt werden. Blob Storage speichert jede
   Nachricht als JSON-Datei nach Datum. Das Archiv kostet praktisch nichts, lässt sich
   per Lifecycle-Regel länger aufbewahren und per Immutability-Policy (WORM) gegen
   nachträgliche Änderung sperren. Die Arduino Cloud hält im Free-Tarif nur einen Tag
   Historie.
4. **Kosten:** IoT Hub F1, der ADX Free Cluster und wenige MB Blob Storage kosten
   zusammen **0 € bis wenige Cent im Monat**. Ein eigener Server bräuchte eine
   dauerhaft laufende VM.
5. **PaaS statt IaaS:** Um Betriebssystem-Updates, Broker-Zertifikate, Backups und
   Hochverfügbarkeit kümmert sich Microsoft. Wir konzentrieren uns auf die fachliche
   Logik, also Store & Forward, Alarm-Flags und Auswertung.
6. **Predictive Maintenance:** Azure Data Explorer bringt Zeitreihen- und
   Anomalie-Funktionen mit (`series_decompose_anomalies`). Damit sehen wir
   Sensor-Drift, also genau unser Wackelkontakt-Problem am KY-028, und die steigende
   Lüfterlaufzeit eines schwächer werdenden Aggregats, bevor der Truck ausfällt.

**Nachteile:** Das F1-Kontingent ist knapp. Wir lösen das mit Batches im
Spaltenformat, siehe README. Außerdem gibt es einen Vendor-Lock-in. Weil wir aber
standardisiertes MQTT und JSON verwenden, wäre ein Wechsel mit überschaubarem Aufwand
möglich.

## 3. Erfüllung der NIST-Merkmale (SP 800-145)

| NIST-Merkmal | So erfüllt unsere Lösung es |
|---|---|
| **On-demand Self-Service** | IoT Hub, Device und Storage haben wir selbst per Portal/CLI (`azure/setup.sh`) in Minuten angelegt, ohne Vertrag, Ticket oder Rückfrage beim Anbieter. |
| **Broad Network Access** | Zugriff über das Internet mit Standardprotokollen (MQTT/TLS, HTTPS). Der Pi sendet aus dem Truck über jedes Netz. Daten und Dashboards sind per Browser von jedem Gerät erreichbar, etwa bei einer Lebensmittelkontrolle vor Ort. |
| **Resource Pooling** | Microsoft betreibt IoT Hub, Storage und ADX mandantenfähig auf gemeinsamer Hardware im Rechenzentrum Frankfurt. Wir wissen nicht, auf welchem Server unsere Daten liegen, nur die Region. |
| **Rapid Elasticity** | Mehr Trucks bedeuten nur einen Tarifwechsel (F1 → S1 → S3) oder mehr Units. Storage und ADX skalieren automatisch. Am Code ändert sich nichts, bei tausenden Trucks kommt der Device Provisioning Service dazu. |
| **Measured Service** | Abgerechnet wird nach Verbrauch: IoT-Hub-Nachrichten/Tag, GB im Storage, Abfragen in ADX. Im Portal sehen wir die Metriken (*IoT Hub → Metriken → Telemetrienachrichten gesendet*) und die *Kostenverwaltung* des Schülerguthabens. |

**Nicht Cloud wäre:** ein Mosquitto/InfluxDB auf einem Pi oder Homeserver bei uns zu
Hause. Dort fehlen Resource Pooling, Elastizität und verbrauchsabhängige Abrechnung.

## 4. Datenschutz und Sicherheit

- **Keine personenbezogenen Daten:** Übertragen werden nur Truck-ID, Temperaturen und
  Aktorwerte. Kämen später GPS oder Fahrer-IDs dazu, wären das personenbezogene Daten
  (DSGVO Art. 4). Dann bräuchten wir eine Rechtsgrundlage und einen AV-Vertrag mit
  Microsoft (DPA).
- **Datenhaltung in der EU:** Region Germany West Central, Microsoft EU Data Boundary.
- **Transportverschlüsselung:** TLS 1.2, Storage mit `min-tls-version TLS1_2` und ohne
  öffentlichen Blob-Zugriff.
- **Identität pro Gerät:** Jeder Truck bekommt einen eigenen SAS-Schlüssel und kann nur
  als er selbst senden. Einen kompromittierten Truck sperrt man einzeln. Der Schlüssel
  liegt nur in `.env` auf dem Pi (`chmod 600`, in `.gitignore`).
- **Ausfallsicherheit:** Die Daten liegen doppelt vor, lokal in der SQLite-DB auf dem
  Pi und in der Cloud. Fällt der Pi aus, bleibt das Cloud-Archiv. Fällt das Netz aus,
  puffert die DB und die Bridge liefert nach.
