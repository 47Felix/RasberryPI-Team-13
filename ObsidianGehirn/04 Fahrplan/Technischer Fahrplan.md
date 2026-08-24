---
tags: [fahrplan, projekt]
---

# Empfohlener technischer Fahrplan (Team13-1)

Basierend auf den Kursinhalten, für unseren Pi mit Hostname "Team13-1" im WLAN "CCiPhone".

1. **OS aufsetzen** – Aktuelles Raspberry Pi OS mit Raspberry Pi Imager, SSH direkt aktiviert, WLAN vorkonfiguriert. ✅ erledigt
2. **SSH-Verbindung herstellen** – `ssh Team13@Team13-1.local`. ✅ erledigt, siehe [[Pi Zugriff]]
3. **Zeit synchronisieren (NTP)** – ITECH-Server, siehe [[Installierte Services]]. ✅ erledigt
4. **Linux-Grundlagen auffrischen** – Verzeichnisstruktur, Rechte, Basisbefehle, siehe [[Kurs - Linux Grundlagen]]
5. **Git installieren und Projekt-Repository klonen**:
   ```bash
   sudo apt update && sudo apt install git -y
   git clone https://github.com/47Felix/RasberryPI-Team-13.git
   ```
   ⏳ noch offen, siehe [[Offene Punkte]]
6. **Elektrotechnische Grundlagen auffrischen** – siehe [[Kurs - Elektrotechnik]]
7. **Sensoren/Aktoren anschließen und ansteuern** – erster Test (LED an GPIO4) softwareseitig vorbereitet, Hardware-Aufbau offen, siehe [[Node-RED Flow - LED Test]]
8. **Node-RED installieren und GPIOs ansteuern** ✅ erledigt, siehe [[Kurs - Node-RED]] und [[Installierte Services]]
9. **MQTT einbinden** ✅ Broker läuft, ⏳ Verknüpfung mit Node-RED noch offen, siehe [[Kurs - MQTT]]
10. **Fernzugriff von außerhalb** (analog Challenge II) – DynDNS, ggf. Apache-Webserver/eigenes Dashboard. ⏳ noch offen
11. **Optional: Datenbankanbindung** für Messdatenspeicherung – Kurs-ID 564, aktuell durch Kennwort gesperrt

## Verwandte Notizen
- [[Offene Punkte]]
- [[Roter Faden - Ice Truck]]

#fahrplan #projekt
