# 아무도 안 물어봇 v2 — STT 없는 반응형 음성 난입 로봇

**설계 기준(2026-11)**: 사람의 말소리 *내용*은 인식하지 않습니다. MAX9814 아날로그 소리 감지로 말 시작을 추정하고, 사전에 Gemini가 생성한 대사와 TTS WAV 음성을 거의 즉시 재생합니다. Arduino UNO는 서보모터를 움직입니다.

## 구성
- `style_samples.txt`: 팀이 직접 정하는 말투 예시(텍스트)
- `generate_bank.py`: LLM이 새 대사를 생성하고 TTS로 WAV를 사전 저장
- `run_robot.py`: Serial의 `SPEECH` 수신 시 WAV 재생 + 서보모터 제어
- `arduino/amudo_bot_v2/amudo_bot_v2.ino`: 마이크 센서 + 서보 + 시리얼
- `.env.example`: API 키·모델명·포트 설정

## 0. 먼저 준비하기
ZIP 파일을 압축 해제한 뒤 VS Code에서 `amudo_bot_v2` 폴더를 엽니다. Python 3.11과 Arduino IDE를 설치합니다.

## 1. Windows + Python 3.11
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env`에 실제 GEMINI_API_KEY, 사용 가능한 모델명, TTS 음성 및 ARDUINO_PORT를 지정합니다. `.env`는 업로드 금지.

## 2. 말투 작성 및 음성 생성(마이크·아두이노 없이 먼저 진행)
`style_samples.txt`를 먼저 편집하고 원하는 예시 대사를 한 줄씩 적으세요. 코드가 예시를 바탕으로 새로운 대사를 만든 후 TTS 음성을 저장합니다.

```powershell
python generate_bank.py --count 8
```
`voices/001.wav` 등 WAV 생성 확인. Gemini 호출에 할당량/요금이 발생할 수 있습니다. 우선 5~8개만 생성하세요. 모델이 사용할 수 없는 경우 Google AI Studio에서 실제 지원 모델로 `.env`를 수정하세요.

## 3. 하드웨어 배선
| 부품 핀 | 연결 |
|---|---|
| MAX9814 VDD | Arduino 5V |
| MAX9814 GND | Arduino GND |
| MAX9814 OUT | Arduino A0 |
| SG90 신호선(노랑/주황) | Arduino D9 |
| SG90 빨강 | 별도 안정적인 5V 전원 + |
| SG90 검정/갈색 | 외부 전원 GND |
| Arduino GND | 외부 전원 GND(공통 GND) |
| Arduino USB | Windows 노트북 |

외부 전원 +5V를 USB로 전원 공급 중인 Arduino 5V에 무작정 직결하지 마세요. 반드시 공통 GND를 연결하세요.

## 4. Arduino IDE
- 보드 `Arduino UNO`, 포트 선택
- `amudo_bot_v2.ino` 업로드
- 감지값 보정: 코드의 `DEBUG_SOUND = true` → 업로드 → 시리얼 모니터 115200 baud 열기 → 줄바꿈 설정 후 `LISTEN` 전송 → 조용할 때/말할 때 `LEVEL:` 비교 → `SOUND_THRESHOLD` 조정 → `DEBUG_SOUND = false` 후 재업로드
- Python 실행 전에는 시리얼 모니터를 반드시 닫으세요.

## 5. 시연
```powershell
python run_robot.py
```
누군가 말할 때 Arduino가 `SPEECH`를 전송하며, 준비된 WAV가 노트북 스피커로 재생됩니다. 동시 서보 고개 움직임, 음성 종료 후 1.5초 대기, 다시 감지. `Ctrl+C` 종료.

## 자주 생기는 문제
- `COM3` 실패: 장치 관리자 또는 Arduino IDE의 실제 포트를 `.env`에 반영하고 시리얼 모니터를 닫습니다.
- 감지 안 됨/너무 자주 감지: `DEBUG_SOUND`로 `LEVEL` 확인 후 `SOUND_THRESHOLD`, `CONFIRM_MS`를 조정합니다. 이 방법은 소리를 측정하는 것이며 사람 목소리만 구분하지 못합니다.
- TTS 실패: Gemini API 접근, 잔여 할당량, 사용 가능한 모델명 확인. Gemini 3.8 TTS는 Interactions API의 WAV 출력을 사용합니다.
- 소리가 안 남: Windows 기본 출력 장치·볼륨·voices WAV 파일 확인.
- 모터 오작동: 외부 5V 전류 용량·공통 GND·배선 점검.
- 이 예제는 아직 실제 API/보드 환경에서 통합 테스트하지 않은 참조 구현이므로 연결 시 검증이 필요합니다.

## 주의
공개 장소에서는 참가자의 동의를 받고 시연하세요. 사람 음성은 텍스트로 변환하거나 서버로 보내지 않으며, 별도 음성 녹음 파일도 저장하지 않습니다. 소리 세기로만 트리거하는 구조이므로 음악·박수에도 반응할 수 있습니다.
