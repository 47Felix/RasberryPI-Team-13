---
tags: [sicherheit, zugangsdaten, taskcards]
---

# TaskCards-Board (ITECH)

Das Team nutzt ein TaskCards-Board (`itech-bs14.taskcards.app`) für Kursmaterialien/Dokumente des DTEW-Workshops (Haupt-Board "2026 International Design Thinking and Entrepreneurship Workshop Hamburg"). Vollständig inhaltlich ausgewertet am 01.09.2026 (siehe [[DTEW Hamburg - Übersicht]] und [[Team 13 - Digitale Demokratie]] für die Ergebnisse).

> [!warning] Link enthält Zugriffs-Token – bewusst NICHT hier hinterlegt
> Der Board-Link enthält einen `token=`-Parameter, der direkten Zugriff gewährt. Da das Repo öffentlich ist (siehe [[⚠️ Zugangsdaten - Hinweis]]), würde ein Commit des vollständigen Links den Zugriff für jeden offenlegen. Den Link bei Anton/Felix erfragen bzw. wie andere Zugangsdaten außerhalb des Repos ablegen.

## Technische Einschränkung für Claude
TaskCards ist eine reine JavaScript-Single-Page-App (Quasar/Vue) – der HTML-Quelltext ist leer (`<div id=q-app></div>`), Inhalte laden erst per API-Call nach dem Laden. Über **WebFetch kann Claude den Board-Inhalt nicht** auslesen. Über die **Claude-in-Chrome-Browser-Erweiterung** (echter Browser, führt JS aus) funktioniert es aber: Board-URL im Chat mitgeben, Claude öffnet sie im Chrome-Tab und liest Text/Karten mit `get_page_text`/`read_page` aus. Anhänge (PDFs/Bilder) liegen als zeitlich befristete, signierte S3-URLs (`taskcards.s3.hidrive.strato.com/attachments/...`, laufen nach 7 Tagen ab) hinter jeder Karte – per Klick im Chrome-Tab abrufbar. **Download der Anhänge in den Cloud-Workspace klappt aktuell nicht:** die Sandbox-Netzwerk-Allowlist blockiert `taskcards.s3.hidrive.strato.com` (curl liefert `403` am Proxy). PDFs mit echtem Text lassen sich trotzdem per `get_page_text` im geöffneten Tab auslesen; reine Bild-/Canvas-PDFs (z. B. aus draw.io exportierte Vorlagen) nur per Screenshot/Zoom visuell erfassen und danach als Text in eine Notiz übertragen – das Original bleibt dann nur auf dem Board, nicht als Datei im Repo.

## Zusätzliche Einschränkung: nächtliche Cloud-Automation (seit 03.09.2026)
Der nächtliche Scheduled-Task (bereitet jeweils den Folgetag vor, siehe [[DTEW Hamburg - Übersicht]]) läuft nicht über die Claude-in-Chrome-Erweiterung, sondern startet in einer eigenen, isolierten Cloud-Sandbox einen echten headless Chromium via Playwright. Getestet am 03.09.2026 (Vorbereitung für Freitag, 04.09.): Der Zugriffsversuch auf `itech-bs14.taskcards.app` (nicht nur auf die Attachment-Domain wie oben beschrieben) wurde vom Sandbox-Egress-Proxy dieser Umgebung mit `403 Forbidden` auf den `CONNECT`-Tunnel abgelehnt, sowohl per `curl` als auch per Playwright/Chromium. Ergebnis: die Sandbox dieser Automation kann **weder Haupt-/Teams-Board noch Gruppenboard lesen oder bearbeiten**, unabhängig vom eigentlichen Board-Inhalt.

> [!warning] Für künftige Nächte
> Dieses Netzwerk-Limit betrifft die Sandbox-Umgebung, nicht den Token/Link selbst – ein erneuter Versuch in derselben Umgebung wird vermutlich wieder scheitern. Die Board-Schritte der nächtlichen Automation (Teamboard lesen, Gruppenboard-Karte aktualisieren) müssen bis auf Weiteres **morgens live von einem Teammitglied** nachgeholt werden. Vorbereitete Inhalte (Kritische Punkte, Pitch-Stichpunkte, Canvas-Entwürfe etc.) landen weiterhin zuverlässig hier im Vault.

## Verwandte Notizen
- [[⚠️ Zugangsdaten - Hinweis]]

#sicherheit #zugangsdaten #taskcards
