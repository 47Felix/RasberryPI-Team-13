/*
  ice_truck_single_board.ino

  Challenge I, Tracks A+B+D auf EINEM Arduino Uno - das ist die tatsaechlich
  verkabelte Hardware (Stand 14.09.2026), anders als die urspruengliche
  Zwei-Arduino-Aufteilung (sensor-arduino + actor-arduino, per I2C an den
  Pi angebunden, siehe ../sensor-arduino und ../actor-arduino): dort war
  noch kein zweiter Arduino/keine I2C-Verbindung zum Pi vorhanden. Diese
  Version deckt alle drei Sensor-Formate und beide Aktoren auf einem Board
  ab, die Kuehlstufen-Entscheidung passiert lokal auf dem Arduino statt im
  Pi-Backend (rules.py) - siehe "Naechste Schritte" unten fuer den Umzug
  auf I2C, sobald der Pi angebunden wird.

  Verkabelung (siehe Team-Vorgabe, Issue #176):
    | Bauteil                          | Rolle              | Pin(s)            |
    |-----------------------------------|--------------------|--------------------|
    | DHT11 (Temp/Feuchte)              | Sensor, Bus-Protokoll (1-Wire) | Signal -> D2 |
    | Fotowiderstand (LDR)              | Sensor, analog     | ueber Spannungsteiler -> A0 |
    | Kippschalter/Taster               | Sensor, digital 1/0| -> D4              |
    | LED fuer DHT11                    | Helligkeitsanzeige | -> D5 (PWM)        |
    | LED fuer Fotowiderstand           | Helligkeitsanzeige | -> D6 (PWM)        |
    | LED fuer Schalter/Taster          | Helligkeitsanzeige | -> D11 (PWM)       |
    | Luefter (DC-Motor) ueber Transistor| Aktor             | Basis ueber 1kOhm -> D3 (PWM) |
    | Servo (Ventil)                    | Aktor              | Signal -> D9       |
    | - reserviert fuer spaeter -       | I2C zum Pi         | A4 (SDA), A5 (SCL) frei lassen |

  Taster an D4 ist ein TASTER, kein Kippschalter - haelt seinen Zustand
  nicht selbst. Deshalb als entprellter Software-Toggle umgesetzt: jeder
  Tastendruck (fallende Flanke) kehrt den gespeicherten Zustand um, statt
  den Pin direkt als Zustand zu lesen (siehe pollToggleButton()).

  Kuehlstufen-Logik (lokal, siehe computeCoolingStage()): baut auf der
  DHT11-Temperatur auf (nicht auf dem LDR - der misst Licht, nicht
  Temperatur, war im Zwei-Arduino-Entwurf nur ein analoger Platzhalter-
  Sensor ohne direkten Bezug zur Kuehlkette). Schwellwerte sind
  Platzhalter (siehe Konstanten unten), haengen an der noch offenen
  Moodle-Aufgabenstellung (Issue #167) - deshalb benannte Konstanten statt
  Magic Numbers, gleiches Prinzip wie in pi-backend/rules.py.

  I2C (A4/A5): Pins bewusst frei/unbeschaltet gelassen, noch keine
  Pi-Anbindung. Wire.begin()/Wire.onRequest() sind trotzdem schon aktiv
  (Slave-Adresse 0x08, liefert dieselben 3 Sensor-Bytes wie
  ../sensor-arduino/sensor_arduino.ino), damit Track C (Pi liest per I2C
  mit) ohne Aenderung an diesem Sketch anschliessen kann, sobald SDA/SCL
  tatsaechlich verkabelt sind. Bis dahin schadet der unbeschaltete Wire.begin()
  nicht (kein Pull-up-Traffic ohne angeschlossenen Bus).

  Naechste Schritte (sobald Pi per I2C dran ist, siehe Issue #180):
    - Kuehlstufen-Entscheidung von hier in pi-backend/rules.py verlagern
      (Wire.onReceive() statt lokaler computeCoolingStage()), damit die
      Regellogik nur noch an einer Stelle gepflegt wird
    - Bis dahin bleibt dieser Sketch eigenstaendig lauffaehig (kein Pi noetig)

  UNGETESTET auf echter Hardware ueber diese Sandbox hinaus - Verkabelung
  nach obiger Tabelle noch nicht mit echtem Multimeter/Oszilloskop
  gegengeprueft, nur gegen die Library-Signaturen kompiliert.
*/

