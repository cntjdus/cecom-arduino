#include <Servo.h>

// MAX9814: OUT->A0, VDD->5V, GND->GND
// SG90: 신호->D9, 전원->외부 5V(+), 접지->외부 GND(-)
// Arduino GND와 외부 전원 GND는 공통 연결. 외부 +5V는 Arduino 5V에 직결하지 않음.
const int MIC_PIN = A0;
const int SERVO_PIN = 9;
const int LED_PIN = LED_BUILTIN;

// 현장에서 Serial의 LEVEL 값으로 조정할 것: 숫자는 예시일 뿐
const int SOUND_THRESHOLD = 5;
const unsigned long CONFIRM_MS = 120;  // 말 시작 후보 확인 시간
const unsigned long ALLOWED_GAP_MS = 120; // 짧은 음절 사이 무음 허용
const bool DEBUG_SOUND = false;       // 감도 보정 시 true

Servo head;
bool armed = false;
bool talking = false;
bool candidate = false;
int loudCount = 0;
unsigned long candidateStart = 0;
unsigned long lastLoudTime = 0;
unsigned long lastMove = 0;
unsigned long lastDebug = 0;
bool tilted = false;

int measurePeakToPeak() {
  int lowValue = 1023;
  int highValue = 0;
  unsigned long start = millis();
  while (millis() - start < 35) {
    int x = analogRead(MIC_PIN);
    if (x < lowValue) lowValue = x;
    if (x > highValue) highValue = x;
  }
  return highValue - lowValue;
}

void handleCommands() {
  if (!Serial.available()) return;
  String cmd = Serial.readStringUntil('\n');
  cmd.trim();
  if (cmd == "LISTEN") {
    armed = true;
    talking = false;
    candidate = false;
    loudCount = 0;
    head.write(90);
    digitalWrite(LED_PIN, LOW);
  } else if (cmd == "TALK") {
    talking = true;
    armed = false;
    candidate = false;
    lastMove = millis();
    digitalWrite(LED_PIN, HIGH);
  } else if (cmd == "STOP") {
    talking = false;
    armed = false;
    candidate = false;
    head.write(90);
    digitalWrite(LED_PIN, LOW);
  }
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  pinMode(MIC_PIN, INPUT);
  Serial.begin(115200);
  Serial.setTimeout(40);
  head.attach(SERVO_PIN);
  head.write(90);
  Serial.println("READY");
}

void loop() {
  handleCommands();
  if (talking) {
    if (millis() - lastMove >= 210) {
      tilted = !tilted;
      head.write(tilted ? 108 : 74);
      lastMove = millis();
    }
    delay(3);
    return;
  }
  if (!armed) {
    delay(8);
    return;
  }

  int level = measurePeakToPeak();
  unsigned long now = millis();
  if (DEBUG_SOUND && now - lastDebug >= 250) {
    Serial.print("LEVEL:");
    Serial.println(level);
    lastDebug = now;
  }
  if (level > SOUND_THRESHOLD) {
    if (!candidate) {
      candidate = true;
      candidateStart = now;
      loudCount = 0;
    }
    lastLoudTime = now;
    loudCount++;
  } else if (candidate && now - lastLoudTime > ALLOWED_GAP_MS) {
    candidate = false;
    loudCount = 0;
  }

  if (candidate && loudCount >= 3 && now - candidateStart >= CONFIRM_MS) {
    armed = false; // 연속 트리거 방지; PC가 LISTEN 보낼 때만 재활성화
    candidate = false;
    loudCount = 0;
    Serial.println("SPEECH");
  }
}
