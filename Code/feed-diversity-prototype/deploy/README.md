# Deployment-Vorbereitung: Feed-Diversity-Prototyp öffentlich erreichbar machen

Diese Dateien wurden in einer Cloud-Sandbox-Session **ohne** Zugriff auf die
Team-VM/den Pi vorbereitet (kein SSH, kein Tailscale von hier aus möglich) -
nichts hiervon wurde bereits angewendet. Ein Mensch oder eine Session mit
VM-Zugriff kann die Schritte unten in wenigen Minuten durchgehen.

## Warum Gunicorn statt `python app.py`

`app.py` läuft aktuell über den Flask-Entwicklungsserver
(`app.run(debug=True, port=5050)`). Für alles außer der lokalen Entwicklung
ist das ungeeignet: nicht für gleichzeitige Anfragen ausgelegt, und
`debug=True` öffnet in Produktion ein aktives Sicherheitsrisiko (Werkzeugs
interaktiver Debugger erlaubt beliebige Code-Ausführung über den Browser,
sobald ein Fehler auftritt). `feed-diversity.service` startet stattdessen
Gunicorn (WSGI-Server) mit `debug=False` (impliziter Default, `app.py` selbst
unverändert lassen - der `if __name__ == "__main__"`-Block mit `debug=True`
wird nur beim direkten lokalen Start über `python app.py` erreicht, Gunicorn
importiert nur das `app`-Objekt).

## Schritt für Schritt

Auf der Zielumgebung (Pi/VM mit Root- oder sudo-Zugriff):

```bash
# 1. Code auf die Zielumgebung bringen (Pfad wie in feed-diversity.service)
sudo mkdir -p /opt/feed-diversity-prototype
sudo chown $USER:$USER /opt/feed-diversity-prototype
git clone <repo-url> /tmp/repo-checkout
cp -r /tmp/repo-checkout/Code/feed-diversity-prototype/* /opt/feed-diversity-prototype/

# 2. Eigenen System-User anlegen (nicht als root laufen lassen)
sudo useradd --system --home /opt/feed-diversity-prototype --shell /usr/sbin/nologin feeddiversity
sudo chown -R feeddiversity:feeddiversity /opt/feed-diversity-prototype

# 3. venv + Abhängigkeiten (inkl. gunicorn, siehe requirements.txt)
cd /opt/feed-diversity-prototype
sudo -u feeddiversity python3 -m venv venv
sudo -u feeddiversity venv/bin/pip install -r requirements.txt

# 4. .env anlegen (SUPABASE_URL/SUPABASE_PUBLISHABLE_KEY/SUPABASE_SECRET_KEY,
#    FLASK_SECRET_KEY, optional ADMIN_DASHBOARD_TOKEN fuer /dashboard -
#    siehe README.md des Prototyps). NIE ins Repo committen.
sudo -u feeddiversity nano /opt/feed-diversity-prototype/.env

# 5. Supabase-Migrationen einmalig anwenden, falls noch nicht geschehen
#    (siehe README.md des Prototyps, Abschnitt "Accounts, Posts, ...")

# 6. systemd-Unit einrichten
sudo cp deploy/feed-diversity.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now feed-diversity
sudo systemctl status feed-diversity   # sollte "active (running)" zeigen

# 7. Caddy installieren (falls noch nicht vorhanden) und Caddyfile einrichten
#    https://caddyserver.com/docs/install
sudo cp deploy/Caddyfile /etc/caddy/Caddyfile
#    Vorher perspektiv.example.org im Caddyfile durch die echte Domain ersetzen!
sudo systemctl reload caddy
```

Danach ist die Seite unter `https://<domain>` erreichbar - Caddy holt das
TLS-Zertifikat automatisch (Let's Encrypt), solange die Domain per DNS auf
diesen Server zeigt und Port 80/443 von außen erreichbar sind (siehe
Firewall-Hinweis unten).

## Azure-NSG-Firewall: Ports 80/443 öffnen

Falls die Ziel-VM in Azure läuft (Network Security Group blockt eingehenden
Verkehr standardmäßig): in der Azure-Portal-NSG der VM zwei eingehende
Regeln ergänzen (oder per `az network nsg rule create`):

- Port 80/TCP (HTTP, nötig für die automatische Let's-Encrypt-Zertifikats-
  Ausstellung/Erneuerung durch Caddy, auch wenn die App selbst nur über 443
  benutzt wird)
- Port 443/TCP (HTTPS, der eigentliche App-Zugriff)

Quelle je nach gewünschter Reichweite: `Any` für öffentlichen Zugriff (siehe
Abwägung unten), oder eine engere Quelle, falls nur bestimmte IP-Bereiche
zugelassen werden sollen.

## Alternative: Tailscale-only statt öffentlichem Zugriff

Das Team nutzt für den Pi-Zugriff bereits Tailscale (siehe `ObsidianGehirn/02
Pi Setup/Pi Zugriff.md`), unter anderem weil das ttyd-Web-Terminal dort einen
offenen, bisher ungelösten Sicherheitsbefund hat (keine eigene
Authentifizierung, passwortloses `sudo` für den `team13`-User, seit dem
Tailscale-Setup fürs ganze Tailnet statt nur das Schul-WLAN erreichbar). Das
ist ein Grund, mit einem *Terminal* vorsichtig zu sein, aber kein
grundsätzlicher Beschluss gegen öffentlichen Zugriff für alles: eine
Lese-/Demo-Webseite ohne Shell-Zugriff ist ein deutlich kleineres Risiko.
Für diesen Prototyp ist eine öffentlich erreichbare Demo-Seite außerdem der
eigentliche Zweck (Vorführung, digi&demo e.V., Peer Feedback), nicht nur ein
internes Werkzeug - deshalb ist oben der öffentliche Weg vorbereitet.

Falls das Team trotzdem lieber **nicht** öffentlich gehen möchte (z.B. für
eine reine Team-interne Vorschau vor der eigentlichen Präsentation): Caddyfile
und NSG-Schritt oben einfach weglassen, stattdessen Gunicorn direkt an
`127.0.0.1:8000` binden lassen (schon so in `feed-diversity.service`
konfiguriert) und nur über Tailscale erreichen (`tailscale serve` oder direkt
per Tailscale-IP + Port, ohne TLS-Zertifikat nötig, da der Tailscale-Tunnel
selbst verschlüsselt). Kein NSG-Port muss dafür geöffnet werden - das ist der
sicherere Standardweg, wenn kein öffentlicher Zugriff gebraucht wird.

## Was diese Vorbereitung NICHT macht

- Kein Deployment wurde ausgeführt - diese Session hat keinen Zugriff auf
  die Ziel-VM.
- Kein Domain-Name ist hier fest verdrahtet (`perspektiv.example.org` ist ein
  Platzhalter im Caddyfile).
- Keine Supabase-Migrationen wurden angewendet (siehe Haupt-README des
  Prototyps und `NIGHTLY_TASK.md`).