#include <DHT.h>
#include <Servo.h>
#include <Wire.h>

#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const uint8_t PIN_LDR = A0;
const uint8_t PIN_TOGGLE_BUTTON = 4;

const uint8_t PIN_LED_DHT11 = 5;
const uint8_t PIN_LED_LDR = 6;
const uint8_t PIN_LED_BUTTON = 11;

const uint8_t PIN_FAN_PWM = 3;
const uint8_t PIN_VALVE_SERVO = 9;

const uint8_t I2C_SLAVE_ADDRESS = 0x08;

// DHT11 braucht laut Datenblatt mind. 1-2s Pause zwischen Messungen.
const unsigned long DHT_READ_INTERVAL_MS = 2000;
// LDR/LED-Update, gleiches Intervall wie im sensor-arduino-Sketch.
const unsigned long SENSOR_UPDATE_INTERVAL_MS = 200;
const unsigned long DEBOUNCE_DELAY_MS = 50;

// Kuehlstufen-Schwellwerte (Platzhalter, siehe Kommentar oben).
const float FAN_ON_TEMP_C = 8.0;    // Stufe 1: Luefter an
const float VALVE_ON_TEMP_C = 12.0; // Stufe 2: zusaetzlich Ventil (Servo) auf
const float TEMP_SPAN_C = 6.0;      // fuer die Rampe von Stufe 1 bis "voll offen"

const uint8_t MAX_FAN_PWM = 255;
const uint8_t MAX_VALVE_ANGLE = 180;

Servo valveServo;

float latestTemperatureC = NAN;
float latestHumidityPct = NAN;
int16_t latestLdrRaw = 0;
volatile uint8_t latestButtonState = 0;  // 0/1, per Taster getoggelt

unsigned long lastDhtRead = 0;
unsigned long lastSensorUpdate = 0;

int lastRawButtonReading = HIGH;  // INPUT_PULLUP: nicht gedrueckt = HIGH
int debouncedButtonState = HIGH;
unsigned long lastDebounceTime = 0;

void setup() {
  dht.begin();

  pinMode(PIN_TOGGLE_BUTTON, INPUT_PULLUP);
  pinMode(PIN_LED_DHT11, OUTPUT);
  pinMode(PIN_LED_LDR, OUTPUT);
  pinMode(PIN_LED_BUTTON, OUTPUT);
  pinMode(PIN_FAN_PWM, OUTPUT);

  valveServo.attach(PIN_VALVE_SERVO);
  valveServo.write(0);

  Wire.begin(I2C_SLAVE_ADDRESS);
  Wire.onRequest(sendSensorDataToPi);

  Serial.begin(9600);
  Serial.println("ice_truck_single_board ready, I2C slave 0x08 (SDA/SCL noch unbeschaltet)");
}

void loop() {
  // Taster jede Iteration pruefen, kein blockierendes delay() im loop().
  pollToggleButton();

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
    // zu springen - ein einzelner Ausreisser soll die Kuehlstufe nicht
    // faelschlich auf "aus" zuruecksetzen.
  }

  if (now - lastSensorUpdate >= SENSOR_UPDATE_INTERVAL_MS) {
    lastSensorUpdate = now;

    latestLdrRaw = analogRead(PIN_LDR);

    updateIndicatorLeds();
    applyCoolingStage(computeCoolingStage(latestTemperatureC));
  }
}

