---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- _class: lead -->

# 🔐 Digitaler Tresor
### Team 13 – WS-Kurzprojekt "Thank god it's (NOT) Friday"

Freitag, 28.08.2026 · Smart Systems (BH4ab)

---

## Unsere Idee: 🔐 Digitaler Tresor / Escape-Box

- 4×4-Keypad zur Code-Eingabe
- Servo als Schließmechanismus
- LCD1602-Statusanzeige
- Buzzer + LEDs für Feedback und Alarm bei Fehlversuchen
- **Show-Moment:** Publikum darf am Ende live versuchen, den Code zu knacken

---

## Hardware

Elegoo-UNO-R3-Starter-Kit:

| Bauteil | Funktion |
|---|---|
| Arduino Uno R3 | Steuerung |
| 4×4 Matrix-Keypad | Code-Eingabe |
| SG90 Micro-Servo | Schloss auf/zu |
| LCD1602 + Poti | Statusanzeige |
| Buzzer + 2 LEDs (grün/rot) | Akustik/Optik-Feedback, Alarm |
| Breadboard | Verkabelung |

---

## Architektur

```
Arduino (Tresor-Sketch)
   │  Serial: EVENT:GRANTED / DENIED:<n> / ALARM
   ▼
Raspberry Pi – Dashboard (Flask)
   ├─ SQLite-Log (jedes Ereignis mit Zeitstempel)
   ├─ Web-Dashboard: Live-Ampel + Verlauf
   ├─ Admin-Formular: Tresor-Code per Web ändern
   └─ Discord-Bot: postet automatisch bei Alarm 🚨
```

Nicht nur ein Tresor – ein **vernetztes System** mit Live-Monitoring.

---

## Erweiterung: Pi-Dashboard

Über den Grund-Tresor hinaus gebaut:

- 🟢/🟡/🔴 **Live-Ampel** (offen / verschlossen / Alarm) + Versuchszähler
- 📜 **Verlauf** aller Ereignisse mit Zeitstempel (SQLite)
- 🔑 **Web-Formular**, um den Tresor-Code zu ändern (eigenes Admin-Passwort, getrennt vom Tresor-Code)
- 💬 **Discord-Alarm**: bei zu vielen Fehlversuchen postet unser Bot automatisch im Team-Server

Erreichbar im WLAN unter `http://team13-1.local:5000`

---

## Herausforderungen & Lessons Learned

- Tinkercad-Simulation half beim Vorab-Testen der Schaltung – erste Serial-Debugging-Versuche liefen dort ins Leere (Pin-Belegung)
- Parallel an Arduino-Sketch UND Pi-Dashboard gearbeitet – Software komplett getestet, bevor überhaupt ein echter Arduino am Pi hing (virtueller Serial-Port als "Fake-Arduino")
- Dabei einen echten Bug gefunden: Discord-Nachrichten wurden zunächst geblockt (falscher User-Agent) – gefixt und verifiziert

---

<!-- _class: lead -->

## 🎤 Live-Demo

1. Tresor mit korrektem Code öffnen
2. Falschen Code eingeben → Alarm nach 3 Versuchen, Discord-Nachricht live mitverfolgen
3. Dashboard im Browser zeigen
4. **Publikum ist dran:** Wer knackt den Code zuerst?

---

<!-- _class: lead -->

# Danke! 🎉

Fragen?
