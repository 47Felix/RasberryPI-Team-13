---
tags: [sicherheit, zugangsdaten]
---

# ⚠️ Zugangsdaten – bewusst NICHT in diesem Vault

Die tatsächlichen Zugangsdaten (GitHub Access Token, Pi-Login, WLAN-Passwort, Moodle-Logins) stehen **nicht** in diesem Git-Repository – auch nicht, obwohl das Repo privat ist.

## Warum?
- Ein Token/Passwort, das einmal committet wurde, bleibt in der Git-Historie – auch wenn die Datei später gelöscht wird.
- GitHub blockt aktive Tokens beim Push häufig automatisch (Push Protection / Secret Scanning).
- Falls das Repo jemals von privat auf öffentlich umgestellt oder mit Dritten geteilt wird, wären sonst alle Zugangsdaten sofort exponiert.

## Wo stehen die echten Zugangsdaten?
Ausschließlich in den **Projekt-Anweisungen des Claude-Projekts** (nicht in einer eigenen Datei) – dort pflegt Claude sie direkt, außerhalb der Versionskontrolle. Dieses Vault selbst ist zwar die primäre Wissensquelle fürs Projekt (siehe [[🏠 Start]]), aber bewusst ohne Zugangsdaten.

## Betroffen sind u.a.
- GitHub Access Token (Repo: RasberryPI-Team-13)
- Pi-Login (Team13-1 / SSH)
- WLAN-Zugangsdaten (CCiPhone)
- Moodle-Logins

> [!tip] Empfehlung
> Falls ihr die Zugangsdaten auch offline/lokal griffbereit haben wollt, nutzt einen Passwort-Manager oder eine lokale Datei außerhalb des Repos – **nicht** eine Datei, die versehentlich mitcommittet werden könnte.

## Verwandte Notizen
- [[Pi Zugriff]]

#sicherheit #zugangsdaten
