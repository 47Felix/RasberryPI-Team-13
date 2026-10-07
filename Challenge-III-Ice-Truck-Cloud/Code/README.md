# Challenge III – Ice Truck in der Cloud (ThingSpeak)

Die Temperaturdaten aus Challenge I (`challenge_i.db` auf dem Pi) werden automatisch in die
Cloud übertragen, dort gespeichert, visualisiert und ausgewertet. Wir nutzen **ThingSpeak**
(MathWorks, SaaS). Plan A war Azure IoT Hub; der Code dafür ist fertig, lief aber nie (Abschnitt
„Alternative: Azure IoT Hub“ unten).

| Dokument | Inhalt |
|---|---|
| [`ENTSCHEIDUNG.md`](ENTSCHEIDUNG.md) | Vergleich der Clouddienste, Begründung, SaaS-Einordnung, NIST-Merkmale |
| [`SICHERHEITSKONZEPT.md`](SICHERHEITSKONZEPT.md) | sichere Datenübertragung, Bedrohungen, Maßnahmen, Nachweise |
| [`DATENSCHUTZ.md`](DATENSCHUTZ.md) | Datensicherheit und DSGVO-Einschätzung, Prüfliste |

## Architektur

```
 Truck (Edge)                                         Cloud
┌─────────────────────────────────┐              ┌──────────────────────────────────────┐
│ Arduinos ─I²C─> app.py          │              │  ThingSpeak-Kanal (privat)           │
│                   │ schreibt    │  HTTPS (TLS) │   Feld 1–8 + Status                  │
│            challenge_i.db ──────┼──────────────┼─> Diagramme, Widgets                 │
│     (Original und Puffer)       │  POST        │   MATLAB: Sensor-Drift, Ausreißer    │
│                   │ liest (ro)  │  Bulk-Update │   React/Alerts: E-Mail bei Alarm     │
│            cloud-bridge/        │              │   CSV-Export als Nachweis            │
│            bridge.py            │              └──────────────────────────────────────┘
│  (Cursor, Batches, Flags)       │
└─────────────────────────────────┘
```

- **Edge:** `cloud-bridge/bridge.py` liest nur lesend aus der bestehenden Datenbank. Der
  Challenge-I-Regelkreis bleibt unverändert, der Truck regelt also auch ohne Netz weiter.
- **Vorauswertung am Edge:** Jeder Batch trägt `flags` (`temp_high`, `sensor_mismatch`,
  `sensor_stuck`). Bei ThingSpeak stehen sie im Statusfeld des letzten Eintrags.

## Store and Forward: was passiert da genau?

**Store** = jede Messung wird zuerst lokal gespeichert, **Forward** = sie wird danach
weitergeleitet, sobald die Cloud erreichbar ist. Die Cloud ist also nie die einzige Kopie, und
ein Funkloch verliert nichts.

1. **Messen und speichern:** `app.py` schreibt alle 5 s eine Zeile in `challenge_i.db`, jede
   mit einer fortlaufenden `id` (1, 2, 3 …). Das passiert unabhängig vom Netz.
2. **Merken, was schon oben ist:** Die Bridge merkt sich in `bridge_state.json` den
   **Cursor** `last_sent_id`, also die `id` der letzten Messung, die die Cloud **bestätigt** hat.
3. **Senden:** Alle `SEND_INTERVAL_SECONDS` holt sie alle Zeilen mit `id > last_sent_id` aus der
   Datenbank (höchstens `MAX_ROWS_PER_MESSAGE`) und schickt sie gebündelt, jede mit ihrer
   **Original-Uhrzeit**.
4. **Erst bei Erfolg weiterschieben:** Antwortet ThingSpeak mit `success`, wird der Cursor auf die
   `id` der letzten gesendeten Zeile gesetzt und **atomar** gespeichert. Gibt es einen Fehler
   (kein Netz, Timeout, falscher Key), bleibt der Cursor stehen.
5. **Nachholen:** Beim nächsten Zyklus beginnt die Bridge wieder genau dort. Während eines
   Funklochs sammelt sich der Rückstand in der Datenbank an. Sobald das Netz wieder da ist,
   wird er in Paketen von bis zu 720 Zeilen nachgeschickt (etwa eine Stunde Messzeit pro
   Paket), und im Diagramm füllt sich die Lücke mit den echten Zeitpunkten.

