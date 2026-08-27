---
tags: [pi, zugriff]
---

# Pi Zugriff (Team13-1)

## Wie greift Claude auf den Pi zu?
Claude läuft in einer Cloud-Sandbox **ohne** Zugriff auf das Schul-WLAN. Direkter SSH-Zugriff von Claude geht nicht – auch nicht über die Device-Bridge zum Mac (läuft in isolierter VM ohne echten LAN-Zugriff).

**Lösung:** Auf dem Pi läuft ein Web-Terminal (`ttyd`) auf Port 7681. Antons Mac ist im selben WLAN wie der Pi → Chrome auf dem Mac erreicht den Pi. Claude steuert Chrome über `mcp__claude-in-chrome__*`-Tools und tippt darüber im Browser-Terminal, als säße es direkt am Pi.

## Zugriffswege

| Weg | Adresse | Für wen |
|---|---|---|
| Web-Terminal (ttyd) | `http://team13-1.local:7681` | Claude (via Chrome-Steuerung auf Antons Mac) |
| Klassisches SSH | `ssh Team13@Team13-1.local` | Anton selbst, im Mac-Terminal |
| Node-RED Editor | `http://team13-1.local:1880` | Alle (Browser) |
| **Tailscale (seit 27.08.2026)** | `ssh team13@100.100.186.55` (Tailscale-IP, Hostname `team13-1-pi`) | Auch die Discord-Bot-VM (`claudediscord-vm`), da beide im selben Tailnet sind – direkter SSH-Zugriff ohne Chrome-Umweg |

> [!warning] Voraussetzung für SSH
> Klassischer SSH-Zugriff funktioniert nur, wenn der zugreifende Rechner im WLAN "CCiPhone" ist. Tailscale umgeht diese Einschränkung (funktioniert von überall, wo Tailscale erreichbar ist).

> [!danger] Sicherheitsbefund (27.08.2026): ttyd ohne Authentifizierung + passwortloses sudo
> Das ttyd-Web-Terminal (Port 7681) hat **keine eigene Login-Abfrage** – jeder mit Netzwerkzugriff auf den Port bekommt sofort eine `team13`-Shell. `team13` ist ausserdem passwortlos (`NOPASSWD`) in der `sudo`-Gruppe. War bisher durch die LAN-Reichweite (nur Schul-WLAN) einigermassen eingegrenzt, ist aber seit dem Tailscale-Setup fuer das ganze Tailnet erreichbar. **Offen, siehe [[Offene Punkte]]**: ttyd mit Basic-Auth absichern oder per Tailscale-ACL einschraenken.
>
> Das SSH-Passwort fuer `team13` wurde am 27.08.2026 zurueckgesetzt (war vergessen) – neuer Wert steht wie gehabt nicht hier im Vault, siehe [[⚠️ Zugangsdaten - Hinweis]].

## ttyd als systemd-Service
`/etc/systemd/system/ttyd.service`, ExecStart `/home/team13/ttyd -p 7681 -W bash`, `Restart=on-failure`, `enabled`. Startet automatisch bei jedem Boot und bei Absturz automatisch neu.

Status prüfen:
```bash
systemctl is-active ttyd; systemctl is-enabled ttyd
```
Sollte `active` / `enabled` zeigen.

> [!caution] Vorsicht bei Änderungen am ttyd-Service selbst
> Wenn ein Chat den ttyd-Service neu konfiguriert/neu startet (`systemctl restart ttyd` o.ä.), reißt kurzzeitig die eigene Verbindung ab (chicken-and-egg-Problem – man sägt sich selbst den Ast ab). Meist kein Problem: Service kommt sofort wieder hoch, kurz warten, neuen Tab öffnen und `http://team13-1.local:7681` neu laden. Falls nicht: Anton kann per SSH fixen (`sudo systemctl restart ttyd`, ggf. `journalctl -u ttyd -n 30`).

## Zugangsdaten
Siehe [[⚠️ Zugangsdaten - Hinweis]] – aus Sicherheitsgründen nicht hier im Vault hinterlegt.

## Verwandte Notizen
- [[Installierte Services]]
- [[Node-RED Flow - LED Test]]

#pi #zugriff
