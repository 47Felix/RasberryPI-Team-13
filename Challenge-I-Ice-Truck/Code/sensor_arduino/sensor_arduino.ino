/*
  sensor_arduino.ino

  Hardware-Update 4 (17.09.2026): reale Verkabelung ist wieder ZWEI
  Arduinos. Dieses Board (0x08) traegt nur noch das KY-028-Temperatur-
  modul - kein DHT11/DHT22, kein Fotowiderstand, kein Tuerkontakt mehr
  hier (die DHT22-Seite ist jetzt auf ../actor_arduino/actor_arduino.ino,
  zusammen mit den Aktoren).

  KY-028: NTC-Thermistor-Modul mit LM393-Komparator. Hat einen Analog-
  ausgang (AO, Spannungsteiler ueber den Thermistor - je waermer, desto
  hoeher/niedriger die Spannung je nach Verschaltung) und einen Digital-
  ausgang (DO, Schwellwert per Onboard-Poti, hier nicht verwendet). Fuer
  "LED-Helligkeit proportional zur Temperatur" brauchen wir den
  kontinuierlichen Analogwert, nicht den Schwellwert-Digitalausgang.

  Pins:
    - A0: KY-028 AO (Analogausgang)
    - D9 (PWM): LED, Helligkeit proportional zum KY-028-Analogwert
    - A4 (SDA) / A5 (SCL): I2C zum Pi

  I2C: Slave-Adresse 0x08, sendet auf Anfrage 2 Bytes:
    [0] KY-028-Analogwert high byte
    [1] KY-028-Analogwert low byte

  UNGETESTET auf echter Hardware - Pin-Zuordnung (A0 fuer AO, D9 fuer die
  LED) uebernimmt die Werte aus der vorherigen Version dieses Sketches,
  bei Abweichung von der tatsaechlichen Verkabelung bitte Konstanten unten
  anpassen. Ob der KY-028-Analogwert bei euch mit steigender Temperatur
  steigt oder faellt, haengt von der Verschaltung des Spannungsteilers ab -
  vor dem Kalibrieren mit einem zweiten Thermometer gegenpruefen, ggf.
  map() unten umdrehen.
*/

#include <Wire.h>

const uint8_t I2C_SLAVE_ADDRESS = 0x08;

const uint8_t PIN_KY028_ANALOG = A0;
const uint8_t PIN_LED_KY028 = 9;

const unsigned long SENSOR_UPDATE_INTERVAL_MS = 200;

volatile int16_t latestKy028Raw = 0;
unsigned long lastSensorUpdate = 0;

void setup() {
  pinMode(PIN_LED_KY028, OUTPUT);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(sendSensorDataToPi);

  Serial.begin(9600);
  Serial.println("sensor_arduino ready, I2C slave 0x08 (KY-028)");
}

void loop() {
  unsigned long now = millis();
  if (now - lastSensorUpdate < SENSOR_UPDATE_INTERVAL_MS) {
    return;
  }
  lastSensorUpdate = now;

  latestKy028Raw = analogRead(PIN_KY028_ANALOG);

  uint8_t brightness = map(latestKy028Raw, 0, 1023, 0, 255);
  analogWrite(PIN_LED_KY028, brightness);
}

void sendSensorDataToPi() {
  Wire.write(highByte(latestKy028Raw));
  Wire.write(lowByte(latestKy028Raw));
}
