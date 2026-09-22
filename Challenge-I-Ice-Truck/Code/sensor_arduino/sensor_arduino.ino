#include <Wire.h>

const uint8_t I2C_SLAVE_ADDRESS = 0x08;

const uint8_t PIN_KY028_ANALOG = A0;
const uint8_t PIN_LED_KY028 = 9;

const int RAW_AT_LED_FULL = 160;
const int RAW_AT_LED_OFF = 457;

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

  uint8_t brightness = constrain(map(latestKy028Raw, RAW_AT_LED_FULL, RAW_AT_LED_OFF, 255, 0), 0, 255);
  analogWrite(PIN_LED_KY028, brightness);
}

void sendSensorDataToPi() {
  Wire.write(highByte(latestKy028Raw));
  Wire.write(lowByte(latestKy028Raw));
}
