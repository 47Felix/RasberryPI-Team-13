# Fragen & Antworten – Vorbereitung für die Präsentation

Nur für euch zur Vorbereitung, kein Teil der eigentlichen Folien. Sortiert nach Themenblock, damit ihr schnell die passende Antwort findet.

---

## Zur Idee

**Warum ein digitaler Tresor?**
Weil sich damit alle Kit-Bauteile (Keypad, Servo, LCD, Buzzer, LEDs) sinnvoll in einem Gerät kombinieren lassen, es einen klaren Show-Moment hat (Publikum darf knacken) und sich gut in unabhängige Arbeitspakete aufteilen lässt.

**Was passiert, wenn das Publikum den Code wirklich knackt?**
Der Tresor öffnet sich ganz normal – genau das ist der Gag. Der Code lässt sich danach jederzeit über das Web-Dashboard ändern.

**Wie lang ist der Code, kann man ihn einfach durchprobieren?**
4-8 Ziffern (aktuell 4-stellig als Standard). Bei 4 Ziffern gibt's 10.000 Kombinationen, aber nach 3 Fehlversuchen löst der Alarm aus – "einfach durchprobieren" fällt schnell auf.

---

## Zur Hardware

**Warum das Elegoo-UNO-R3-Kit?**
Weil es das Kit war, das im Workshop zur Verfügung stand, und es alle nötigen Bauteile (Keypad, Servo, LCD, Buzzer, LEDs) direkt mitbringt.

**Warum kein Buzzer im aktuellen Sketch, wenn er doch im Kit ist?**
Pin D11 ist dafür bereits reserviert, die Integration war zeitlich die letzte Priorität – Fokus lag zuerst auf Keypad, Servo, LCD und der Pi-Anbindung.

**Wo ist das Gehäuse?**
Bewusst weggelassen – die Challenge ist benotungsfrei, wir haben die Zeit lieber in Funktion und die Pi-Dashboard-Erweiterung gesteckt statt in Optik.

---

## Zum Code / zur Technik

**Wie wird geprüft, ob der Code richtig ist?**
Der Arduino vergleicht die eingegebene Zeichenkette direkt mit dem gespeicherten Code (`String`-Vergleich). Bei Übereinstimmung öffnet der Servo, bei Falscheingabe zählt ein Fehlversuchs-Zähler hoch.

**Was passiert nach 3 Fehlversuchen genau?**
Der Alarm-Modus läuft: LCD zeigt "!! ALARM !!", die rote LED blinkt 10x, und wenn der Pi angeschlossen ist, kommt zusätzlich automatisch eine Discord-Nachricht im Team-Server an.

**Ist der Code irgendwo fest im Code (Sketch) hinterlegt – ist das nicht unsicher?**
Ja, initial ist ein Standardcode im Sketch hinterlegt. Über das Pi-Dashboard lässt er sich aber jederzeit ändern, ohne den Sketch neu zu flashen (per Serial-Kommando vom Pi an den Arduino).

**Wie kommunizieren Arduino und Pi?**
Über die USB-Serial-Verbindung (9600 Baud). Der Arduino sendet strukturierte Textzeilen wie `EVENT:GRANTED` oder `EVENT:DENIED:2`, der Pi liest die und reagiert entsprechend.

---

## Zur Pi-Dashboard-Erweiterung

**Warum überhaupt ein Dashboard, reicht der Tresor nicht allein?**
Der Tresor allein hätte nur lokal am Gerät funktioniert. Mit dem Dashboard kann man von jedem Gerät im WLAN den Status live sehen, den Verlauf nachvollziehen und den Code ändern – näher an einem "echten" IoT-Projekt.

**Was speichert ihr genau, und wo?**
Jedes Ereignis (Tür geöffnet, Fehlversuch, Alarm) mit Zeitstempel in einer SQLite-Datenbank auf dem Pi. Kein Ton, kein Bild, keine personenbezogenen Daten.

**Wie ist das Admin-Passwort fürs Dashboard abgesichert – ist das dasselbe wie der Tresor-Code?**
Nein, bewusst getrennt: Ein eigenes, zufällig generiertes Admin-Passwort schützt die `/admin`-Seite. Wer das Dashboard bedienen darf, kennt dadurch nicht automatisch den Tresor-Code.

**Was passiert, wenn der Pi oder das WLAN ausfällt?**
Der Tresor selbst funktioniert komplett unabhängig vom Pi (Arduino braucht den Pi nicht, um zu öffnen/schließen). Nur Logging, Dashboard und Discord-Alarm würden dann ausfallen.

**Wie habt ihr das getestet, wenn ihr keinen Arduino zur Hand hattet?**
Mit einem virtuellen seriellen Port (über das Linux-Tool `socat`), der einen echten Arduino simuliert hat. Damit ließ sich die komplette Pi-Software (Logging, Dashboard, Code-ändern, Discord-Alarm) durchtesten, ohne dass Hardware angeschlossen war.

---

## Zum Vorgehen / Team

**Wie habt ihr euch die Arbeit aufgeteilt?**
In unabhängige Arduino-Teilmodule, die parallel entwickelt und am Ende in einem gemeinsamen Sketch zusammengeführt wurden.

**Was war die größte Herausforderung?**
Die parallele Entwicklung an Sketch und Dashboard, ohne dass beide Seiten sich gegenseitig blockiert haben – gelöst, indem die Pi-Software komplett unabhängig vom echten Arduino getestet wurde.

**Was würdet ihr mit mehr Zeit noch machen?**
Buzzer-Integration fertigstellen, echten Hardware-Test mit dem Dashboard durchführen, ggf. eine physische LED-Ampel statt nur der Web-Anzeige.

---

## Falls kritisch nachgefragt wird

**Ist das Dashboard von außerhalb des Schul-WLANs erreichbar?**
Nur über eine zusätzlich eingerichtete VPN-Verbindung (Tailscale) für die Entwicklung/Fernwartung – im Normalbetrieb ist es nur im lokalen WLAN erreichbar.

**Habt ihr Sicherheitslücken gefunden?**
Ja, ehrlich gesagt: Beim Einrichten ist aufgefallen, dass das bestehende Web-Terminal auf dem Pi keine eigene Anmeldung hatte. Das haben wir dokumentiert und als offenen Punkt vermerkt – für ein Schulprojekt mit begrenztem Netzwerkradius akzeptabel, aber nicht ideal.
