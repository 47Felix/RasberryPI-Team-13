---
tags: [moodle, challenges, cloud, thingspeak, alarm]
---

# Challenge III – Alarme über ThingSpeak (Discord + Mail)

Stand 07.10.2026. Gehört zu [[Challenge III - Ice Truck in Cloud]]. Zählt im Bewertungsbogen unter **„Zusätzliche Funktionen“ (/5)**. Das Protokoll der Messdaten (/10) ist der ThingSpeak-Channel, nicht Discord (siehe unten).

> **Keine Keys ins Repo oder in den Chat.** Webhook-URL, Read-Key und Alerts-API-Key stehen nur in der MATLAB Analysis in ThingSpeak. Am 07.10.2026 wurden sie versehentlich in den Chat geschrieben und mussten erneuert werden (Discord-Webhook neu anlegen, Alerts-Key und Read-Key in ThingSpeak neu generieren).

## Aufbau (läuft komplett in der Cloud, der Pi wird nicht gebraucht)

```
Pi → ThingSpeak-Channel (Field 3 = Temperatur)
        └─ React: Field 3 > 30, "On Data Insertion", nur beim ersten Mal
              └─ Action: MATLAB Analysis
                    ├─ Discord-Webhook (POST)
                    └─ ThingSpeak Alerts API (E-Mail)
```

React-Einstellungen: Condition Type `Numeric`, Test Frequency `On Data Insertion`, Field 3 `is greater than` 30, **Option „Run action only the first time the condition is met“** (sonst Nachricht pro Messung, Mail-Limit schnell erreicht).

## MATLAB Analysis (Platzhalter statt Keys)

```matlab
channelID   = <CHANNEL_ID>;
readKey     = '<READ_KEY>';              % nur bei privatem Channel nötig
webhook     = '<DISCORD_WEBHOOK_URL>';
alertApiKey = '<ALERTS_API_KEY>';        % beginnt mit TAK, Profil -> My Profile
grenzwert   = 30;
mailAn      = true;                      % beim Testen false (Mail-Limit!)

[temp, ts] = thingSpeakRead(channelID, 'Fields', 3, 'ReadKey', readKey);
ts.TimeZone = 'UTC';                     % thingSpeakRead liefert UTC
ts.TimeZone = 'Europe/Berlin';           % dann umrechnen (MEZ/MESZ automatisch)
zeit = char(ts, 'dd.MM.yyyy HH:mm:ss');

if temp > grenzwert
    % --- Discord ---
    msg = sprintf('ALARM Ice Truck: %.1f °C (Grenzwert %d °C) am %s', temp, grenzwert, zeit);
    try
        webwrite(webhook, struct('content', msg), ...
            weboptions('MediaType', 'application/json', 'UserAgent', 'IceTruckAlert/1.0'));
    catch ME
        disp(['Discord: ' ME.message]);
    end

    % --- E-Mail (nur ASCII, JSON per jsonencode) ---
    if mailAn
        subject = 'Ice Truck Alarm: Temperatur zu hoch';
        body    = sprintf('Temperatur %.1f Grad (Grenzwert %d Grad) am %s. Bitte Kuehlung pruefen.', temp, grenzwert, zeit);
        json    = jsonencode(struct('subject', subject, 'body', body));
        opts    = weboptions('HeaderFields', ["ThingSpeak-Alerts-API-Key", alertApiKey; ...
                                              "Content-Type", "application/json"]);
        try
            webwrite("https://api.thingspeak.com/alerts/send", json, opts);
        catch ME
            disp(['Mail: ' ME.message]);
        end
    end
else
    disp(sprintf('Kein Alarm: %.1f °C', temp));
end
```

Der Code ist nicht gegen ein Test-Setup außerhalb unseres Kontos geprüft. Die Discord-Nachricht und die Mail kamen aber in unseren Tests an.

## Was wir gelernt haben (Stolperfallen)

| Problem | Ursache | Lösung |
|---|---|---|
| `????` statt Emoji in Discord | ThingHTTP verträgt keine Emojis im Body | Emoji weglassen, oder MATLAB Analysis (Struct wird sauber kodiert) |
| `%25%25channel_..._field_3%25%25` in der Nachricht | Platzhalter URL-kodiert und Channel-ID nicht ersetzt | Echte Channel-ID, `%%` tippen. Wert blieb bei uns trotzdem leer → MATLAB Analysis |
| Wert im ThingHTTP-Platzhalter leer | ThingHTTP nicht von React ausgelöst, falsche ID/Feldnummer oder privater Channel | MATLAB Analysis liest den Wert selbst per `thingSpeakRead` |
| Zeit in der Nachricht 2 Stunden falsch | `thingSpeakRead` liefert UTC, `TimeZone='Europe/Berlin'` allein benennt nur um | Erst `'UTC'`, dann `'Europe/Berlin'` setzen |
| Alarm bei 25 °C trotz Grenzwert 30 | Code liest immer den **letzten** Eintrag, auch bei manuellem Start | `if temp > grenzwert` im Code |
| Mail kommt nicht, `429 Too Many Requests` | Limit für Alert-Mails im Free-Konto beim Testen erreicht | Warten, nicht mehr dutzendfach testen, `mailAn=false` beim Entwickeln |
| Mail zerhackt/fehlend | `°`/`ü` im selbst gebauten JSON-String | Nur ASCII und `jsonencode` |
| Discord 403 | Cloudflare blockt Standard-User-Agent | Eigener `UserAgent` in `weboptions` |