Beispiel: Messung 100–220 laufen, das WLAN fällt aus. Der Cursor bleibt bei 100, `app.py`
misst weiter bis 220. Nach dem Wiederverbinden holt die Bridge 101–220 und lädt sie mit
den ursprünglichen Zeitstempeln hoch. Der Cursor springt auf 220.

**Grenzen:**
- *At-least-once:* Stürzt die Bridge genau zwischen „Cloud hat bestätigt“ und „Cursor
  gespeichert“ ab, wird das letzte Paket doppelt gesendet. Deshalb steht die lokale `id` im
  Statusfeld (`id=4711`), Duplikate sind erkennbar.
- Wird die Datenbank gelöscht, muss auch `bridge_state.json` gelöscht werden, sonst wartet die
  Bridge auf `id`s, die nicht mehr vorkommen.
- Beim allerersten Start schickt die Bridge nur neue Messungen (`START_FROM=now`). Mit
  `START_FROM=all` lädt sie den gesamten Bestand nach.

**Demo für die Vorstellung:** 
1. Dienst stoppen: `sudo systemctl stop cloud-bridge`, ca. 3 Minuten warten (die Messungen laufen weiter).
2. Dienst starten: `sudo systemctl start cloud-bridge`. Im ThingSpeak-Diagramm füllt sich die Lücke
   rückwirkend.
3. Realistischer ist ein echter Netzausfall (WLAN des Pi kurz trennen), zum Vorführen aber riskanter,
   weil dabei auch die SSH-Verbindung abbricht.

## Kontingent (ThingSpeak Free, laut Anbieter prüfen)

- höchstens **1 Request alle 15 s**; die Bridge wartet von selbst
- ca. **3 Mio. Nachrichten pro Jahr** (≈ 8.200 pro Tag); jeder Eintrag im Bulk-Update zählt einzeln

| Einstellung | Einträge pro Tag | Kontingent reicht … |
|---|---|---|
| `THINGSPEAK_DOWNSAMPLE=1` (jede 5-s-Messung) | 17.280 | ca. 6 Monate |
| `THINGSPEAK_DOWNSAMPLE=3` (15-s-Raster) | 5.760 | ein ganzes Jahr |

Für das Projekt und die Vorstellung nehmen wir jede Messung (`1`). Im Dauerbetrieb oder mit
mehreren Trucks `3` oder ein Lizenz-Upgrade. Lokal bleiben immer alle Messungen in der DB. Die
letzte Zeile jedes Pakets geht immer mit, damit Alarm-Flags nicht verloren gehen.

## Einrichtung

### 1. Kanal anlegen (5 min)

1. Konto auf <https://thingspeak.mathworks.com> anlegen (Schul-E-Mail geht).
2. *Channels → New Channel*, Name `Ice Truck Team13-1`, alle 8 Felder aktivieren und so benennen:

   | Feld | Name | Feld | Name |
   |---|---|---|---|
   | Field 1 | Temp Sensor-Board °C | Field 5 | Ventil-Winkel |
   | Field 2 | Temp Aktor-Board °C | Field 6 | Rohwert Sensor-Board |
   | Field 3 | Ø Temperatur °C | Field 7 | Rohwert Aktor-Board |
   | Field 4 | Lüfter PWM | Field 8 | KY-028 Digital |

   Das Statusfeld enthält `id=<lokale ID>` und ggf. `flags=temp_high,…`.
3. Der Kanal muss **privat** bleiben (*Sharing → Keep channel view private*).
4. Tab *API Keys*: **Channel ID**, **Write API Key** und **Read API Key** notieren (geheim, nie committen).

### 2. Pi

```bash
cd ~/RasberryPI-Team-13 && git pull
cd Challenge-III-Ice-Truck-Cloud/Code/cloud-bridge
python3 -m venv venv                  # der ThingSpeak-Sender braucht nur die Standardbibliothek
cp .env.example .env && chmod 600 .env
nano .env                             # THINGSPEAK_CHANNEL_ID und THINGSPEAK_WRITE_API_KEY eintragen
sudo cp cloud-bridge.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now cloud-bridge
journalctl -u cloud-bridge -f         # nach ≤ 1 min: "… Messungen gesendet"
```

