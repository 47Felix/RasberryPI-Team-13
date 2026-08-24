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
