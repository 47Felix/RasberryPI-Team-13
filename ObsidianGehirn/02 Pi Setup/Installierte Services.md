---
tags: [pi, services]
---

# Installierte/eingerichtete Software auf dem Pi

Stand 24.08.2026.

## Betriebssystem
Raspberry Pi OS, Debian **"trixie"**, 64-bit (aarch64)

## NTP-Zeitsynchronisation
Eingerichtet über `systemd-timesyncd` (**nicht** das alte `ntp`-Paket – gibt es unter Trixie nicht mehr) mit den ITECH-Zeitservern `10.14.213.11`, `10.14.213.12`, `10.14.213.13` in `/etc/systemd/timesyncd.conf`.

Status prüfen:
```bash
timedatectl timesync-status
```

## Mosquitto (MQTT-Broker)
`mosquitto`, `mosquitto-clients` installiert, läuft als systemd-Service, Autostart aktiv. Standardport **1883**.

**Update 23.09.2026 (Challenge II Track A, #193):** Debian-Mosquitto band ohne eigene Config nur auf `127.0.0.1`/`::1` - für Node-RED lokal ausreichend, aber von keinem Handy/Tablet erreichbar. Zusatzkonfiguration `/etc/mosquitto/conf.d/team13-icetruck.conf` (Kopie im Repo unter `Challenge-II-Ice-Truck-Extension/Code/mosquitto/`) öffnet einen Listener auf `0.0.0.0:1883`, mit Passwort-Pflicht (`allow_anonymous false`, ein Nutzer `team13-1`) und einer ACL (`/etc/mosquitto/acl`), die den Nutzer auf `team13-1/#` beschränkt. End-to-end getestet (authentifizierter Pub/Sub-Roundtrip über die Tailscale-IP, anonyme Verbindung wird abgelehnt). Zugangsdaten stehen nicht hier, siehe [[⚠️ Zugangsdaten - Hinweis]]. Details/Status siehe `Challenge-II-Ice-Truck-Extension/Code/README.md`.

## Node.js
v22.23.2 über das offizielle NodeSource-Repo (`deb.nodesource.com/node_22.x`) – **nicht** über das normale Debian-Repo (liefert nur v20, zu alt für aktuelles Node-RED).

## Node-RED
v5.0.4, global per npm installiert, eigener systemd-Service (`/etc/systemd/system/nodered.service`, User `team13`, `Restart=on-failure`, Autostart aktiv). Läuft dauerhaft, auch nach Neustart.

- Zusatz-Node `node-red-node-pi-gpio` installiert (GPIO-Zugriff via "rpi gpio in/out"-Nodes)
- Siehe [[Node-RED Flow - LED Test]] für den aktuellen Flow

## ttyd (Web-Terminal)
`/home/team13/ttyd`, systemd-Service `ttyd.service`, Autostart aktiv. Details: [[Pi Zugriff]]

## Verwandte Notizen
- [[Pi Zugriff]]
- [[Node-RED Flow - LED Test]]
- [[Technischer Fahrplan]]

#pi #services
