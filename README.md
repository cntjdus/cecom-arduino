# 🤖 CECOM - 아두이노로 쓸데없는 물건 만들기 대회

> **아무도 물어보지 않았지만, 굳이 끼어듭니다.**

사람들이 대화를 시작하면 아무도 요청하지 않은 말을 냅다 내뱉는 AI 로봇입니다.

일반적인 AI 음성 비서는 사용자의 질문을 이해하고 도움을 제공하지만, **아무도 안 물어봇**은 정반대의 목적으로 만들어졌습니다.

사람들이 무슨 이야기를 나누는지는 중요하지 않습니다. 누군가 말을 시작하기만 하면 킹받는 말투로 대화에 끼어들어 흐름을 방해합니다.

**기술력은 있는데 쓸모는 없는, 대화 방해 전문 AI 로봇입니다.**

---

## 📌 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| 프로젝트 유형 | Arduino 기반 AI 피지컬 컴퓨팅 |
| 개발 목적 | 아두이노로 쓸데없는 물건 만들기 대회 |
| 개발 언어 | Python, C/C++ |
| 주요 기술 | Arduino, Gemini API, TTS, Serial Communication |
| 개발 환경 | VS Code, Arduino IDE |

---

## 💡 기획 배경

오늘날 AI는 사용자의 의도를 정확하게 이해하고, 유용한 답변을 제공하는 방향으로 발전하고 있습니다.

하지만 모든 AI가 반드시 도움이 되어야 할까요?

저희는 이러한 의문에서 출발하여, **사용자에게 전혀 도움이 되지 않는 AI**를 만들어 보기로 했습니다.

이 로봇은 상대방의 말을 이해하거나 적절한 답변을 제공하지 않습니다. 단순히 누군가 말을 시작했다는 사실만 감지하고, 아무도 원하지 않은 발언을 합니다.

AI 기술을 활용해 사람의 대화를 방해한다는 점에서 쓸데없지만, 바로 그 쓸데없음이 작품의 핵심입니다.

---

## ✨ 주요 기능

### 🎤 1. 주변 소리 감지

- MAX9814 마이크 센서를 통해 주변 소리를 감지합니다.
- 소리의 크기와 지속 시간을 측정하여 발화 시작 여부를 추정합니다.
- 설정된 기준값을 초과하는 소리가 일정 시간 지속되면 시스템이 작동합니다.
- 별도의 호출어나 버튼 입력 없이 자동으로 반응합니다.

### 🧠 2. AI 기반 대사 생성

- 팀원들이 직접 작성한 말투 예시를 Gemini API에 제공합니다.
- Few-shot Prompting 방식으로 원하는 캐릭터의 말투를 적용합니다.
- 훈수, 비꼼, 무지성 반박 등 다양한 유형의 대사를 생성합니다.
- 생성된 대사는 음성 합성을 위해 텍스트 파일로 관리합니다.

### 🔊 3. TTS 음성 합성

- 생성된 텍스트를 TTS(Text-to-Speech) 기술로 음성으로 변환합니다.
- 별도의 직접 녹음 없이 AI 음성을 생성할 수 있습니다.
- 음성 파일은 WAV 형식으로 저장합니다.
- 대사마다 음성을 미리 생성하여 실행 중 발생하는 지연을 줄입니다.

### 💬 4. 자동 대화 난입

- 사람이 말하기 시작한 것으로 추정되면 미리 생성된 음성 파일 중 하나를 무작위로 재생합니다.
- 상대방의 발언이 끝날 때까지 기다리지 않고 대화 도중 끼어듭니다.
- 직전에 사용한 음성이 연속으로 재생되지 않도록 처리합니다.
- 대화 내용과 관계없이 발언하는 것이 특징입니다.

### 🤖 5. 서보모터 제어

- AI 음성 출력과 동시에 SG90 서보모터가 작동합니다.
- 로봇이 말하는 동안 고개를 좌우로 움직입니다.
- 음성 출력이 종료되면 기본 위치로 복귀합니다.

### 🔄 6. 자동 반복 및 중복 감지 방지

- AI가 말하는 동안에는 마이크 감지를 일시적으로 중단합니다.
- 로봇이 자신의 음성을 감지하여 반복적으로 작동하는 현상을 방지합니다.
- 발언이 종료되면 일정 시간 대기한 후 다시 감지 상태로 전환합니다.

---

## 🛠️ 기술 스택

### Software

| 기술 | 역할 |
| --- | --- |
| Python | 전체 프로그램 제어 및 음성 재생 |
| C/C++ | Arduino 하드웨어 제어 |
| Gemini API | 말투 예시 기반 AI 대사 생성 |
| Gemini TTS | 텍스트를 음성으로 변환 |
| PySerial | Python과 Arduino 간 시리얼 통신 |
| python-dotenv | API 키 및 환경변수 관리 |
| VS Code | Python 개발 환경 |
| Arduino IDE | Arduino 코드 작성 및 업로드 |

