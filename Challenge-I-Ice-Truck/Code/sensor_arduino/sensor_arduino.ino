#include <Wire.h>

const uint8_t I2C_SLAVE_ADDRESS = 0x08;

const uint8_t PIN_KY028_ANALOG = A0;
const uint8_t PIN_KY028_DIGITAL = 11;
const uint8_t PIN_LED_KY028 = 9;

// Muss zu calibration.py SENSOR_BOARD_CALIBRATION passen (raw_high = warm/an,
// raw_low = Ruhewert/aus) - sonst leuchtet die LED entweder durchgehend oder
// gar nicht, weil der reale Rohwertbereich nie in Naehe der Grenzen kommt.
const int RAW_AT_LED_FULL = 137;
const int RAW_AT_LED_OFF = 170;

const unsigned long SENSOR_UPDATE_INTERVAL_MS = 200;
const unsigned long DEBUG_PRINT_INTERVAL_MS = 1000;

volatile int16_t latestKy028Raw = 0;
volatile uint8_t latestKy028Digital = 0;
unsigned long lastSensorUpdate = 0;
unsigned long lastDebugPrint = 0;

void setup() {
  pinMode(PIN_LED_KY028, OUTPUT);
  pinMode(PIN_KY028_DIGITAL, INPUT);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(sendSensorDataToPi);
  disableInternalI2CPullups();

  Serial.begin(9600);
  Serial.println("sensor_arduino ready, I2C slave 0x08 (KY-028)");
}

// Kein Levelshifter zwischen Arduino (5V) und Pi (3.3V) - externe Pull-ups
// (4,7k) haengen auf der Pi-Seite an 3,3V statt an 5V (siehe README, Pin-
// Tabelle I2C). Wire.begin() aktiviert aber standardmaessig eigene interne
// 5V-Pull-ups auf SDA/SCL (A4/A5), die den Bus sonst Richtung 5V ziehen und
// die Pi-GPIOs gefaehrden. I2C ist open-drain, daher reicht reiner Pull-up-
// Tausch ohne aktiven Levelshifter-Baustein.
void disableInternalI2CPullups() {
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  digitalWrite(A4, LOW);
  digitalWrite(A5, LOW);
}

void loop() {
  unsigned long now = millis();
  if (now - lastSensorUpdate < SENSOR_UPDATE_INTERVAL_MS) {
    return;
  }
  lastSensorUpdate = now;

  latestKy028Raw = analogRead(PIN_KY028_ANALOG);
  latestKy028Digital = digitalRead(PIN_KY028_DIGITAL);

  uint8_t brightness = constrain(map(latestKy028Raw, RAW_AT_LED_FULL, RAW_AT_LED_OFF, 255, 0), 0, 255);
  analogWrite(PIN_LED_KY028, brightness);

  if (now - lastDebugPrint >= DEBUG_PRINT_INTERVAL_MS) {
    lastDebugPrint = now;
    Serial.print("DEBUG sensor: ky028_raw=");
    Serial.print(latestKy028Raw);
    Serial.print(" ky028_digital=");
    Serial.println(latestKy028Digital);
  }
}

void sendSensorDataToPi() {
  Wire.write(highByte(latestKy028Raw));
  Wire.write(lowByte(latestKy028Raw));
  Wire.write(latestKy028Digital);
}
