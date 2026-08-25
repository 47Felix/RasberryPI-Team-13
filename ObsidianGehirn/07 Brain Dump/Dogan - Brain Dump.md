---
tags: [braindump, dogan]
---

# Dogan – Brain Dump

Formlose Notizen, Ergebnisse und Gedanken von Dogan. Neuester Eintrag oben, einfach mit Datum anfangen.

> [!tip]
> Kein Format-Zwang – Stichpunkte, Fragen, Code-Schnipsel, Ideen, was heute beim Arbeiten passiert ist. Siehe [[🧠 Brain Dump - Übersicht]] für den Sinn dahinter.

## 25.08.2026 – Arduino + Elegoo-Kit: Temperatursensor (Issue #3)

**Aufbau:** DHT11-Temperatur-/Feuchtigkeitsmodul (3-Pin-Breakout, Elegoo-Starterkit) auf einem Breadboard, verkabelt mit einem Elegoo-UNO-R3 (Arduino-Uno-Klon). Drei Jumper-Kabel vom Modul zum Arduino: `-`/GND → **GND**-Pin, `+`/VCC → **5V**-Pin (nicht VIN!), `out`/Signal → **Digitalpin 2**.

**Sketch (Arduino IDE):**
```cpp
#include <DHT.h>

#define DHTPIN 2      // Pin, an dem "out"/"S" hängt
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000); // DHT11 braucht mind. 1-2s Pause zwischen Messungen

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("Fehler beim Auslesen vom DHT-Sensor!");
    return;
  }

  Serial.print("Luftfeuchtigkeit: ");
  Serial.print(h);
  Serial.print(" %  |  Temperatur: ");
  Serial.print(t);
  Serial.println(" °C");
}
```
Library: „DHT sensor library" (Adafruit) + Abhängigkeit „Adafruit Unified Sensor", über den Bibliotheksverwalter installiert.

**Status:** Sensor antwortet (keine Fehlermeldung mehr), Messwerte aktuell aber noch unplausibel (Temperatur ~2°C, Feuchtigkeit steigt gleichmäßig um 0,10 %/Messung) – vermutlich lockerer Kontakt an Sensor/Steckbrett. Noch nicht final gelöst, als nächstes: Verkabelung fest nachdrücken und Arduino neu starten.

## 24.08.2026

-

## Verwandte Notizen
- [[🧠 Brain Dump - Übersicht]]

#braindump #dogan