### Hardware

| 부품 | 역할 |
| --- | --- |
| Arduino UNO R3 | 센서 입력 및 모터 제어 |
| KY-038 마이크 센서 | 주변 소리 감지 |
| SG90 서보모터 | 로봇 고개 움직임 |
| 브레드보드 | 회로 구성 |
| 점퍼선 | 부품 간 연결 |
| USB 케이블 | Arduino와 PC 연결 |
| 외부 5V 전원 | 서보모터 전원 공급 |
| PC 및 스피커 | AI 프로그램 실행 및 음성 출력 |

---

## ⚙️ 시스템 아키텍처

### 1. AI 대사 및 음성 생성

프로그램 실행 전에 Gemini API를 활용해 대사와 음성을 생성합니다.

```text
[팀원들이 작성한 말투 예시]
            │
            ▼
    style_samples.txt
            │
            ▼
       Gemini API
            │
            ▼
      새로운 대사 생성
            │
            ▼
        Gemini TTS
            │
            ▼
      WAV 음성 파일 저장
            │
            ▼
       voices/ 폴더
```

### 2. 로봇 실행 과정

```text
        [사람이 대화 시작]
                 │
                 ▼
        [MAX9814 마이크]
          주변 소리 감지
                 │
                 ▼
         [Arduino UNO]
       소리 크기 및 지속 시간 확인
                 │
                 ▼
        [SPEECH 신호 전송]
                 │
          USB Serial
                 │
                 ▼
         [Python 프로그램]
                 │
          랜덤 음성 선택
                 │
          ┌──────┴──────┐
          ▼             ▼
     [스피커 출력]   [Arduino]
          │             │
      AI 대사 재생   서보모터 작동
          │             │
          └──────┬──────┘
                 ▼
           [발언 종료]
                 │
                 ▼
        [일정 시간 대기]
                 │
                 ▼
         [감지 상태 복귀]
                 │
                 ▼
            반복 실행
```

---

## 🔌 하드웨어 회로 구성

### KY-038 마이크 센서

| KY-038 | Arduino UNO |
| --- | --- |
| VDD | 5V |
| GND | GND |
| OUT | A0 |

### SG90 서보모터

| SG90 | 연결 위치 |
| --- | --- |
| 신호선 | Arduino D9 |
| 전원선 | 외부 5V 전원 (+) |
| 접지선 | 외부 전원 GND |

Arduino GND와 외부 전원 GND는 공통으로 연결합니다.

서보모터에 별도 전원을 사용하는 경우 외부 전원의 +5V를 Arduino의 5V 핀에 무작정 직결하지 않도록 주의합니다.

### Arduino ↔ Python 시리얼 통신

| 명령어 | 방향 | 기능 |
| --- | --- | --- |
| `LISTEN` | Python → Arduino | 소리 감지 활성화 |
| `SPEECH` | Arduino → Python | 발화 시작 추정 신호 |
| `TALK` | Python → Arduino | 서보모터 동작 시작 |
| `STOP` | Python → Arduino | 서보모터 동작 종료 |

통신 속도는 `115200 baud`를 사용합니다.

---

## 📁 프로젝트 구조

```text
amudo_bot_v2/
│
├── arduino/
│   └── amudo_bot_v2/
│       └── amudo_bot_v2.ino
│
├── generate_bank.py
├── run_robot.py
├── style_samples.txt
├── requirements.txt
│
├── .env
├── .gitignore
├── README.md
│
└── voices/
    ├── 001.wav
    ├── 002.wav
    ├── 003.wav
    └── lines.txt
```

| 파일 | 설명 |
| --- | --- |
| `generate_bank.py` | Gemini API를 이용한 대사 및 음성 생성 |
| `run_robot.py` | Arduino 신호 수신 및 음성 출력 |
| `style_samples.txt` | AI 말투 예시 데이터 |
| `requirements.txt` | Python 라이브러리 목록 |
| `.env.example` | 환경변수 설정 예시 |
| `amudo_bot_v2.ino` | 아두이노 센서 및 서보모터 제어 |
| `voices/` | 생성된 WAV 음성 파일 저장 |

---

## 🚀 실행 방법

### 1. 개발 환경 준비

**필요 환경**

- Windows
- Python 3.11 이상
- VS Code
- Arduino IDE
- Arduino UNO
- Gemini API Key

### 2. Python 가상환경 설정

VS Code에서 프로젝트 폴더를 열고 터미널에 다음 명령어를 입력합니다.

```powershell
py -3.13 -m venv .venv
```

가상환경 활성화:

```powershell
.\.venv\Scripts\Activate.ps1
```

라이브러리 설치:

```powershell
python -m pip install -r requirements.txt
```

### 3. Gemini API 키 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성합니다.

