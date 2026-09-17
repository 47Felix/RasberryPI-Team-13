/*
  sensor_arduino.ino

  Challenge I Track A + B + C (Sensor-Seite):
  - Track A: liest zwei Sensor-Formate aus (analog + digital)
  - Track B: je Sensor eine PWM-LED, Helligkeit proportional zum Messwert
  - Track C: dient selbst als I2C-Slave, damit der Pi die Werte abholen kann -
    deckt damit auch das geforderte "Bus-Protokoll"-Format aus Track A ab,
    ohne einen zusaetzlichen dritten Arduino nur als I2C-Slave-Platzhalter zu
    brauchen (siehe README.md fuer die Begruendung dieser Entscheidung)

  Sensoren (siehe README "Hardware-Update 4"):
    - KY-028-Modul (Analogausgang AO) an A0 - unkalibrierter Rohwert, kein
      eigener Temperatursensor fuer die Kuehlstufen-Entscheidung (die laeuft
      ueber den DHT22 am actor_arduino, siehe pi-backend/rules.py)
    - Tuerkontakt-Kippschalter an D2 (digital, Platzhalter fuer "Kuehlraumtuer
      offen/zu" - passt inhaltlich besser zum Kuehlketten-Szenario als ein
      beliebiger Taster)

  LEDs (PWM-faehige Pins):
    - D9: Helligkeit proportional zum Analogwert (0-1023 -> 0-255)
    - D10: volle Helligkeit wenn Tuer offen, sonst aus (digitaler Sensor hat
      keine "Hoehe", nur an/aus)

  I2C: Slave-Adresse 0x08, sendet auf Anfrage 3 Bytes:
    [0] Analogwert high byte
    [1] Analogwert low byte
    [2] Digitalwert (0 oder 1)

  UNGETESTET auf echter Hardware (siehe README) - kompiliert nur lokal
  gegen die Wire-Library-Signaturen ueberprueft, keine reale Verkabelung/
  kein reales Board in dieser Sandbox verfuegbar.
*/

#include <Wire.h>

const uint8_t I2C_SLAVE_ADDRESS = 0x08;

const uint8_t PIN_ANALOG_SENSOR = A0;
const uint8_t PIN_DOOR_SWITCH = 2;
const uint8_t PIN_LED_ANALOG = 9;
const uint8_t PIN_LED_DOOR = 10;

volatile int16_t latestAnalogValue = 0;
volatile uint8_t latestDoorState = 0;

void setup() {
  pinMode(PIN_DOOR_SWITCH, INPUT_PULLUP);
  pinMode(PIN_LED_ANALOG, OUTPUT);
  pinMode(PIN_LED_DOOR, OUTPUT);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(sendSensorDataToPi);

  Serial.begin(9600);
  Serial.println("sensor_arduino ready, I2C slave 0x08");
}

void loop() {
  latestAnalogValue = analogRead(PIN_ANALOG_SENSOR);
  // INPUT_PULLUP: Schalter geschlossen (Tuer zu) zieht den Pin auf LOW
  latestDoorState = (digitalRead(PIN_DOOR_SWITCH) == LOW) ? 0 : 1;

  uint8_t analogBrightness = map(latestAnalogValue, 0, 1023, 0, 255);
  analogWrite(PIN_LED_ANALOG, analogBrightness);
  analogWrite(PIN_LED_DOOR, latestDoorState ? 255 : 0);

  delay(200);
}

void sendSensorDataToPi() {
  Wire.write(highByte(latestAnalogValue));
  Wire.write(lowByte(latestAnalogValue));
  Wire.write(latestDoorState);
}
