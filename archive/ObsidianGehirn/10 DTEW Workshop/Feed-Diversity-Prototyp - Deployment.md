---
tags: [dtew, deployment, regeln]
---

# Feed-Diversity-Prototyp – Deployment

> [!important] Verbindliche Regel (seit 09.09.2026)
> **Jede Änderung an `Code/feed-diversity-prototype/`, die nach `main` gemerged wird, wird sofort danach live deployt** – nicht erst beim nächsten größeren Update sammeln. Der Prototyp ist eine öffentlich erreichbare Demo-Seite (DTEW Hamburg, digi&demo e.V.), die jederzeit gezeigt/verlinkt werden kann, deshalb soll `main` und der Live-Stand nie auseinanderlaufen.

## Wo läuft das

Live auf der Shared-VM `ClaudeDiscord` (Azure, siehe [[Claude Discord Bot Setup]]), nicht auf dem Pi:

- Code: `/home/team13/feed-diversity` (reine Dateikopie, kein Git-Checkout – `.env`/`venv` bleiben dadurch außerhalb vom Repo)
- Persistenter Quell-Checkout für Deploys: `/home/team13/feed-diversity-src` (Git-Clone von `main`)
- Service: systemd-Unit `feed-diversity` (Gunicorn, Port 80)

## Deploy-Befehl (nach jedem Merge)

```bash
bash /home/team13/feed-diversity-src/Code/feed-diversity-prototype/deploy/update.sh
```

Zieht `main`, rsynct den Prototyp-Ordner ins Live-Verzeichnis (lässt `.env`/`venv`/`__pycache__` unangetastet), installiert `requirements.txt` neu und startet den `feed-diversity`-Service neu. Volle Details/Erstsetup: [`Code/feed-diversity-prototype/deploy/README.md`](https://github.com/47Felix/RasberryPI-Team-13/blob/main/Code/feed-diversity-prototype/deploy/README.md).

## Für Claude

Nach jedem PR-Merge, der `Code/feed-diversity-prototype/` betrifft (egal ob Claude selbst gemerged hat oder Anton/Felix), den Deploy-Befehl oben direkt danach ausführen und kurz im Chat/Commit erwähnen, dass live deployt wurde – ohne extra nachzufragen, ob das gewünscht ist (analog zur laufenden Doku-Pflicht, siehe [[Doku-Regeln]]). Gilt nur für Merges nach `main`; auf Feature-Branches ist nichts live, da besteht kein Deploy-Bedarf.

## Verwandte Notizen
- [[Branch-Strategie]]
- [[Doku-Regeln]]
- [[Team 13 - Digitale Demokratie]]

#dtew #deployment #regeln
