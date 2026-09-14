/*
  actor_arduino.ino

  Challenge I Track D + E (Aktor-Seite):
  - Track D: Luefter (PWM ueber Transistor) fuer einfache Kuehlanforderungen,
    Ventil (Servo) fuer hoehere Anforderungen (Durchfluss = Oeffnungswinkel)
  - Track E: I2C-Slave, empfaengt Soll-Werte vom Pi statt lokal zu
    entscheiden - die eigentliche Regellogik sitzt im Pi-Backend (Track F,
    siehe Challenge-I-Ice-Truck/Code/pi-backend/rules.py), dieser Sketch
    setzt nur um, was er per I2C bekommt

  Pins:
    - D9 (PWM): Transistor-Basis fuer den Luefter (DC-Motor aus dem Kit)
    - D6: Servo-Signal fuer das Ventil (Winkel = Oeffnungsgrad, 0-180)

  I2C: Slave-Adresse 0x09, erwartet auf Wire.onReceive() genau 2 Bytes:
    [0] Luefterstufe 0-255 (direkt als PWM-Duty-Cycle)
    [1] Ventil-Winkel 0-180 (Grad)

  UNGETESTET auf echter Hardware (siehe README) - Transistor/H-Bruecken-
  Verkabelung und Servo-Anschluss sind nicht in dieser Sandbox pruefbar.
*/

#include <Wire.h>
#include <Servo.h>

const uint8_t I2C_SLAVE_ADDRESS = 0x09;

const uint8_t PIN_FAN_PWM = 9;
const uint8_t PIN_VALVE_SERVO = 6;

Servo valveServo;

void setup() {
  pinMode(PIN_FAN_PWM, OUTPUT);
  valveServo.attach(PIN_VALVE_SERVO);
  valveServo.write(0);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onReceive(applySetpointsFromPi);

  Serial.begin(9600);
  Serial.println("actor_arduino ready, I2C slave 0x09");
}

void loop() {
  // Alles Reaktionsgetriebene passiert in applySetpointsFromPi(); die
  // Actor-Seite haelt selbst keinen Zustand ausser den zuletzt gesetzten
  // Werten (bleiben bestehen, bis der Pi neue schickt).
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
