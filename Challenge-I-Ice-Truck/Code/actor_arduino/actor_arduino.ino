#include <Servo.h>
#include <Wire.h>

const uint8_t I2C_SLAVE_ADDRESS = 0x09;

const uint8_t PIN_KY028_ANALOG = A0;
const uint8_t PIN_LED_KY028 = 5;
const uint8_t PIN_FAN_PWM = 4;
const uint8_t PIN_VALVE_SERVO = 6;

// Muss zu calibration.py ACTOR_BOARD_CALIBRATION passen (raw_high = warm/an,
// raw_low = Ruhewert/aus) - sonst leuchtet die LED entweder durchgehend oder
// gar nicht, weil der reale Rohwertbereich nie in Naehe der Grenzen kommt.
const int RAW_AT_LED_FULL = 177;
const int RAW_AT_LED_OFF = 214;

const unsigned long SENSOR_UPDATE_INTERVAL_MS = 200;
const unsigned long FAN_SOFT_PWM_PERIOD_MS = 20;
const unsigned long DEBUG_PRINT_INTERVAL_MS = 1000;

volatile int16_t latestKy028Raw = 0;
volatile uint8_t currentFanPwm = 0;
volatile uint8_t lastValveAngle = 0;
unsigned long lastSensorUpdate = 0;
unsigned long lastDebugPrint = 0;

Servo valveServo;

void setup() {
  pinMode(PIN_LED_KY028, OUTPUT);
  pinMode(PIN_FAN_PWM, OUTPUT);
  valveServo.attach(PIN_VALVE_SERVO);
  valveServo.write(0);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(sendKy028DataToPi);
  Wire.onReceive(applySetpointsFromPi);
  disableInternalI2CPullups();

  Serial.begin(9600);
  Serial.println("actor_arduino ready, I2C slave 0x09 (KY-028)");
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
  updateFanSoftwarePwm();

  unsigned long now = millis();
  if (now - lastSensorUpdate < SENSOR_UPDATE_INTERVAL_MS) {
    return;
  }
  lastSensorUpdate = now;

  latestKy028Raw = analogRead(PIN_KY028_ANALOG);

  uint8_t brightness = constrain(map(latestKy028Raw, RAW_AT_LED_FULL, RAW_AT_LED_OFF, 255, 0), 0, 255);
  analogWrite(PIN_LED_KY028, brightness);

  if (now - lastDebugPrint >= DEBUG_PRINT_INTERVAL_MS) {
    lastDebugPrint = now;
    bool fanPinIsOn = digitalRead(PIN_FAN_PWM) == HIGH;
    Serial.print("DEBUG actor: ky028_raw=");
    Serial.print(latestKy028Raw);
    Serial.print(" fan_pwm_setpoint=");
    Serial.print(currentFanPwm);
    Serial.print(" fan_should_run=");
    Serial.print(currentFanPwm > 0 ? "yes" : "no");
    Serial.print(" fan_pin_now=");
    Serial.print(fanPinIsOn ? "ON(HIGH)" : "OFF(LOW)");
    Serial.print(" valve_angle=");
    Serial.println(lastValveAngle);
  }
}

void updateFanSoftwarePwm() {
  unsigned long cyclePosMs = millis() % FAN_SOFT_PWM_PERIOD_MS;
  unsigned long onTimeMs = (unsigned long)currentFanPwm * FAN_SOFT_PWM_PERIOD_MS / 255;
  digitalWrite(PIN_FAN_PWM, cyclePosMs < onTimeMs ? HIGH : LOW);
}

void sendKy028DataToPi() {
  Wire.write(highByte(latestKy028Raw));
  Wire.write(lowByte(latestKy028Raw));
}

void applySetpointsFromPi(int numBytes) {
  if (numBytes < 2) {
    while (Wire.available()) {
      Wire.read();
    }
    return;
  }

  uint8_t fanPwm = Wire.read();
  int rawValveAngle = Wire.read();
  uint8_t valveAngle = constrain(rawValveAngle, 0, 180);

  currentFanPwm = fanPwm;
  lastValveAngle = valveAngle;
  valveServo.write(valveAngle);
}
