/*
  DHT11_Temperatursensor_Arduino.ino

  Liest Temperatur und Luftfeuchtigkeit vom DHT11-Sensor (Elegoo-Starterkit)
  über einen Arduino Uno aus und gibt die Werte im seriellen Monitor aus.

  Team13-1 / Smart Systems Pi-Projekt – GitHub-Issue #3

  Verkabelung (DHT11 3-Pin-Modul -> Arduino Uno):
    -  / GND      -> GND
    +  / VCC      -> 5V   (nicht VIN!)
    out / Signal  -> Digitalpin 2

  Benötigte Bibliothek (über den Arduino-IDE-Bibliotheksverwalter installieren):
    - "DHT sensor library" (Adafruit)
    - Abhängigkeit "Adafruit Unified Sensor" mitinstallieren
*/

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
