# Sicherheitskonzept: sichere Datenübertragung in die Cloud

Gilt für die laufende Lösung: Raspberry Pi → `cloud-bridge` → ThingSpeak (HTTPS).
Einordnung und Begründung der Cloud-Wahl: [`ENTSCHEIDUNG.md`](ENTSCHEIDUNG.md). Datenschutz:
[`DATENSCHUTZ.md`](DATENSCHUTZ.md).

## 1. Schutzziele

| Schutzziel | Bedeutung für den Ice Truck |
|---|---|
| **Vertraulichkeit** | Nur wir sehen die Temperaturdaten und können in den Kanal schreiben |
| **Integrität** | Eine Messung kommt unverändert und ohne Fälschung in der Cloud an |
| **Vollständigkeit / Verfügbarkeit** | Auch bei Funkloch oder Pi-Neustart geht keine Messung verloren |
| **Nachweisbarkeit** | Jede Messung hat eine eindeutige ID und einen Zeitstempel |

## 2. Datenfluss und Vertrauensgrenzen

```
 Truck (vertrauenswürdig)                    Internet (nicht vertrauenswürdig)        Anbieter
┌────────────────────────────────┐
│ Arduinos ─I²C─> app.py         │
│                  │  schreibt   │
│             challenge_i.db     │   ← Original, bleibt lokal (Quelle der Wahrheit)
│                  │  liest (nur lesend)
│             cloud-bridge       │ ═══ HTTPS (TLS), POST ═══════════════> ThingSpeak
│  .env (chmod 600): Write Key   │      Write Key im Body, nicht in der URL   Kanal (privat)
│  bridge_state.json (Cursor)    │
└────────────────────────────────┘
```

Die Vertrauensgrenze verläuft zwischen Pi und Internet. Alles, was sie überquert, ist
verschlüsselt und authentifiziert.

## 3. Bedrohungen und Gegenmaßnahmen

| # | Bedrohung | Maßnahme | Wo umgesetzt |
|---|---|---|---|
| 1 | Mitlesen im WLAN/Mobilfunknetz | Nur HTTPS (TLS). Die Adresse im Code ist fest `https://api.thingspeak.com/…`, ein Klartext-Fallback existiert nicht. Das Zertifikat wird von Python geprüft (Standardverhalten von `urllib`). | `bridge.py`, `ThingSpeakSender.URL` |
| 2 | Fremde schreiben falsche Werte in den Kanal | Schreiben geht nur mit dem **Write API Key**. Er liegt nur auf dem Pi und nicht im Repository. | `.env`, `.gitignore` |
| 3 | Key wird gestohlen oder im Log/Git sichtbar | Key im **POST-Body**, nicht in der URL (taucht nicht in Proxy- oder Server-Logs auf). `.env` hat `chmod 600` und steht in `.gitignore`. Die Bridge schreibt den Key nie ins Log. | `bridge.py`, README, `.gitignore` |
| 4 | Fremde lesen die Daten | Kanal ist **privat**. Auslesen geht nur mit dem getrennten **Read API Key** (anderer Schlüssel als zum Schreiben). Laut MathWorks Privacy Policy sind private Daten durch API-Keys geschützt, die jederzeit zurückgesetzt werden können. Öffentliche Kanäle würden zusätzlich Kontoname und Profil-Link zeigen. | ThingSpeak-Kanaleinstellungen |
| 4a | Kontingent erschöpft: der Kanal nimmt keine Daten mehr an (Licensing FAQ, Frage 12) | Verbrauch unter *My Account* beobachten, Ausdünnen per `THINGSPEAK_DOWNSAMPLE`. Die Bridge protokolliert die Ablehnung, lässt den Cursor stehen und puffert lokal weiter. | `send()`, `.env` |
| 5 | Messungen gehen bei Funkloch/Absturz verloren | **Store and Forward:** Die lokale DB ist der Puffer, der Cursor rückt erst nach bestätigtem Senden weiter, der Stand wird atomar gespeichert. | `send_pending()`, `save_state()` |
| 6 | Doppelte Messungen nach Absturz zwischen Senden und Speichern | At-least-once mit lokaler `id` je Messung im Statusfeld (`id=4711`), Duplikate sind erkennbar und filterbar. | `build_updates()` |
| 7 | Bridge verändert oder zerstört Messdaten | Datenbank wird **nur lesend** geöffnet (`mode=ro`), geschrieben wird nur von `app.py`. | `open_db()`, Test `test_open_db_is_read_only` |
| 8 | Falsche oder verfälschte Zeit | Zeitstempel in UTC. Die Pi-Zeit wird per NTP synchronisiert (`systemd-timesyncd`, siehe Vault „Installierte Services“). Grenze: siehe Restrisiken. | `app.py`, Systemkonfiguration |
| 9 | Dienst wird missbraucht, um Rechte auszuweiten | Systemd-Dienst läuft als normaler Nutzer `team13` mit `NoNewPrivileges` und privatem `/tmp`. | `cloud-bridge.service` |
| 10 | Bridge hängt sich bei Netzproblem auf | Jede Anfrage hat ein Timeout von 30 s. Fehler werden abgefangen, geloggt und im nächsten Zyklus erneut versucht. Der Dienst läuft weiter (`Restart=on-failure`). | `main()`, `send()` |
| 11 | Fehlkonfiguration (falscher Key/Kanal) bleibt unbemerkt | ThingSpeak antwortet bei falschem Key mit Fehler. Die Bridge wirft ihn weiter, loggt ihn und verschiebt den Cursor nicht. | `send()`, Test `test_thingspeak_rejection_keeps_cursor` |

## 4. Umsetzung im Detail