```env
GEMINI_API_KEY=YOUR_API_KEY

LLM_MODEL=사용_가능한_Gemini_모델_ID
TTS_MODEL=사용_가능한_TTS_모델_ID
TTS_VOICE=Puck

ARDUINO_PORT=COM3
```

Gemini 모델 ID는 Google AI Studio에서 사용 가능한 모델을 확인한 뒤 설정합니다.

`ARDUINO_PORT`는 실제 Arduino가 연결된 COM 포트로 변경합니다.

> ⚠️ `.env` 파일에는 실제 API 키가 포함되므로 GitHub에 업로드하지 않습니다.

### 4. AI 말투 데이터 작성

`style_samples.txt` 파일에 원하는 말투의 예시를 한 줄씩 작성합니다.

Gemini는 해당 데이터를 참고하여 새로운 대사를 생성합니다.

별도의 모델 파인튜닝 없이 프롬프트 기반으로 말투를 적용합니다.

### 5. AI 대사 및 음성 생성

다음 명령어를 실행합니다.

```powershell
python generate_bank.py --count 20
```

실행 과정은 다음과 같습니다.

```text
말투 예시 불러오기
        ↓
Gemini 대사 생성
        ↓
TTS 음성 합성
        ↓
WAV 파일 저장
        ↓
voices/ 폴더 생성
```

`--count` 옵션으로 생성할 대사 개수를 지정할 수 있습니다.

> ⚠️ 기본 `generate_bank.py`는 재실행 시 기존 음성을 덮어쓸 수 있습니다. 기존 음성을 보존하려면 별도로 백업하거나 음성 추가 저장 패치를 적용해야 합니다.

### 6. Arduino 코드 업로드

Arduino IDE에서 다음 파일을 엽니다.

```text
arduino/amudo_bot_v2/amudo_bot_v2.ino
```

Arduino IDE에서 아래와 같이 설정합니다.

```text
Board : Arduino Uno
Port  : Arduino가 연결된 COM 포트
```

설정이 완료되면 업로드 버튼을 눌러 코드를 보드에 업로드합니다.

### 7. 로봇 실행

Arduino IDE의 시리얼 모니터를 닫은 후 VS Code 터미널에서 실행합니다.

```powershell
python run_robot.py
```

실행 후 주변 소리가 감지되면 저장된 WAV 파일 중 하나를 무작위로 재생하며, 동시에 서보모터가 움직입니다.

프로그램을 종료하려면 `Ctrl + C`를 누릅니다.

---

## 🎚️ 소리 감지 설정

Arduino 코드에서 다음 값을 변경하여 마이크 감도를 조절할 수 있습니다.

```cpp
const int SOUND_THRESHOLD = 30;
const unsigned long CONFIRM_MS = 280;
const unsigned long ALLOWED_GAP_MS = 140;
const bool DEBUG_SOUND = false;
```

| 변수 | 설명 |
| --- | --- |
| `SOUND_THRESHOLD` | 소리 감지 기준값 |
| `CONFIRM_MS` | 발화 시작 후보를 확인하는 최소 시간 |
| `ALLOWED_GAP_MS` | 소리 사이 허용하는 짧은 무음 시간 |
| `DEBUG_SOUND` | 소리 측정값 출력 여부 |

실제 사용 환경에 따라 기준값을 조절해야 합니다.

`SOUND_THRESHOLD`는 데시벨(dB)이 아니라 아날로그 입력 신호의 변화 폭을 기준으로 합니다.

감도를 높이면 작은 소리에도 반응하지만, 주변 소음에 의한 오작동 가능성도 커집니다.

---

## ⚠️ 주의사항 및 한계

### 음성 인식 방식

본 프로젝트는 STT(Speech-to-Text)를 사용하지 않습니다.

따라서 사람의 대화 내용을 분석하거나 특정 단어를 인식하지 않습니다.

마이크로 측정한 소리의 크기와 지속 시간을 기준으로 발화 시작 여부를 추정하기 때문에 음악, 웃음소리, 연속적인 박수 등에 반응할 수도 있습니다.

### 실시간 AI 생성 여부

Gemini API는 음성 출력 시점이 아니라 사전에 대사를 생성할 때 사용합니다.

실제 로봇 작동 중에는 저장된 WAV 파일을 재생하므로, 매번 새로운 문장을 실시간으로 생성하지는 않습니다.

이는 대화에 끼어드는 반응 속도를 높이기 위한 설계입니다.

### 시리얼 포트 충돌

Arduino IDE와 Python 프로그램이 동시에 같은 COM 포트를 사용하면 연결 오류가 발생할 수 있습니다.

Arduino 코드를 업로드할 때는 `run_robot.py`를 종료하고, Python 프로그램을 실행할 때는 Arduino IDE의 시리얼 모니터를 닫아야 합니다.

---