---
tags: [dtew, workshop, digitale-demokratie]
---

# DTEW 0912 (Samstag) – Freier Tag, optionale Bremen-Exkursion & Workshop-Abschluss

Vorbereitung für Samstag, 12.09.2026 (siehe [[DTEW Hamburg - Übersicht]]). Laut Zeitplan ist Samstag 12.09. der **letzte Tag in Deutschland zur freien Verfügung** – es gibt kein offizielles Workshop-Pflichtprogramm mehr, nur eine optionale Bremen-Exkursion. Das ist damit der letzte Tag des zweiwöchigen DTEW-Zeitraums (31.08.–12.09.); Case 3 – Feed-/Recommender-Design gegen Bubble-Verstärkung, Personas Mia/Tom, Prototyp "Perspective Compass" – wurde laut [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] bereits am 10.09. final vorgestellt (Blogpost, 1-Minuten-Pitch, Innovation Fair, Farewell Party). Wie an den Vortagen: Alles mit 📝 markiert **muss vor Ort/live im Team passieren**, kein Schreibtisch-Ersatz möglich.

> [!danger] Board-Zugriff heute Nacht erneut geprüft – erneut mit derselben Policy-Ablehnung gescheitert
> Live getestet (Playwright/Chromium aus dieser Cloud-Sandbox, wie in der Aufgabenstellung gefordert): `page.goto` auf das Haupt-/Teams-Board schlägt mit `net::ERR_TUNNEL_CONNECTION_FAILED` fehl. Der Proxy-Status-Endpoint (`$HTTPS_PROXY/__agentproxy/status`) bestätigt einen frischen `recentRelayFailures`-Eintrag: `connect_rejected` / `403` auf den `CONNECT`-Tunnel zu `itech-bs14.taskcards.app:443` – **derselbe Fehler wie bei `www.google.com:443`**, also eine generelle Richtlinien-Ablehnung dieser Sandbox-Umgebung für praktisch alle externen Hosts außerhalb einer Allowlist, kein taskcards-spezifisches oder temporäres Problem. Damit weiterhin identisch zum seit 03.09. dokumentierten Befund (siehe [[TaskCards Board]]).
> - **Zu Issue [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100)** ("Board-Zugriff der Nacht-Automation repariert", offen seit 07.09.): Der dort beschriebene Fix ist ein **lokaler Cronjob (`board-sync.sh`) auf der Team-VM** – ein anderer Ausführungskontext als diese isolierte Cloud-Sandbox-Session. Die zwei Kontexte sind vermutlich unabhängig: `board-sync.sh` auf der VM kann durchaus laufen, während diese Cloud-Automation (dieselbe, die auch diese Notiz schreibt) strukturell nie an das Board herankommt, weil die Sandbox-Netzwerk-Policy es blockt – nicht, weil der Fix fehlerhaft wäre.
> - Aufgabenliste unten stammt deshalb wie an den Vortagen **nur aus der Übersicht** (Stand Board 01.09.), nicht aus einer tagesaktuellen Samstags-Karte.
> - Team-13-Karte auf dem Gruppenboard konnte weder gelesen noch aktualisiert werden – Text unten zum Reinkopieren vorbereitet.
> - **Letzte Nacht des Workshop-Zeitraums:** Nach heute gibt es laut Übersicht keinen weiteren Workshop-Tag mehr, auf den diese Automation vorbereiten müsste. Ob die nächtliche DTEW-Vorbereitung danach noch benötigt wird, ist eine Team-Entscheidung – siehe "Was noch fehlt" unten. Falls `board-sync.sh` auf der VM tatsächlich zuverlässig lief, wäre es sinnvoll, das in Issue [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100) einmal explizit zu bestätigen (z. B. per Log-Check), bevor der Workshop endgültig abgeschlossen wird – die Diskrepanz aus [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]] wurde nie aufgelöst.

