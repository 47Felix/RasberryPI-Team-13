# Challenge III - Ice Truck in Cloud (Code-Ueberblick)

Bezieht sich auf die Vault-Notiz `ObsidianGehirn/03 Moodle Kurs/Challenge III - Ice Truck in Cloud.md`
(Aufgabenstellung, Entscheidungsmatrix, NIST-Nachweis, Fortschritt).

## Architektur

```
Arduinos -> pi-backend (SQLite) -> Node-RED -> lokaler Mosquitto (Challenge II)
                                                   |  Bridge (TLS 8883, QoS 1, gepuffert)
                                                   v
  ===================== gemietete Cloud-VM (IaaS, Azure) =====================
  Mosquitto (TLS, Auth, ACL) -> Telegraf -> InfluxDB -> Grafana (HTTPS via Caddy)
```
Lokale SQLite bleibt als Fallback/Puffer; die Cloud ist die zusaetzliche, standortunabhaengige Sicherung.

## Ordner
| Pfad | Zweck |
|---|---|
| `Code/cloud-server/` | docker-compose Stack fuer die VM (Broker, Zeitreihen-DB, Dashboards) |
| `Code/pi-bridge/team13-cloud-bridge.conf` | Mosquitto-Bridge auf dem Pi -> Cloud |
| `Code/analysis/flux-queries.md` | Auswertungen / Predictive-Maintenance-Beispiele |

## Deployment (Kurzform, braucht VM + DNS-Name)
1. VM (Azure, Ubuntu) mit Docker; NSG/Firewall: 80, 443, 8883 offen, 22 nur eigene IP. 8086/1883 NICHT oeffnen.
2. DNS-Name auf die VM zeigen lassen (z. B. `icetruck-team13.<region>.cloudapp.azure.com`).
3. Zertifikat: `sudo certbot certonly --standalone -d <hostname>` (vor `docker compose up`, Port 80 frei).
4. `cd Code/cloud-server && cp .env.example .env` und Werte setzen.
5. Passwoerter anlegen:
   `docker run --rm -it -v $PWD/mosquitto:/m eclipse-mosquitto:2 sh -c "touch /m/passwd && mosquitto_passwd -b /m/passwd pi-bridge <pw> && mosquitto_passwd -b /m/passwd telegraf <pw>"`
6. `docker compose up -d`, Grafana unter `https://<hostname>` oeffnen.
7. Pi: `team13-cloud-bridge.conf` anpassen, nach `/etc/mosquitto/conf.d/`, `sudo systemctl restart mosquitto`.
8. Test: `mosquitto_sub -h <hostname> -p 8883 --capath /etc/ssl/certs -u telegraf -P <pw> -t 'team13-1/icetruck/#' -v`

## Status
Alles hier ist **entworfen, aber noch nicht deployt/getestet** (kein VM-/Pi-Zugriff aus dieser Session,
nur `docker-compose.yml` per YAML-Parser geprueft). Zugangsdaten stehen nie im Repo (siehe Vault `Zugangsdaten - Hinweis`).