Im Kanal unter *Private View* erscheinen die Diagramme. Mit `.env.example` als Vorlage sind
die Werte für den 5-Sekunden-Betrieb schon gesetzt (`THINGSPEAK_DOWNSAMPLE=1`,
`SEND_INTERVAL_SECONDS=15`, `MAX_MESSAGES_PER_CYCLE=1`, `MAX_ROWS_PER_MESSAGE=720`).

Nach einer Änderung der `.env`: `sudo systemctl restart cloud-bridge`. Nach einer Änderung an
`cloud-bridge.service`: `sudo cp cloud-bridge.service /etc/systemd/system/ && sudo systemctl daemon-reload && sudo systemctl restart cloud-bridge`.

### 3. Auswertung und Alarme in ThingSpeak

- **Visualisierung:** *Private View* zeigt automatisch ein Diagramm pro Feld. Zusätzlich gibt es
  Widgets (Gauge, Numeric Display) über *Add Widgets*.
- **Sensor-Drift (Predictive Maintenance), MATLAB Visualization:** *Apps → MATLAB Visualization*.
  Wandert ein Sensor vom anderen weg? So erkennt man den Wackelkontakt am KY-028 früh:
  ```matlab
  channelID = <channel id>; readKey = '<read api key>';
  [d, t] = thingSpeakRead(channelID, 'Fields', [1 2], 'NumDays', 7, 'ReadKey', readKey);
  delta = movmean(abs(d(:,1) - d(:,2)), 40);
  plot(t, delta); ylabel('|Sensor - Aktor| in °C'); title('Sensor-Drift');
  ```
- **Alarm per E-Mail:** Den *Alerts API Key* aus *Account → My Profile* kopieren. Unter
  *Apps → MATLAB Analysis → New* dieses Skript anlegen. Die Mail geht an die Adresse des
  ThingSpeak-Kontos:
  ```matlab
  alertApiKey = '<alerts api key>';
  alertUrl = "https://api.thingspeak.com/alerts/send";
  options = weboptions("HeaderFields", ["ThingSpeak-Alerts-API-Key", alertApiKey]);

  [t, ~] = thingSpeakRead(<channel id>, 'Fields', 3, 'NumMinutes', 5, 'ReadKey', '<read api key>');
  if ~isempty(t) && max(t) > 28
      subject = "Ice Truck: Temperatur zu hoch";
      body = sprintf("Höchste Temperatur der letzten 5 min: %.1f °C", max(t));
      webwrite(alertUrl, "body", body, "subject", subject, options);
  end
  ```
  Das Skript regelmäßig ausführen: *Apps → TimeControl*, alle 5 Minuten, Aktion *MATLAB Analysis*.
  Alternativ löst *Apps → React* („Field 3 größer als 28“) das Skript direkt beim Eintreffen eines
  Werts aus. Zum Testen die Schwelle kurz auf 20 °C setzen.
- **Alarm per Discord (optional):** über *Apps → ThingHTTP* eine POST-Anfrage an einen
  Discord-Webhook (Kanaleinstellungen → Integrationen → Webhooks) definieren und mit *React*
  auslösen. Die Webhook-URL ist geheim wie ein Key.
- **Export für den Nachweis:** *Data Import/Export → Export* als CSV, oder
  `https://api.thingspeak.com/channels/<id>/feeds.csv?start=…&end=…&api_key=<read key>`.
  Den Read Key in dieser URL nicht weitergeben.

## Nachrichtenformat (intern)

`send_pending()` baut pro Zyklus ein Paket im Spaltenformat. ThingSpeak bekommt daraus
`bulk_update.json`, Azure würde das Paket als Nachricht erhalten:

```json
{"schema":"icetruck-v1","truck_id":"icetruck-team13-1",
 "first_ts":"2026-09-30T08:00:00+00:00","last_ts":"2026-09-30T08:00:55+00:00",
 "min_temp_c":6.4,"max_temp_c":7.1,"flags":[],
 "cols":["id","timestamp_utc","sensor_board_raw","sensor_board_temp_c","sensor_board_digital",
         "actor_board_raw","actor_board_temp_c","fan_pwm","valve_angle"],
 "rows":[[4711,"2026-09-30T08:00:00+00:00",190,6.8,0,188,7.1,0,0], …]}
```

