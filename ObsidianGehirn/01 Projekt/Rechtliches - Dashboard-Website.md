---
tags: [projekt, pi-dashboard, recht, datenschutz]
---

# Rechtliches: Pi-Dashboard-Website

> [!info] Stand
> 08.09.2026 – Impressum- und Datenschutz-Seite plus technische Basics ins Dashboard eingebaut (PR folgt, Branch `code/dashboard-rechtliches`). **Noch offen:** echte Betreiber-/Kontaktdaten eintragen und den Text von der Lehrkraft gegenlesen lassen (siehe "Was das Team noch tun muss").

Ausgangspunkt war die Frage im Chat, welche rechtlichen Sachen eine Website wie unser [[Erweiterung - Raspberry Pi Dashboard|Tresor-Dashboard]] braucht. Das Dashboard ist zwar nicht offen im Internet (nur Schul-WLAN + Tailnet, siehe [[Pi Zugriff]]), aber sobald es von aussen erreichbar ist, gelten die Pflichten unten. Als Uebung fuers Lernfeld ist es ohnehin sinnvoll, das sauber zu haben.

Kein Rechtsrat, nur eine Umsetzung nach bestem Wissen. Vor einer echten Veroeffentlichung von der Lehrkraft absegnen lassen.

## Was rechtlich relevant ist (Kurzueberblick)

| Thema | Rechtsgrundlage | Status im Dashboard |
|---|---|---|
| Impressum | § 5 DDG, § 18 MStV | Seite `/impressum`, Daten aus `.env` |
| Datenschutzerklaerung | Art. 13 DSGVO | Seite `/datenschutz` |
| Cookie-Einwilligung | § 25 TDDDG | Nicht noetig: nur technisch notwendiges Session-Cookie, kein Tracking |
| Transportverschluesselung | Art. 32 DSGVO | HSTS + Secure-Cookies via `DASHBOARD_HTTPS=1`, sobald ein HTTPS-Proxy davor haengt |
| Datenminimierung Logs | Art. 5 Abs. 1 lit. c DSGVO | Werkzeug-Zugriffslog standardmaessig aus |
| Sicherheits-Header | Art. 32 DSGVO ("Stand der Technik") | CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy |
| Drittlandtransfer | Art. 44 ff. DSGVO | Nur bei aktivem Discord-Alarm, in der Datenschutzerklaerung benannt, keine personenbezogenen Daten in der Meldung |
| Urheberrecht | UrhG | Keine Fremd-Assets: alles selbst geschrieben, keine CDNs/Fonts/Icons von Dritten |
| Barrierefreiheit (BFSG) | BFSG (seit 28.06.2025) | Trifft ein reines Schulprojekt ohne Geschaeftsverkehr nicht, WCAG bleibt trotzdem gute Uebung |

## Was im Code umgesetzt wurde (`Code/pi-dashboard/`)

- **`/impressum`** und **`/datenschutz`** als eigene Seiten, in `base.html` per Footer auf **jeder** Seite verlinkt (2-Klick-Regel).
- Betreiber-, Kontakt- und Verantwortlichen-Angaben kommen aus **Umgebungsvariablen** (`.env` auf dem Pi), nicht aus dem Repo. Fehlt ein Wert, zeigt die Seite an der Stelle einen gelben "noch auszufuellen"-Kasten, statt falsche oder leere Angaben zu machen.
- **Session-Cookie gehaertet**: `HttpOnly`, `SameSite=Lax`, `Secure` abhaengig von `DASHBOARD_HTTPS`.
- **Sicherheits-Header** ueber `after_request`: Content-Security-Policy (nur eigene Quellen, `unsafe-inline` noetig wegen der Inline-Styles/-Skripte im Template), `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, bei HTTPS zusaetzlich HSTS.
- **Zugriffs-Logging aus**: der Werkzeug-Logger wird auf `WARNING` gesetzt, damit nicht pro Request eine Zeile mit Client-IP ins Journal geht. Mit `DASHBOARD_ACCESS_LOG=1` zum Debuggen wieder anschaltbar.
- Datenschutz-Text beschreibt die tatsaechlichen Verarbeitungen dieser App: Server-Logs, Admin-Session-Cookie, SQLite-Ereignisprotokoll (nur Geraete-Events, keine Namen/Codes), optionaler Discord-Alarm. Der Discord-Abschnitt schaltet automatisch zwischen "aktiv/Drittland" und "nicht konfiguriert" um, je nachdem ob `DISCORD_BOT_TOKEN` + `DISCORD_ALARM_CHANNEL_ID` gesetzt sind.

## Neue Umgebungsvariablen (`.env` auf dem Pi)

| Variable | Zweck | Pflicht? |
|---|---|---|
| `DASHBOARD_IMPRESSUM_NAME` | Betreiber (Person bzw. Schule/Traeger) | ja, vor Veroeffentlichung |
| `DASHBOARD_IMPRESSUM_ADDRESS` | ladungsfaehige Anschrift | ja |
| `DASHBOARD_IMPRESSUM_CONTACT` | Kontakt (E-Mail + zweiter Weg); alternativ `DASHBOARD_CONTACT_EMAIL` | ja |
| `DASHBOARD_IMPRESSUM_RESPONSIBLE` | inhaltlich Verantwortliche/r nach § 18 Abs. 2 MStV | ja |
| `DASHBOARD_DATENSCHUTZ_AUFSICHT` | zustaendige Datenschutz-Aufsichtsbehoerde (Bundesland der Schule) | empfohlen |
| `DASHBOARD_HTTPS` | `1`, wenn ein HTTPS-Proxy/Tailscale-Serve davor haengt (aktiviert Secure-Cookies + HSTS) | nur bei HTTPS |
| `DASHBOARD_ACCESS_LOG` | `1` reaktiviert das Zugriffs-Logging mit IP fuer die Fehlersuche | nein |

## Was das Team noch tun muss

- [ ] Entscheiden, **wer** als Verantwortlicher im Impressum steht (ein Teammitglied privat oder die Schule/der Ausbildungstraeger, dann vorher dort fragen).
- [ ] Die vier `DASHBOARD_IMPRESSUM_*`-Variablen in der `.env` auf dem Pi setzen (Werte stehen bewusst nicht hier im Vault, siehe [[⚠️ Zugangsdaten - Hinweis]]). Danach greift der Env-Reload-Watcher automatisch, kein Neustart noetig.
- [ ] Konkrete Aufsichtsbehoerde eintragen (`DASHBOARD_DATENSCHUTZ_AUFSICHT`), je nach Bundesland der Schule.
- [ ] Impressum- und Datenschutz-Text von der Lehrkraft gegenlesen lassen, bevor das Dashboard aus dem reinen Klassenkontext heraus erreichbar gemacht wird.
- [ ] Falls dauerhaft ueber HTTPS erreichbar (z.B. `tailscale serve`): `DASHBOARD_HTTPS=1` setzen.
- [ ] "Stand"-Datum in `impressum.html` / `datenschutz.html` anpassen, wenn der Text inhaltlich geaendert wird.

## Deploy auf dem Pi (nach Merge)

```bash
cp Code/pi-dashboard/app.py ~/tresor-dashboard/app.py
cp Code/pi-dashboard/templates/*.html ~/tresor-dashboard/templates/
# .env um die DASHBOARD_IMPRESSUM_*-Zeilen ergaenzen
sudo systemctl restart tresor-dashboard
```

## Verwandte Notizen
- [[Erweiterung - Raspberry Pi Dashboard]]
- [[Pi Zugriff]]
- [[Offene Punkte]]

#projekt #pi-dashboard #recht #datenschutz
