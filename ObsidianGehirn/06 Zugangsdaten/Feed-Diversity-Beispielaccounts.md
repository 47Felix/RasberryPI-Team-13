---
tags: [zugangsdaten, feed-diversity-prototyp]
---

# Feed-Diversity-Beispielaccounts – Übersicht (ohne Zugangsdaten)

> [!warning] Keine Zugangsdaten in dieser Notiz
> Diese Notiz listet nur Namen und Zweck der Beispiel-Accounts für den
> Feed-Diversity-Prototyp. E-Mail-Adressen und Passwörter stehen ausschließlich
> in einer lokalen, nicht committeten `.env` auf der Zielumgebung, siehe
> [[⚠️ Zugangsdaten - Hinweis]]. Diese Regel gilt ausnahmslos, auch für einen
> Prototyp-Datensatz.

## Zweck

`Code/feed-diversity-prototype/seed_demo_accounts.py` legt diese Accounts über
Supabase Auth an, damit eine Vorführung sofort zeigt, wie der Standard-Feed
(`ranking.dominant_perspective()`/`dominant_political_label()`) sich anhand der
Like-Historie eines Accounts in eine Richtung verzerrt. Details/Ausführung
siehe README des Prototyps, Abschnitt "Beispiel-Accounts für den Standard-Algorithmus".

## Accounts

| Rolle | Anzeigename | Like-Verhalten (bewusst einseitig) |
|---|---|---|
| Demo-Account A | Nora Bergmann | konsequent "contra" + "left" |
| Demo-Account B | Jonas Kessler | konsequent "pro" + "right" |
| Demo-Account C | Lea Vogt | konsequent "contra" + "left" |
| Demo-Account D | Tarek Aydin | konsequent "pro" + "right" |
| Admin | Team 13 Admin | veröffentlicht die Seed-Posts, selbst ohne Like-Historie |

## Stand (09.09.2026, Nacht-Session)

Skript ist geschrieben und lokal gegen einen fehlenden Supabase-Zugriff
geprüft (bricht sauber ab, keine Dummy-Werte). **Noch nicht ausgeführt** –
dieser Automations-Lauf hatte keine `SUPABASE_URL`/`SUPABASE_SECRET_KEY`/
`SUPABASE_PUBLISHABLE_KEY` als Umgebungsvariable zur Verfügung. Jemand mit
Zugriff auf die echten Supabase-Zugangsdaten muss die `DEMO_*_EMAIL`/`_PASSWORD`-
Variablen in einer lokalen `.env` ergänzen und das Skript einmal laufen lassen,
siehe `Code/feed-diversity-prototype/NIGHTLY_TASK.md`.

Seit dieser Session sind App/Datensatz komplett auf Englisch umgestellt
(Team-Entscheidung vom 09.09., siehe NIGHTLY_TASK.md) – die politische
Selbstauskunft heißt jetzt `left`/`center`/`right` statt `links`/`mitte`/`rechts`,
die Themen-Keys sind Englisch (`climate`, `transport`, usw.). Diese Notiz bleibt
bewusst auf Deutsch (Team-interne Doku, kein Besucher-Publikum), nur die
zitierten Systemwerte in der Tabelle oben wurden auf die neuen englischen
Werte aktualisiert.

## Verwandte Notizen
- [[⚠️ Zugangsdaten - Hinweis]]
- [[Doku-Regeln]]

#zugangsdaten #feed-diversity-prototyp
