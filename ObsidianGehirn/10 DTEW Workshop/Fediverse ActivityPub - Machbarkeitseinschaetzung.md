---
tags: [dtew, workshop, digitale-demokratie, fediverse]
---

# Fediverse/ActivityPub – Machbarkeitseinschätzung (Nacht-Session 07.09.2026)

Ausgangspunkt: Felix' Brain-Dump-Eintrag vom 07.09. ([[Felix - Brain Dump]])
wünscht sich ein Forum, das zwei politische Lager im selben Feed
unterschiedliche Meinungen sehen lässt, und bittet konkret darum, Fediverse/
ActivityPub als Anbindung zu prüfen. Diese Notiz ist die ehrliche
Einschätzung dazu, im selben Stil wie die Machbarkeits-Einschätzung zu Lasses
ML-Vorschlägen vom 01.09. (siehe [[Team 13 - Digitale Demokratie]]): was ist
in der verbleibenden Zeit realistisch umsetzbar, was bleibt nur
konzeptionell skizzierbar.

## Was ActivityPub tatsächlich ist

ActivityPub ist ein W3C-Standard für dezentrale soziale Netzwerke (Mastodon,
Pleroma, Akkoma, GoToSocial u.a. bauen darauf auf). Ein vollständiger
Client/Server-Actor braucht mehrere Teile gleichzeitig:

- Einen über WebFinger auffindbaren "Actor" (eigene JSON-LD-Identität)
- HTTP Signatures (kryptographisch signierte Zustellung jeder Aktivität)
- Inbox/Outbox-Endpunkte samt Follower-/Following-Collections
- Verarbeitung des Activity-Vokabulars (Create, Follow, Like, Announce, …)
- Interop-Eigenheiten zwischen Implementierungen (Mastodon, Pleroma etc.
  weichen in Details vom reinen Standard ab)

Das ist ein Protokoll-Stack, keine einzelne API – realistisch mehrere Wochen
Aufwand für ein funktionierendes, mit echten Servern föderierendes Setup,
selbst mit vorhandenen Python-Bibliotheken als Startpunkt.

## Einschätzung: nicht machbar in der verbleibenden Zeit

Ein vollständiger ActivityPub-Server/-Actor für den Prototyp (der selbst
postet, folgbar ist, Aktivitäten empfängt und verarbeitet) ist für die
verbleibende Prototyping-Zeit **nicht** realistisch – vergleichbar mit
Lasses ML-Vorschlägen 2/3 vom 01.09., die aus demselben Grund (zu
aufwändig für zwei Wochen ohne Vorerfahrung im entsprechenden Bereich)
zurückgestellt wurden. Das gilt für Team 13 unabhängig vom fehlenden
ML-Bezug hier – es ist schlicht ein eigenständiger Protokoll-Stack, der
Zeit braucht, die für den Kern des Prototyps (Feed-Ranking) fehlen würde.

## Was stattdessen machbar und risikoarm ist

Mastodon (und kompatible Server wie Pleroma/Akkoma/GoToSocial) bieten eine
**öffentliche, unauthentifizierte REST-API** für lesenden Zugriff auf
öffentliche Inhalte, u.a.:

- `GET /api/v1/timelines/tag/{hashtag}` – öffentliche Posts zu einem Hashtag
- `GET /api/v1/timelines/public?local=true` – öffentliche lokale Timeline
- `GET /api/v1/accounts/{id}/statuses` – öffentliche Posts eines Accounts

Kein Account, kein Token, keine kryptographische Signatur nötig – reines
`GET` gegen eine Instanz wie `mastodon.social`. Wichtig für die Einordnung:
das ist die **Mastodon-REST-API**, nicht das ActivityPub-Protokoll selbst
(kein WebFinger, keine Activity-JSON-LD-Objekte, keine Signaturen) – viele
"Fediverse-Integrationen" nutzen in der Praxis genau diesen pragmatischen
Weg statt einer vollen ActivityPub-Implementierung, weil er für reines
Lesen ausreicht und den Protokoll-Stack oben komplett umgeht.

**Umgesetzt in dieser Nacht-Session:** `Code/feed-diversity-prototype/fediverse.py`
holt öffentliche Mastodon-Posts zu einem pro Thema hinterlegten Hashtag
(z.B. Klima-Themen -> `#klimapolitik`) und zeigt sie im Feed als eigenen,
deutlich als extern gekennzeichneten Abschnitt ("aus dem Fediverse, nur
lesend") – als zusätzliche Perspektivquelle außerhalb der eigenen
Supabase-Posts, wie in der Aufgabenliste vorgeschlagen. Fällt die Anfrage
aus (Instanz nicht erreichbar, Rate-Limit, Netzwerkfehler), zeigt der
Abschnitt einen leeren Zustand statt eines Fehlers – dasselbe Fail-Open-
Verhalten wie `db.py` bei einem nicht erreichbaren Supabase.

> [!warning] Nicht live getestet
> Die Cloud-Sandbox dieser Session erlaubt nur ausgehende Verbindungen zu
> einer festen Allowlist von Domains (Paketregistries, Anthropic-APIs) – ein
> Testaufruf gegen `mastodon.social` wurde vom sandboxeigenen Proxy mit
> `403` blockiert. Der Code folgt demselben defensiven Muster wie die
> bestehende Supabase-Anbindung (Timeout, Exception-Handling, leerer
> Zustand statt Absturz) und ist mit gemockten Requests unit-getestet, aber
> **noch nicht gegen die echte Mastodon-API verifiziert**. Muss vor dem
> Vorführen einmal in einer Umgebung mit normalem Internetzugriff (Pi/VM,
> nicht diese Sandbox) geprüft werden.

## Offene Punkte, falls weiterverfolgt

- Konkrete Instanz/Hashtag-Zuordnung pro Thema festlegen und im Team
  gegenchecken (aktuell nur ein erster Vorschlag in `fediverse.py`)
- Rate-Limits/Caching bedenken, falls die Instanz bei jedem Feed-Aufruf
  angefragt wird (aktuell: keine Caching-Schicht, jeder `/`-Aufruf fragt live an)
- Externe Fediverse-Posts haben keine eigene `political_label`/`perspective`-
  Einordnung – im UI bewusst nicht in die bestehenden Ranking-Achsen
  gepresst, sondern als eigener, klar getrennter "extern"-Block angezeigt
- Ein echter ActivityPub-Actor (eigener Prototyp-Account, der selbst postet
  und folgbar ist) bleibt reine Konzept-Skizze für eine mögliche
  Weiterführung nach dem Workshop, siehe Integrationsdiskussion vom 02.09.
  in [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]]
  (Bluesky/Mastodon als realistischer Adoptionspfad, nicht als
  Zwei-Wochen-Feature)

## Verwandte Notizen
- [[Felix - Brain Dump]]
- [[Team 13 - Digitale Demokratie]]
- [[DTEW 0209 - Kritische Punkte, Problem Statements und Ideation]]
- [[Doku-Regeln]]

#dtew #workshop #digitale-demokratie #fediverse