### Transport
- HTTPS mit Zertifikatsprüfung, kein Klartext-Fallback.
- Pro Anfrage ein Bulk-Update mit bis zu 720 Messungen, höchstens eine Anfrage alle
  15,5 Sekunden (Limit des Free-Tarifs, von der Bridge selbst eingehalten).

### Authentifizierung und Schlüssel
- **Zwei getrennte Schlüssel:** Write Key (nur Pi) und Read Key (nur für Auswertungen,
  Export und Alarme). Wird der Read Key bekannt, kann niemand schreiben.
- **Aufbewahrung:** `.env` im Verzeichnis `cloud-bridge/` auf dem Pi, Rechte `600`, vom Git
  ausgeschlossen. Der systemd-Dienst liest sie über `EnvironmentFile`.
- **Wichtig:** Schlüssel gehören nicht in Chats, Tickets, Screenshots oder Folien.

### Key-Rotation (nach jedem Verdacht auf Bekanntwerden, sonst regelmäßig)
1. ThingSpeak → Kanal → *API Keys* → *Generate New Write API Key* (analog für den Read Key).
2. Auf dem Pi in `cloud-bridge/.env` den Wert `THINGSPEAK_WRITE_API_KEY` ersetzen.
3. `sudo systemctl restart cloud-bridge`, danach `journalctl -u cloud-bridge -n 20`: Es
   muss „… Messungen gesendet“ erscheinen, keine Fehlermeldung.
4. Den alten Key nicht mehr verwenden. Er ist nach dem Neuerzeugen ungültig.

### Integrität und Vollständigkeit
- Originaldaten bleiben in `challenge_i.db`. Die Cloud ist die zweite Kopie.
- Cursor (`bridge_state.json`) wird atomar geschrieben (Temp-Datei + `os.replace`), ein
  Stromausfall hinterlässt keinen halben Stand.
- Wird die Datenbank gelöscht oder neu angelegt, muss auch `bridge_state.json` gelöscht werden,
  sonst wartet die Bridge auf IDs, die nicht mehr vorkommen.

### Verfügbarkeit
- Fällt das Netz aus, läuft die Regelung auf dem Pi unverändert weiter. Die Bridge holt den
  Rückstand später nach.
- Fällt der Pi aus, bleiben alle bis dahin hochgeladenen Daten in der Cloud.

## 5. Nachweise: so prüfen wir, dass es stimmt

Auf dem Pi ausführen und für die Vorstellung als Screenshot festhalten:

```bash
# 1. Verschlüsselung: TLS-Version und Zertifikat von ThingSpeak
curl -sv https://api.thingspeak.com 2>&1 | grep -E "SSL connection|TLSv|subject:|issuer:|expire date"

# 2. Schlüsseldatei nur für den Besitzer lesbar (erwartet: -rw-------)
ls -l ~/RasberryPI-Team-13/Challenge-III-Ice-Truck-Cloud/Code/cloud-bridge/.env

# 3. Schlüsseldatei ist vom Git ausgeschlossen (erwartet: Pfad der .env wird ausgegeben)
cd ~/RasberryPI-Team-13 && git check-ignore -v Challenge-III-Ice-Truck-Cloud/Code/cloud-bridge/.env

# 4. Der Key steckt nicht im Repository (erwartet: keine Ausgabe)
git grep -n "THINGSPEAK_WRITE_API_KEY=[A-Z0-9]\{8\}" -- . ':!*.example'

# 5. Dienst läuft und sendet
systemctl is-active cloud-bridge && journalctl -u cloud-bridge -n 5 --no-pager
```

Außerdem als Nachweis: Die Tests (`cloud-bridge/tests/`) prüfen, dass die Datenbank nur
lesend geöffnet wird, der Cursor bei Fehlern stehen bleibt und nach einem Funkloch
nachgeliefert wird.

## 6. Restrisiken und geplante Verbesserungen

| Restrisiko | Auswirkung | Plan |
|---|---|---|
| **Pi-Terminal (ttyd, Port 7681) ohne eigene Anmeldung**, Nutzer `team13` ohne Passwort in der sudo-Gruppe | Wer das Netz (Tailnet) erreicht, kommt auf den Pi und damit an den Write Key | Absichern durch Basic-Auth oder Tailscale-ACL (offener Punkt im Vault) |
| Key liegt im Klartext in `.env` | Wer Root-Zugriff auf den Pi hat, liest ihn | Dateirechte 600; für die Flotte Secret-Store/TPM; Key-Rotation |
| **Ein Write Key pro Kanal**, nicht pro Gerät wie bei Azure | Ein gestohlener Key erlaubt das Schreiben in den ganzen Kanal | Pro Truck ein eigener Kanal mit eigenem Key |
| Kein unveränderliches Archiv bei ThingSpeak | Der Kanalinhaber kann Daten löschen oder ändern | Lokale DB als Original; regelmäßiger CSV-Export; im Produktivbetrieb Azure Blob mit Immutability |
| Keine Batterie-Uhr im Pi: nach Kaltstart ohne Netz zeigt die Uhr kurz eine falsche Zeit | Messungen in dieser Zeit tragen eine falsche Uhrzeit | Dienste erst nach Zeitsynchronisation starten (`After=time-sync.target`), RTC-Modul nachrüsten (offener Punkt im Vault) |
| Free-Tarif ohne Verfügbarkeitszusage | Cloud kann ausfallen | Puffer auf dem Pi überbrückt das; für die Flotte bezahlter Tarif |
| Keine Ende-zu-Ende-Signatur der Messwerte | Ein Angreifer mit dem Key könnte plausible Fälschungen senden | Für den Prototyp nicht nötig; später signierte Nachrichten (z. B. Azure mit Device-Zertifikaten) |
