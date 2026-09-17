/*
  actor_arduino.ino

  Challenge I Track D + E, plus Klima-Sensorik (2-Board-Aufbau, siehe
  README "Hardware-Update 4"):
  - Track D: Luefter (PWM ueber Transistor) fuer einfache Kuehlanforderungen,
    Ventil (Servo) fuer hoehere Anforderungen (Durchfluss = Oeffnungswinkel)
  - Track E: I2C-Slave, empfaengt Soll-Werte vom Pi statt lokal zu
    entscheiden - die eigentliche Regellogik sitzt im Pi-Backend (Track F,
    siehe Challenge-I-Ice-Truck/Code/pi-backend/rules.py), dieser Sketch
    setzt nur um, was er per I2C bekommt
  - Zusaetzlich: DHT22 (Temp/Feuchte) haengt physisch an diesem Board, nicht
    am Sensor-Board - der Pi liest die Werte per I2C ab (Wire.onRequest),
    damit sie in die SQLite-DB kommen und die Kuehlstufen-Entscheidung
    speisen.

  Pins:
    - D2: DHT22-Signal (Temp/Feuchte)
    - D5 (PWM): LED, Helligkeit proportional zur Temperatur (Track B)
    - D9 (PWM): Transistor-Basis fuer den Luefter
    - D6: Servo-Signal fuer das Ventil (Winkel = Oeffnungsgrad, 0-180)

  I2C: Slave-Adresse 0x09, zwei Richtungen:
    - Wire.onRequest(sendClimateDataToPi): 4 Bytes, Temperatur (int16,
      Zehntelgrad) + Feuchte (int16, Zehntelprozent)
    - Wire.onReceive(applySetpointsFromPi): erwartet genau 2 Bytes,
      [0] Luefterstufe 0-255 (direkt als PWM-Duty-Cycle)
      [1] Ventil-Winkel 0-180 (Grad)

  UNGETESTET auf echter Hardware (siehe README) - Transistor/H-Bruecken-
  Verkabelung und Servo-Anschluss sind nicht in dieser Sandbox pruefbar.
*/

#include <DHT.h>
#include <Servo.h>
#include <Wire.h>

const uint8_t I2C_SLAVE_ADDRESS = 0x09;

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const uint8_t PIN_LED_DHT22 = 5;
const uint8_t PIN_FAN_PWM = 9;
const uint8_t PIN_VALVE_SERVO = 6;

// DHT22 braucht laut Datenblatt mind. 2s Pause zwischen Messungen.
const unsigned long DHT_READ_INTERVAL_MS = 2000;
unsigned long lastDhtRead = 0;

// LED-Helligkeit skaliert auf diesen Temperaturbereich (Platzhalter, siehe
// rules.py FAN_ON_TEMP_C/VALVE_ON_TEMP_C fuer die tatsaechliche Regellogik -
// die LED hier ist nur eine Anzeige, keine Steuerung).
const float LED_TEMP_MIN_C = 0.0;
const float LED_TEMP_MAX_C = 40.0;

float latestTemperatureC = NAN;
float latestHumidityPct = NAN;

Servo valveServo;

void setup() {
  dht.begin();

  pinMode(PIN_LED_DHT22, OUTPUT);
  pinMode(PIN_FAN_PWM, OUTPUT);
  valveServo.attach(PIN_VALVE_SERVO);
  valveServo.write(0);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(sendClimateDataToPi);
  Wire.onReceive(applySetpointsFromPi);

  Serial.begin(9600);
  Serial.println("actor_arduino ready, I2C slave 0x09");
}

void loop() {
  if (millis() - lastDhtRead >= DHT_READ_INTERVAL_MS) {
    lastDhtRead = millis();
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (!isnan(h) && !isnan(t)) {
      latestHumidityPct = h;
      latestTemperatureC = t;
    }
    // Bei NAN (Lesefehler): letzten gueltigen Wert behalten statt auf 0
    // zu springen - ein einzelner Ausreisser soll die Anzeige/den Pi nicht
    // mit einem falschen Wert fuettern.

    if (!isnan(latestTemperatureC)) {
      float clamped = constrain(latestTemperatureC, LED_TEMP_MIN_C, LED_TEMP_MAX_C);
      uint8_t brightness = map((long)(clamped * 10), (long)(LED_TEMP_MIN_C * 10),
                                (long)(LED_TEMP_MAX_C * 10), 0, 255);
      analogWrite(PIN_LED_DHT22, brightness);
    }
  }

  // Aktorik selbst haelt keinen Zustand ausser den zuletzt per I2C
  // gesetzten Werten (applySetpointsFromPi), bleiben bestehen bis der Pi
  // neue schickt.
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

void sendClimateDataToPi() {
  int16_t tempTenths = isnan(latestTemperatureC) ? -1 : (int16_t)(latestTemperatureC * 10);
  int16_t humTenths = isnan(latestHumidityPct) ? -1 : (int16_t)(latestHumidityPct * 10);

  Wire.write(highByte(tempTenths));
  Wire.write(lowByte(tempTenths));
  Wire.write(highByte(humTenths));
  Wire.write(lowByte(humTenths));
}
