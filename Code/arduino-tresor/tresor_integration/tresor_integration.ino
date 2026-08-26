#include <Keypad.h>
#include <Servo.h>
#include <LiquidCrystal.h>

// --- Keypad ---
const byte ROWS = 4;
const byte COLS = 4;
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {2, 3, 4, 5};
byte colPins[COLS] = {6, 7, 8, 9};
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// --- Servo ---
Servo lockServo;
const int servoPin = 10;
const int lockedAngle = 0;
const int unlockedAngle = 90;

// --- LEDs ---
const int greenLED = 12;
const int redLED = 13;

// --- LCD ---
LiquidCrystal lcd(A0, A1, A2, A3, A4, A5);

// --- Code-Logik ---
String correctCode = "1234";
String enteredCode = "";
int failedAttempts = 0;
const int maxAttempts = 3;

void setup() {
  lockServo.attach(servoPin);
  lockServo.write(lockedAngle);

  pinMode(greenLED, OUTPUT);
  pinMode(redLED, OUTPUT);

  lcd.begin(16, 2);
  showIdleScreen();
}

void loop() {
  char key = keypad.getKey();
  if (!key) return;

  if (key == '#') {
    checkCode();
  } else if (key == '*') {
    enteredCode = "";
    showIdleScreen();
  } else {
    enteredCode += key;
    updateInputDisplay();
  }
}

void showIdleScreen() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Code eingeben:");
}

void updateInputDisplay() {
  lcd.setCursor(0, 1);
  lcd.print("                "); // Zeile leeren
  lcd.setCursor(0, 1);
  for (unsigned int i = 0; i < enteredCode.length(); i++) lcd.print("*");
}

void checkCode() {
  if (enteredCode == correctCode) {
    accessGranted();
  } else {
    accessDenied();
  }
  enteredCode = "";
}

void accessGranted() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("ZUGANG GEWAEHRT");
  lcd.setCursor(0, 1);
  lcd.print("Tresor offen!");

  digitalWrite(greenLED, HIGH);
  lockServo.write(unlockedAngle);
  delay(4000);
  lockServo.write(lockedAngle);
  digitalWrite(greenLED, LOW);

  failedAttempts = 0;
  delay(1000);
  showIdleScreen();
}

void accessDenied() {
  failedAttempts++;

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("FALSCHER CODE");
  lcd.setCursor(0, 1);
  lcd.print("Versuch " + String(failedAttempts) + "/" + String(maxAttempts));

  digitalWrite(redLED, HIGH);
  delay(1000);
  digitalWrite(redLED, LOW);

  if (failedAttempts >= maxAttempts) alarmMode();

  delay(1000);
  showIdleScreen();
}

void alarmMode() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("!! ALARM !!");

  for (int i = 0; i < 10; i++) {
    digitalWrite(redLED, HIGH);
    delay(150);
    digitalWrite(redLED, LOW);
    delay(150);
  }

  failedAttempts = 0;
}