## Tests

```bash
cd cloud-bridge && python3 -m venv venv && venv/bin/pip install -r requirements-dev.txt
venv/bin/python -m pytest -q tests
```

Die Tests laufen ohne Cloud, mit Fake-Sender bzw. Fake-HTTP gegen eine echte SQLite-DB aus
`pi-backend/db.py`. Abgedeckt sind: erster Start, Nachholen im Batch, Limit pro Zyklus, Cursor
bleibt bei Sendefehler und bei abgelehntem Upload stehen, Health-Flags, Ausdünnen für ThingSpeak,
Flags im Statusfeld, Auswahl des Backends und dass die Datenbank nur lesend geöffnet wird.
Für die Azure-Variante zusätzlich `requirements.txt` installieren.

## Alternative: Azure IoT Hub (Plan A, nicht in Betrieb)

Für den Flottenbetrieb die bessere Wahl (EU-Region, unveränderliches Archiv, Schlüssel pro
Gerät). Der Code ist fertig, wurde aber nie gegen einen echten IoT Hub getestet, weil der
Zugang zum Schülerkonto am 30.09.2026 nicht ging. Umschalten mit `CLOUD_BACKEND=azure`.

### Azure einrichten (ca. 10 min)

Im Portal die **Cloud Shell** (Bash) öffnen und `azure/setup.sh` ausführen:

```bash
SUFFIX=team13x1 LOCATION=germanywestcentral bash setup.sh
```

Das Skript legt die Ressourcengruppe, den IoT Hub (F1), das Device, den Storage-Container
und beide Routen an und gibt am Ende den **Device-Connection-String** aus.

<details><summary>Falls die CLI-Befehle scheitern: dasselbe im Portal</summary>

1. *IoT Hub erstellen*: Tarif **Free (F1)**, Region Germany West Central / West Europe.
2. IoT Hub → *Geräte* → *Gerät hinzufügen*, ID `icetruck-team13-1`, Authentifizierung
   „Symmetrischer Schlüssel“ → primäre Verbindungszeichenfolge kopieren.
3. *Speicherkonto erstellen* (Standard LRS), Container `telemetry` anlegen (privat).
4. IoT Hub → *Nachrichtenrouting* → Route `to-archive`: Endpunkt „Storage“, Container
   `telemetry`, **Codierung JSON**, Quelle „Gerätetelemetrienachrichten“.
5. Zweite Route `to-builtin` auf den integrierten Endpunkt `events`. Ohne diese Route
   landet nach Schritt 4 nichts mehr am eingebauten Endpunkt.
</details>

Auf dem Pi: `pip install -r requirements.txt` im venv, in `.env` `CLOUD_BACKEND=azure` und
`IOTHUB_DEVICE_CONNECTION_STRING` setzen, für Netze ohne Port 8883 `IOTHUB_WEBSOCKETS=1`.
Mitlesen: `az iot hub monitor-events -n iothub-icetruck-team13x1 -d icetruck-team13-1 --properties app`.
Visualisierung mit Azure Data Explorer (Free Cluster): Tabelle, Mapping und Funktion aus
[`azure/adx.kql`](azure/adx.kql), dann Dashboard-Kacheln aus Abschnitt 3 der Datei. Das
IoT-Hub-Kontingent (F1: 8.000 Nachrichten pro Tag) ist der Grund, warum die Bridge im
Spaltenformat bündelt.

## Offene Punkte

- [ ] Alarm per E-Mail (und optional Discord) in ThingSpeak einrichten und testen
- [ ] Sensor-Drift-Diagramm als MATLAB Visualization anlegen
- [ ] Offline-Test vorführen (Dienst stoppen, warten, starten) und Screenshot machen
- [ ] Write/Read Key neu erzeugen und in `.env` eintragen (beide wurden im Chat geteilt)
- [ ] Prüfliste in [`DATENSCHUTZ.md`](DATENSCHUTZ.md), Abschnitt 8, abhaken
- [ ] Screenshots für die Vorstellung: Kanal mit Diagrammen, TLS-Nachweis, Kontingent im Konto
- [ ] Optional: Azure-Variante (`azure/setup.sh`), sobald der Zugang wieder geht
