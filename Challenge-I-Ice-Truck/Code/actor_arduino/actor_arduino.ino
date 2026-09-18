/*
  actor_arduino.ino

  Hardware-Update 5 (17.09.2026): DHT22 auf diesem Board hat nie eine
  gueltige Messung geliefert (dht.readHumidity()/readTemperature() gaben
  ab dem ersten Aufruf durchgehend NaN zurueck, per Serial verifiziert -
  Wiring wurde mehrfach gegengeprueft). Team hat den DHT22 durch ein
  zweites KY-028-Modul ersetzt - dieses Board hat jetzt also GENAU DAS
  GLEICHE Sensorprinzip wie ../sensor_arduino/sensor_arduino.ino (KY-028,
  unkalibrierter Analogwert), zusaetzlich weiterhin die Aktoren.

  Rolle dieses Boards:
  - Sensor: KY-028 (Analogausgang AO), gleiches Prinzip wie sensor_arduino
  - Aktoren: Luefter (PWM auf D3) und Servo (Ventil, D6)
  - I2C-Slave-Adresse 0x09: liefert auf Anfrage den KY-028-Rohwert (2
    Bytes, gleiches Format wie sensor_arduino.ino), nimmt per
    Wire.onReceive() die Aktor-Sollwerte vom Pi entgegen (Kuehlstufen-Logik
    sitzt im Pi-Backend, siehe pi-backend/rules.py + pi-backend/calibration.py)

  Kalibrierung (2026-09-17, per Referenzthermometer, siehe auch
  pi-backend/calibration.py::ACTOR_BOARD_CALIBRATION): Rohwert faellt mit
  steigender Temperatur (23.0C -> 16.5, 30.0C -> 12.5, hier auf Ganzzahlen
  gerundet). LED soll bei 30C und waermer voll hell sein, bei -10C und
  kaelter aus, dazwischen linear - RAW_AT_LED_FULL/RAW_AT_LED_OFF unten
  sind die aus der Kalibriergeraden hochgerechneten Rohwert-Grenzen dafuer
  (-10C ist ausserhalb der gemessenen 23-30C, also extrapoliert, nicht
  gemessen).

  Pins:
    - A0: KY-028 AO (Analogausgang)
    - D5 (PWM): LED, Helligkeit proportional zum KY-028-Rohwert
    - D3 (PWM): Transistor-/H-Bruecken-Eingang fuer den Luefter (war D9,
      siehe Hardware-Update 7 in README.md)
    - D6: Servo-Signal fuer das Ventil (Winkel = Oeffnungsgrad, 0-180)
    - A4 (SDA) / A5 (SCL): I2C zum Pi

  Bug gefunden 2026-09-18 (Hardware-Update 7 in README.md): der Luefter
  drehte trotz korrekter I2C-Sollwerte nicht richtig, weil PIN_FAN_PWM
  vorher auf D9 lag. Auf dem Arduino Uno belegt die Servo-Bibliothek fest
  Timer1 fuer ihre Pulserzeugung (Servo::attach() reicht, unabhaengig vom
  gewaehlten Pin) - Timer1 ist aber auch der Hardware-Timer hinter
  analogWrite() auf D9/D10, wodurch dort nach dem Servo-Attach kein
  sauberes PWM mehr rauskam. Fix: Luefter auf D3 (Timer2) verschoben,
  unabhaengig von Servo (Timer1) und LED auf D5 (Timer0).

  I2C: Slave-Adresse 0x09
    - Wire.onRequest(): sendet 2 Bytes [KY-028-Rohwert hi, lo] - gleiches
      Format wie sensor_arduino.ino::sendSensorDataToPi()
    - Wire.onReceive(): erwartet 2 Bytes [fan_pwm 0-255, valve_angle 0-180]
      - unveraendert gegenueber der vorherigen Version dieses Sketches

  Benoetigte Bibliotheken: "Servo" ist vorinstalliert, kein DHT/Adafruit-
  Unified-Sensor mehr noetig (DHT22 raus).
*/

#include <Servo.h>
#include <Wire.h>

const uint8_t I2C_SLAVE_ADDRESS = 0x09;

const uint8_t PIN_KY028_ANALOG = A0;
const uint8_t PIN_LED_KY028 = 5;
const uint8_t PIN_FAN_PWM = 3;
const uint8_t PIN_VALVE_SERVO = 6;

// Rohwert bei 30C (LED voll hell) bzw. -10C (LED aus), siehe Kalibrierung
// oben - Rohwert faellt mit steigender Temperatur, daher RAW_AT_LED_FULL <
// RAW_AT_LED_OFF.
const int RAW_AT_LED_FULL = 13;
const int RAW_AT_LED_OFF = 35;

const unsigned long SENSOR_UPDATE_INTERVAL_MS = 200;

volatile int16_t latestKy028Raw = 0;
unsigned long lastSensorUpdate = 0;

Servo valveServo;

void setup() {
  pinMode(PIN_LED_KY028, OUTPUT);
  pinMode(PIN_FAN_PWM, OUTPUT);
  valveServo.attach(PIN_VALVE_SERVO);
  valveServo.write(0);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(sendKy028DataToPi);
  Wire.onReceive(applySetpointsFromPi);

  Serial.begin(9600);
  Serial.println("actor_arduino ready, I2C slave 0x09 (KY-028)");
}

void loop() {
  unsigned long now = millis();
  if (now - lastSensorUpdate < SENSOR_UPDATE_INTERVAL_MS) {
    return;
  }
  lastSensorUpdate = now;

  latestKy028Raw = analogRead(PIN_KY028_ANALOG);

  uint8_t brightness = constrain(map(latestKy028Raw, RAW_AT_LED_FULL, RAW_AT_LED_OFF, 255, 0), 0, 255);
  analogWrite(PIN_LED_KY028, brightness);
}

void sendKy028DataToPi() {
  Wire.write(highByte(latestKy028Raw));
  Wire.write(lowByte(latestKy028Raw));
}

void applySetpointsFromPi(int numBytes) {
  if (numBytes < 2) {
    // Unvollstaendiges Paket - ignorieren statt mit halben Daten zu regeln
    while (Wire.available()) {
      Wire.read();
    }
    return;
  }

  uint8_t fanPwm = Wire.read();
  uint8_t valveAngle = constrain(Wire.read(), 0, 180);

  analogWrite(PIN_FAN_PWM, fanPwm);
  valveServo.write(valveAngle);
}