Weitere Hinweise:
- Die Mail geht immer an die **Adresse des ThingSpeak-Kontos**, ein anderer Empfänger ist nicht einstellbar.
- ThingSpeak hängt an jede Alert-Mail selbst eine Zeile „Time: … +0000“ (UTC-Sendezeit) an. Sie lässt sich nicht ändern.
- Das genaue Mail-Limit kennen wir nicht. Vor der Präsentation in den aktuellen MathWorks-Bedingungen nachlesen, bevor wir eine Zahl nennen.
- Zum Testen ohne Pi: `https://api.thingspeak.com/update?api_key=<WRITE_KEY>&field3=35`, dazwischen einen Wert unter 30 schicken (wegen „nur beim ersten Mal“). Free-Limit: etwa alle 15 s ein Wert.
- Discord-Bot-Profilbild im Webhook auf ein neutrales Icon (Thermometer/Warnschild) stellen statt Foto.

## „Protokollieren“ – Discord oder ThingSpeak?
Der Bogen verlangt: *„Die Messdaten werden in einer Cloud protokolliert und können visualisiert werden“* (/10). Gemeint sind die **Messdaten**:

- **Protokoll = ThingSpeak-Channel.** Jeder Messwert mit Original-Zeitstempel (`created_at`), Diagramme, CSV-Export. Bei Funkloch holt `bridge.py` den Rückstand mit Originalzeit nach.
- **Discord = Benachrichtigung** (zählt unter „Zusätzliche Funktionen“). Als Protokoll ungeeignet: Nachrichten sind löschbar/bearbeitbar, keine strukturierten Werte, kein sauberer Export.
- **Nachweis für den Alarm:** CSV-Export des Alarmzeitraums + Discord-Screenshot (Zeit und Wert passen zusammen).
- Optional (nur bei Zeit übrig): zweiter Channel „Alarm-Log“, in den die Analysis jeden Alarm schreibt. Bringt für den Bogen kaum Punkte.

## Präsentations-Merkliste (07.10.2026)

1. **Pi bis zur Vorstellung durchlaufen lassen**, damit das Diagramm Verlauf, Alarm und Erholung zeigt.
2. **Offline-Test einmal machen:** WLAN am Pi trennen, 5 Min warten, wieder verbinden → Rückstand kommt nach (Argument für „lückenlos“).
3. **Screenshots vorbereiten:** ThingSpeak-Diagramm, Discord-Alarm, Alarm-Mail, CSV-Export.
4. **Ehrlich sagen, was Grenzen sind:** ThingSpeak Free (≈3 Mio. Nachrichten/Jahr, Mail-Limit, Server in den USA = Drittlandübermittlung). Für echten Jahresnachweis (VO 178/2002, 37/2005) regelmäßig per CSV sichern oder zu Azure Blob Storage (Immutability) wechseln. Wie lange ThingSpeak Free die Daten hält, vorher in den MathWorks-Bedingungen prüfen, nicht als Fakt nennen.
5. **Einordnung:** ThingSpeak = **SaaS**, Azure IoT Hub = PaaS, eigene VM = IaaS. Azure war am 30.09.2026 nicht erreichbar → Plan B ThingSpeak.
6. **Folie „sichere Datenübertragung“ (/10) fehlt noch:** Pi → HTTPS/TLS → ThingSpeak, Write-Key nur in `.env` auf dem Pi, Webhook-URL und Alerts-Key nur in ThingSpeak, nichts davon im Repo. Azure-Variante: MQTT über TLS 1.2, Device-Schlüssel.
7. **Beim Live-Test nur einen Alarm auslösen** (nicht dutzende, wegen Mail-Limit), `mailAn=true` nur dafür.
8. **Datenschutz-Satz:** Temperaturdaten ohne Personenbezug, daher vertretbar. Bei GPS/Fahrerdaten nicht ohne Weiteres (DSGVO Kap. V).

#moodle #challenges #cloud