void pollToggleButton() {
  int rawReading = digitalRead(PIN_TOGGLE_BUTTON);

  if (rawReading != lastRawButtonReading) {
    lastDebounceTime = millis();
  }

  if (millis() - lastDebounceTime > DEBOUNCE_DELAY_MS) {
    if (rawReading != debouncedButtonState) {
      debouncedButtonState = rawReading;

      // INPUT_PULLUP: Taste gedrueckt zieht den Pin auf LOW. Nur bei der
      // fallenden Flanke togglen, nicht beim Loslassen - sonst zaehlt ein
      // Tastendruck doppelt.
      if (debouncedButtonState == LOW) {
        latestButtonState = latestButtonState ? 0 : 1;
      }
    }
  }

  lastRawButtonReading = rawReading;
}

void updateIndicatorLeds() {
  // DHT11: Temperatur 0-40 Grad C auf Helligkeit gemappt (Platzhalter-
  // Bereich, siehe Kommentar oben zu den Schwellwerten).
  if (!isnan(latestTemperatureC)) {
    int brightness = constrain(map((long)(latestTemperatureC * 10), 0, 400, 0, 255), 0, 255);
    analogWrite(PIN_LED_DHT11, brightness);
  }

  analogWrite(PIN_LED_LDR, map(latestLdrRaw, 0, 1023, 0, 255));
  analogWrite(PIN_LED_BUTTON, latestButtonState ? 255 : 0);
}

// Kuehlstufe: 0 = aus, 1 = Luefter, 2 = Luefter + Ventil.
uint8_t computeCoolingStage(float temperatureC) {
  if (isnan(temperatureC) || temperatureC < FAN_ON_TEMP_C) {
    return 0;
  }
  if (temperatureC < VALVE_ON_TEMP_C) {
    return 1;
  }
  return 2;
}

void applyCoolingStage(uint8_t stage) {
  if (stage == 0) {
    analogWrite(PIN_FAN_PWM, 0);
    valveServo.write(0);
    return;
  }

  // Rampe innerhalb der Stufe, damit der Luefter nicht abrupt auf voll
  // springt, sobald FAN_ON_TEMP_C ueberschritten ist.
  float aboveThreshold = constrain(latestTemperatureC - FAN_ON_TEMP_C, 0.0, TEMP_SPAN_C);
  uint8_t fanPwm = (uint8_t)constrain((aboveThreshold / TEMP_SPAN_C) * MAX_FAN_PWM, 40, MAX_FAN_PWM);
  analogWrite(PIN_FAN_PWM, fanPwm);

  if (stage == 1) {
    valveServo.write(0);
    return;
  }

  float aboveValveThreshold = constrain(latestTemperatureC - VALVE_ON_TEMP_C, 0.0, TEMP_SPAN_C);
  uint8_t valveAngle = (uint8_t)constrain((aboveValveThreshold / TEMP_SPAN_C) * MAX_VALVE_ANGLE, 30, MAX_VALVE_ANGLE);
  valveServo.write(valveAngle);
}

// Gleiches Byte-Format wie ../sensor-arduino/sensor_arduino.ino, plus
// Feuchte, damit der Pi (sobald angebunden) den vollen DHT11-Messwert
// mitbekommt statt nur die Temperatur.
void sendSensorDataToPi() {
  int16_t tempTenths = isnan(latestTemperatureC) ? -1 : (int16_t)(latestTemperatureC * 10);
  int16_t humTenths = isnan(latestHumidityPct) ? -1 : (int16_t)(latestHumidityPct * 10);

  Wire.write(highByte(tempTenths));
  Wire.write(lowByte(tempTenths));
  Wire.write(highByte(humTenths));
  Wire.write(lowByte(humTenths));
  Wire.write(highByte(latestLdrRaw));
  Wire.write(lowByte(latestLdrRaw));
  Wire.write(latestButtonState);
}