## Aufgaben von morgen (laut Übersicht, Stand Board 01.09. – s. Warnkasten zur Unsicherheit)
- **Kein Pflichtprogramm** – Samstag 12.09. ist der letzte Tag in Deutschland zur freien Verfügung
- Optionale Exkursion: **Bremen** (Altstadt, Rathaus/Roland, Schnoorviertel, Böttcherstraße)
- Kein weiterer offizieller Workshop-Termin danach (12.09. ist laut Zeitplan das Ende des DTEW-Zeitraums 31.08.–12.09.)

## 📝 Nur vor Ort/live möglich
- **Entscheidung, ob/wie die Bremen-Exkursion stattfindet** – reine Team-Präferenz, nicht vorwegnehmbar
- **Echtes Board morgens früh prüfen** – falls doch noch eine Samstags-Karte existiert oder sich seit der letzten Prüfung (10.09.) etwas geändert hat, insbesondere ob `board-sync.sh` zwischenzeitlich lief (siehe Warnkasten)
- **Team-13-Karte auf dem Gruppenboard final aktualisieren** – Text unten fertig zum Reinkopieren, sobald das Board erreichbar ist
- **Abschluss-Checkliste unten im Team durchgehen** – das ist die letzte reguläre Gelegenheit vor der Abreise, die seit Tagen offenen Punkte zu klären

## ✅ Vorbereitet: Abschluss-Checkliste (letzter Tag – vor der Abreise klären)

Alle folgenden Punkte stehen laut GitHub-Issue-Tracker weiterhin offen (Stand heute Nacht, `kanban:todo`), einige seit über einer Woche. Da nach heute kein Workshop-Tag mehr folgt, ist dies die letzte Gelegenheit, sie im Team direkt zu klären statt sie auf "danach" zu verschieben:

1. **Sicherheitsrelevant, höchste Priorität:** Geleakten Supabase-Token widerrufen ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92)) – seit dem Sicherheitsvorfall vom 04.09. offen. Sollte unabhängig vom Workshop-Ende zeitnah erledigt werden, da der Prototyp weiterhin live deployed ist (siehe [[Feed-Diversity-Prototyp - Deployment]]).
2. Produktname final entscheiden ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)) – Arbeitstitel "Perspective Compass" wurde im Pitch/Blogpost vom 10.09. bereits so verwendet, ohne dass eine Team-Entscheidung dokumentiert ist.
3. Logo visuell gestalten ([#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96)) – Entwurf von dnbk72 existiert laut [[DTEW - Strategie-Praesentation]] bereits, nur noch nicht final übernommen.
4. Rollen im Team festlegen (Scrum Master/Product Owner) ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)) – seit dem Sprint-Ende am 07.09. wiederholt als offen vermerkt.
5. Retrospektive nachholen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98)) – "was lief gut/schlecht" über die zwei Wochen, jetzt mit vollständigem Rückblick möglich.
6. Donnerstag (03.09.) rückwirkend dokumentieren ([#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97)) – einzige Lücke in der Tagesnotizen-Reihe.
7. Team-Zusammensetzung klären (Anton) – taucht laut [[DTEW Hamburg - Übersicht]] nicht in `groups_2026.xlsx` auf; wurde im Blogpost-Entwurf vom 10.09. als offene Frage markiert und sollte vor der endgültigen Veröffentlichung geklärt sein, falls das nicht schon vor Ort passiert ist.
8. Nächtliche DTEW-Automation: entscheiden, ob sie nach heute noch benötigt wird (siehe Warnkasten oben) – falls nicht, sollte der zugehörige Scheduled Task/Trigger deaktiviert werden, statt nachts weiter erfolglos gegen die Sandbox-Policy zu laufen.

> [!tip] Für die Live-Runde
> Punkt 1 (Token) ist unabhängig vom Workshop-Ende sicherheitsrelevant und sollte priorisiert werden. Punkte 2–6 sind reine Aufräumarbeiten, die sich am letzten Tag ohne Zeitdruck erledigen lassen. Punkt 7 betrifft die externe Blogpost-Veröffentlichung, falls die noch nicht final ist. Punkt 8 ist eine Automations-/Tooling-Entscheidung, keine Case-Arbeit.

## ✅ Vorbereitet: Team-13-Karte fürs Gruppenboard (Abschlussstand, zum Reinkopieren sobald Board erreichbar)

- **Stand Samstag, 12.09. (Workshop-Ende):** Prototyp "Perspective Compass" fertig und live (Standard- vs. diversity-aware Feed-Ranking, echte Accounts, Likes/Kommentare, Vielfalts-Score, politische Einordnung als zweite Achse, read-only Fediverse-Vorschau). Finaler Blogpost, 1-Minuten-Pitch und Marktstand am 10.09. bei der Innovation Fair durchgeführt.
- **Offene Punkte vor Abreise:** Produktname/Logo final entscheiden ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)/[#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96)), Rollen festlegen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99)), Retrospektive ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98)), Supabase-Token widerrufen ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92)).

*Hinweis: Falls `board-sync.sh` auf der VM seit 07.09. zuverlässig lief, könnte die Karte bereits aktueller sein als hier angenommen (z. B. mit den Updates vom 10./11.09.) – vor dem Reinkopieren mit dem tatsächlichen Board-Stand abgleichen, nicht blind überschreiben.*

## Was noch fehlt

- [ ] **Supabase-Token widerrufen** ([#92](https://github.com/47Felix/RasberryPI-Team-13/issues/92)) – sicherheitsrelevant, unabhängig vom Workshop-Ende
- [ ] Produktname final entscheiden ([#93](https://github.com/47Felix/RasberryPI-Team-13/issues/93)), Logo gestalten ([#96](https://github.com/47Felix/RasberryPI-Team-13/issues/96))
- [ ] Rollen (Scrum Master/Product Owner) festlegen ([#99](https://github.com/47Felix/RasberryPI-Team-13/issues/99))
- [ ] Retrospektive durchführen ([#98](https://github.com/47Felix/RasberryPI-Team-13/issues/98))
- [ ] Donnerstag (03.09.) rückwirkend dokumentieren ([#97](https://github.com/47Felix/RasberryPI-Team-13/issues/97))
- [ ] Team-Zusammensetzung (Anton) vor Blogpost-Veröffentlichung final klären, falls noch offen
- [ ] Team-13-Karte auf dem Gruppenboard aktualisieren (heute Nacht nicht möglich, s.o.)
- [ ] Klären, ob `board-sync.sh` auf der VM tatsächlich zuverlässig lief (Widerspruch zwischen Issue [#100](https://github.com/47Felix/RasberryPI-Team-13/issues/100) "repariert" und dem wiederholten Fehlschlag aus dieser Cloud-Sandbox, zuletzt auch heute Nacht bestätigt)
- [ ] Entscheiden, ob die nächtliche DTEW-Automation nach dem 12.09. noch gebraucht wird bzw. deaktiviert werden sollte
- [ ] Übrige offene Punkte siehe [Kanban-Board](https://47felix.github.io/RasberryPI-Team-13/DTEW-Workshop/kanban-board/) bzw. [Issues #92–#102](https://github.com/47Felix/RasberryPI-Team-13/issues?q=is%3Aissue+92..102+in%3Anumber)

## Verwandte Notizen
- [[DTEW Hamburg - Übersicht]]
- [[DTEW 0910 - Finaler Blogpost, Pitch-Skript und Innovation Fair]]
- [[DTEW 0909 - Stand-Vorbereitung, Blogpost und Website-Eintrag]]
- [[DTEW - Strategie-Praesentation]]
- [[Team 13 - Digitale Demokratie]]
- [`Code/feed-diversity-prototype/README.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/README.md)
- [[Feed-Diversity-Prototyp - Deployment]]
- [[TaskCards Board]] – Board-Zugriff & technische Einschränkungen (weiterhin bestätigt bis zur letzten Workshop-Nacht)
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie
