# Challenge III – Auswahl der IoT-Cloud-Lösung

**Entscheidung: ThingSpeak (MathWorks), eingeordnet als SaaS.**
Plan A war Azure IoT Hub (PaaS). Code und Einrichtungsskript dafür sind fertig
(`azure/`), liefen aber nie, weil der Zugang zum Azure-Schülerkonto am 30.09.2026 nicht
funktionierte. Seitdem läuft die Übertragung vom Raspberry Pi über denselben Bridge-Code
nach ThingSpeak.

Verwandte Dokumente:
[`SICHERHEITSKONZEPT.md`](SICHERHEITSKONZEPT.md) (sichere Übertragung) ·
[`DATENSCHUTZ.md`](DATENSCHUTZ.md) (Datensicherheit und DSGVO) ·
[`README.md`](README.md) (Einrichtung, Store and Forward)

> Quellen für ThingSpeak (Stand 30.09.2026):
> [Licensing FAQ](https://thingspeak.mathworks.com/pages/license_faq),
> [License Options](https://thingspeak.mathworks.com/prices),
> [MathWorks Privacy Policy](https://www.mathworks.com/company/trust-center/privacy-policy.html).
> Die Angaben zu Azure, AWS und Arduino Cloud stammen aus unserer Recherche und sollten vor
> der Abgabe nochmals auf den Seiten der Anbieter gegengeprüft werden.

## 1. Anforderungen aus der Aufgabe

- Nachweis von Temperaturverläufen (VO (EG) 178/2002, 37/2005): lückenlos, datiert, jederzeit
  und ortsunabhängig abrufbar, ohne manuelles Auslesen
- Daten dürfen bei Ausfall des Raspberry Pi nicht verloren gehen
- Auswertung der Messwerte für Predictive Maintenance
- Lösung muss die fünf NIST-Merkmale (SP 800-145) erfüllen, ein privater Server zu Hause
  zählt nicht als Cloud

## 2. Vergleich der Optionen

| Kriterium | **ThingSpeak** | **Azure IoT Hub** | AWS IoT Core | Arduino Cloud | Eigene VM (Mosquitto + InfluxDB + Grafana) |
|---|---|---|---|---|---|
| **Einordnung** | **SaaS** | PaaS | PaaS | SaaS | IaaS |
| **Protokolle** | HTTP(S)-REST, MQTT | MQTT 3.1.1 (TLS 8883 oder WebSockets 443), AMQP, HTTPS | MQTT, WebSockets, HTTPS | MQTT über eigene Bibliothek, auf Arduino/ESP zugeschnitten | frei wählbar |
| **Speicherung** | Kanal mit 8 Feldern und Statusfeld, CSV/JSON-Export | Routing ohne Code in Blob Storage, Data Lake, Cosmos DB | Rules Engine nach S3, DynamoDB, Timestream | eingebaut, im Free-Tarif nur sehr kurze Historie | InfluxDB, selbst betrieben |
| **Visualisierung** | Diagramme, Widgets, MATLAB-Auswertung eingebaut | Azure Data Explorer (Free Cluster), Power BI, Grafana | Managed Grafana (kostenpflichtig), QuickSight | fertige Dashboards | Grafana, frei gestaltbar |
| **Kosten** | Free-Tarif für nicht-kommerzielle kleine Projekte (unter 3 Mio. Nachrichten pro Jahr, 4 Kanäle, 15 s Intervall), keine Kreditkarte | IoT Hub F1 gratis (8.000 Nachrichten/Tag), Rest aus dem Schülerguthaben | Free Tier zeitlich begrenzt, Kreditkarte nötig | Free-Tarif mit starken Einschränkungen | VM-Miete ab ca. 8–15 € im Monat |
| **Datenschutz** | Anbieter in den USA, Speicherort weltweit, im EU-US Data Privacy Framework aktiv gelistet (nur Nicht-Beschäftigtendaten) | EU-Regionen möglich (Germany West Central) | EU-Region Frankfurt möglich | Anbieter in der EU, wenig Kontrolle über Speicherdauer | volle Kontrolle, volle Verantwortung |
| **Aufwand für uns** | gering | mittel | mittel | gering | hoch (Betrieb, Updates, Zertifikate) |
| **Zugang für uns** | Konto in Minuten angelegt, **läuft** | Schülerkonto am 30.09. nicht erreichbar, **nie in Betrieb** | Kreditkarte nötig | nicht geprüft | nur als Entwurf (`alternative-iaas-vm/`), **nie deployt** |

Vorgestellt und verglichen werden vor allem **ThingSpeak** und **Azure IoT Hub**; AWS,
Arduino Cloud und die eigene VM sind als weitere Alternativen bewertet.

## 3. Entscheidung und technische Begründung

Wir setzen **ThingSpeak** ein, weil es die Anforderungen bei geringstem Aufwand erfüllt:

1. **Protokolle:** Die HTTPS-Schnittstelle (`bulk_update.json`) passt zur Bridge und nimmt
   viele Messungen mit **eigenem Zeitstempel** pro Eintrag an. Genau das braucht Store and
   Forward: Nach einem Funkloch werden verpasste Messungen mit ihrer Originalzeit
   nachgeliefert, und das Diagramm füllt die Lücke. MQTT wäre ebenfalls möglich.
2. **Speicherung und Visualisierung eingebaut:** Kanal, Diagramme, Widgets und CSV-Export
   gibt es ohne eigenen Server. Für Predictive Maintenance laufen MATLAB-Auswertungen direkt
   in der Anwendung (Sensor-Drift, Ausreißer).
3. **Kosten:** 0 €, keine Kreditkarte. Laut Licensing FAQ gilt der Free-Tarif für
   nicht-kommerzielle Nutzung mit höchstens 3 Mio. Nachrichten im Jahr, 4 Kanälen und einem
   Update-Intervall von 15 Sekunden. Daraus folgt unser Aufbau: Die Messung läuft alle
   5 Sekunden, die Bridge bündelt und lädt alle 15 Sekunden hoch. Ein Schulprojekt ist
   nicht-kommerziell, die Lizenzen „Academic“ und „Student“ sind für Hochschulen
   („degree-granting institution“) gedacht und „Home“ nur für Privatnutzung.
4. **Datenschutz vertretbar:** Es werden nur Truck-ID, Temperaturen, Aktorwerte und
   Zeitstempel übertragen, keine Personendaten (siehe `DATENSCHUTZ.md`).
5. **Verfügbarkeit für uns:** Azure war am Tag der Umsetzung nicht erreichbar. Mit
   ThingSpeak konnten wir sofort liefern.

**Nachteile und wie wir damit umgehen:**

| Nachteil | Umgang |
|---|---|
| Server in den USA (Drittland) | Nur Daten ohne Personenbezug; Prüfung von Auftragsverarbeitung und Datenübertragung, siehe `DATENSCHUTZ.md` |
| Kein unveränderliches Archiv (kein WORM) wie bei Azure Blob Storage | Das Original bleibt in der lokalen SQLite-Datenbank; regelmäßiger CSV-Export als zusätzliches Archiv |
| Free-Tarif mit festen Limits; ist das Jahreskontingent leer, nimmt der Kanal keine Daten mehr an | Bündeln und Ausdünnen (`THINGSPEAK_DOWNSAMPLE`), Verbrauch unter *My Account* beobachten; die Bridge puffert lokal weiter |
| Free-Tarif nur für **nicht-kommerzielle** Nutzung, max. 4 Kanäle | Für ein Schulprojekt passend; ein Unternehmen mit echten Trucks braucht die kostenpflichtige Standard-Lizenz |
| Ein Write Key für den ganzen Kanal | Pro Truck ein eigener Kanal mit eigenem Key; Key-Rotation, siehe `SICHERHEITSKONZEPT.md` |
| Vendor-Lock-in | Der Sender ist austauschbar: dieselbe Bridge kann auch an Azure IoT Hub senden (`CLOUD_BACKEND=azure`) |

## 4. Einordnung: IaaS, PaaS oder SaaS?

**Unsere Lösung ist SaaS.**

| Wer verwaltet …? | IaaS (eigene VM) | PaaS (Azure IoT Hub) | **SaaS (ThingSpeak)** |
|---|---|---|---|
| Hardware, Rechenzentrum | Anbieter | Anbieter | Anbieter |
| Betriebssystem, Laufzeit | **wir** | Anbieter | Anbieter |
| Broker und Datenbank | **wir** | Anbieter | Anbieter |
| Anwendung (Kanäle, Diagramme) | **wir** | **wir** (Routing, Auswertung) | Anbieter |
| Daten und Konfiguration | wir | wir | **wir** |

**Begründung:** ThingSpeak ist eine fertige Anwendung, die wir im Browser nutzen. Wir
legen einen Kanal an und liefern Daten. Wir installieren, programmieren und patchen keine
Plattform. Die MATLAB-Skripte sind eine Funktion innerhalb dieser Anwendung und machen
sie nicht zu einer Plattform, auf der wir eigene Dienste betreiben, daher gilt es nicht als
PaaS.

Zum Vergleich wäre Azure IoT Hub PaaS: Die Plattform gehört dem Anbieter, aber wir bauen
Routing, Archiv und Auswertung selbst. Die eigene VM wäre IaaS.

## 5. NIST-Merkmale (SP 800-145)

| Merkmal | So erfüllt unsere Lösung es | Einschränkung / Abweichung |
|---|---|---|
| **On-demand Self-Service** | Konto, Kanal und API-Keys selbst im Browser angelegt, in Minuten, ohne Vertrag oder Rückfrage | Free-Tarif mit festen Nutzungsbedingungen |
| **Broad Network Access** | HTTPS aus jedem Netz; Diagramme im Browser und in der Handy-Ansicht | Der Pi braucht Internet; Ausfälle überbrückt der lokale Puffer |
| **Resource Pooling** | Die Plattform bedient viele Kunden gemeinsam; die Daten werden laut Privacy Policy dort gespeichert, „wo immer wir oder unsere Drittserviceanbieter arbeiten“ | Von uns nicht überprüfbar; wir kennen weder Server noch genauen Standort |
| **Rapid Elasticity** | Weitere „Units“ lassen sich jederzeit zukaufen (Licensing FAQ, Frage 10): 1 Unit = 33 Mio. Nachrichten pro Jahr, Intervall bis 1 s, mehr Kanäle, ohne Codeänderung | Im Free-Tarif feste Limits, **kein automatisches** Skalieren; ein Upgrade ist ein bewusster Schritt, bei leerem Kontingent nimmt der Kanal keine Daten mehr an (Frage 12) |
| **Measured Service** | Verbrauch und Restkontingent stehen auf der Seite *My Account* (Frage 16); ThingSpeak warnt bei knappem oder erschöpftem Kontingent (Fragen 17 und 18) | Im Free-Tarif keine Rechnung, nur Zählung und Warnung (Screenshot aus *My Account* als Beleg) |

**Nicht Cloud wäre:** ein Mosquitto/InfluxDB auf einem Pi oder Homeserver bei uns zu Hause.
Dort fehlen Resource Pooling, Elastizität und verbrauchsabhängige Abrechnung.

## 6. Datensicherheit, DSGVO und sichere Übertragung

- **Sichere Datenübertragung:** [`SICHERHEITSKONZEPT.md`](SICHERHEITSKONZEPT.md): Verschlüsselung,
  Authentifizierung, Schlüsselverwaltung, Vollständigkeit, Bedrohungen und Restrisiken.
- **Datensicherheit und DSGVO:** [`DATENSCHUTZ.md`](DATENSCHUTZ.md): welche Daten, Personenbezug,
  Drittlandübermittlung, technische und organisatorische Maßnahmen, Prüfliste.

## 7. Plan A: Azure IoT Hub (vorbereitet, nicht eingesetzt)

Für die Flotte bleibt Azure die bessere Wahl: EU-Datenhaltung, unveränderliches Archiv
(Blob Storage mit Immutability-Policy) für den Ein-Jahres-Nachweis, ein eigener Schlüssel
pro Gerät und keine Ausdünnung der Messwerte nötig.

Vorbereitet sind:

- `azure/setup.sh`: legt IoT Hub (F1), Device, Storage-Container und Routing an
- `azure/adx.kql`: Abfragen für Data Explorer (Verlauf, Alarme, Sensor-Drift, Anomalien)
- `cloud-bridge/bridge.py`: Sender `AzureIoTHubSender`, aktivierbar mit `CLOUD_BACKEND=azure`
  (Python-Bibliothek `azure-iot-device` gegen die echte Bibliothek geprüft, nie gegen einen
  echten IoT Hub)
- `alternative-iaas-vm/`: Entwurf für die IaaS-Variante mit eigener VM, ebenfalls nie deployt
