/*
  actor_arduino.ino

  Hardware-Update 4 (17.09.2026): reale Verkabelung ist wieder ZWEI
  Arduinos (nicht mehr das eine Board aus ice_truck_single_board.ino),
  aber mit anderer Aufteilung als der urspruengliche Zwei-Board-Entwurf:
  dieses Board (0x09) traegt beide Aktoren UND den DHT22 - das zweite
  Board (siehe ../sensor_arduino/sensor_arduino.ino, 0x08) traegt nur noch
  das KY-028-Modul. Kein Tuerkontakt/Taster mehr in diesem Aufbau.

  Rolle dieses Boards:
  - Aktoren: Luefter (DC-Motor ueber Transistor ODER H-Bruecke - fuer die
    Firmware macht das keinen Unterschied, beides wird einfach per PWM auf
    D9 angesteuert; welches Bauteil tatsaechlich bestueckt ist, aendert nur
    die Verkabelung, nicht den Sketch) und Servo (Ventil, variabler Winkel)
  - Sensor: DHT22 (Temp/Feuchte) mit eigener Helligkeits-LED - Helligkeit
    proportional zur Temperatur, wie im vorherigen Einzelboard-Sketch
    (siehe ice_truck_single_board.ino, updateIndicatorLeds())
  - I2C-Slave-Adresse 0x09: liefert auf Anfrage die DHT22-Werte, nimmt per
    Wire.onReceive() die Aktor-Sollwerte vom Pi entgegen (Kuehlstufen-Logik
    sitzt im Pi-Backend, siehe pi-backend/rules.py)

  Pins:
    - D2: DHT22-Signal (1-Wire/Bus-Protokoll)
    - D5 (PWM): LED, Helligkeit proportional zur DHT22-Temperatur
    - D9 (PWM): Transistor-/H-Bruecken-Eingang fuer den Luefter
    - D6: Servo-Signal fuer das Ventil (Winkel = Oeffnungsgrad, 0-180)
    - A4 (SDA) / A5 (SCL): I2C zum Pi

  I2C: Slave-Adresse 0x09
    - Wire.onRequest(): sendet 4 Bytes [tempTenths hi, tempTenths lo,
      humTenths hi, humTenths lo] - gleiches Format wie DHT22-Teil von
      ice_truck_single_board.ino::sendSensorDataToPi()
    - Wire.onReceive(): erwartet 2 Bytes [fan_pwm 0-255, valve_angle 0-180]
      - unveraendert gegenueber der vorherigen Version dieses Sketches

  UNGETESTET auf echter Hardware - Pin-Zuordnung ist eine Annahme (Wiederve-
  rwendung der vorherigen Fan/Servo-Pins D9/D6 aus diesem Sketch plus der
  DHT22/LED-Pins D2/D5 aus ice_truck_single_board.ino), bei Abweichung von
  der tatsaechlichen Verkabelung bitte Konstanten unten anpassen.

  Benoetigte Bibliotheken: "DHT sensor library" (Adafruit) + Abhaengigkeit
  "Adafruit Unified Sensor", "Servo" ist vorinstalliert.
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

Servo valveServo;

float latestTemperatureC = NAN;
float latestHumidityPct = NAN;
unsigned long lastDhtRead = 0;

void setup() {
  dht.begin();

  pinMode(PIN_LED_DHT22, OUTPUT);
  pinMode(PIN_FAN_PWM, OUTPUT);
  valveServo.attach(PIN_VALVE_SERVO);
  valveServo.write(0);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(sendDht22DataToPi);
  Wire.onReceive(applySetpointsFromPi);

  Serial.begin(9600);
  Serial.println("actor_arduino ready, I2C slave 0x09");
}

void loop() {
  unsigned long now = millis();

  if (now - lastDhtRead >= DHT_READ_INTERVAL_MS) {
    lastDhtRead = now;
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (!isnan(h) && !isnan(t)) {
      latestHumidityPct = h;
      latestTemperatureC = t;
    }
    // Bei NAN (Lesefehler): letzten gueltigen Wert behalten statt auf 0
    // zu springen.

    updateIndicatorLed();
  }
}

void updateIndicatorLed() {
  if (isnan(latestTemperatureC)) {
    return;
  }
  // Temperatur 0-40 Grad C auf Helligkeit gemappt (Platzhalter-Bereich,
  // gleiche Skala wie im vorherigen Einzelboard-Sketch).
  int brightness = constrain(map((long)(latestTemperatureC * 10), 0, 400, 0, 255), 0, 255);
  analogWrite(PIN_LED_DHT22, brightness);
}

void sendDht22DataToPi() {
  int16_t tempTenths = isnan(latestTemperatureC) ? -1 : (int16_t)(latestTemperatureC * 10);
  int16_t humTenths = isnan(latestHumidityPct) ? -1 : (int16_t)(latestHumidityPct * 10);

  Wire.write(highByte(tempTenths));
  Wire.write(lowByte(tempTenths));
  Wire.write(highByte(humTenths));
  Wire.write(lowByte(humTenths));
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
