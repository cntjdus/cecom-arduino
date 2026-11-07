"""Arduino에서 SPEECH 신호 수신 -> 사전 합성한 WAV 1개 재생 + 모터 제어.
Windows용: winsound 사용 (다른 OS라면 재생 라이브러리 변경 필요)
"""
import os
import random
import time
import winsound
from pathlib import Path

import serial
from dotenv import load_dotenv
from serial.tools import list_ports

load_dotenv()
PORT = os.getenv("ARDUINO_PORT", "COM3")
BAUD = 115200
COOLDOWN_SECONDS = 1.5


def send(board: serial.Serial, msg: str) -> None:
    board.write((msg + "\n").encode("ascii"))
    board.flush()


def main() -> None:
    clips = sorted(Path("voices").glob("*.wav"))
    if not clips:
        raise RuntimeError("voices/에 WAV 파일이 없습니다. 먼저 python generate_bank.py --count 8 실행")
    print(f"[준비] 음성 {len(clips)}개 / 포트 {PORT}")
    print("[참고] 포트 목록:", [x.device for x in list_ports.comports()])
    previous = None

    with serial.Serial(PORT, BAUD, timeout=0.4) as board:
        time.sleep(2.0)  # UNO는 USB 연결 시 자동 리셋됨
        board.reset_input_buffer()
        send(board, "LISTEN")
        print("[대기] 사람의 말소리 시작을 기다리는 중. 종료 Ctrl+C")
        try:
            while True:
                line = board.readline().decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                if line.startswith("LEVEL:"):
                    print("[마이크]", line)
                    continue
                if line != "SPEECH":
                    print("[아두이노]", line)
                    continue

                choices = [p for p in clips if p != previous] or clips
                clip = random.choice(choices)
                previous = clip
                print(f"[끼어들기] {clip.name}")
                send(board, "TALK")
                try:
                    winsound.PlaySound(str(clip.resolve()), winsound.SND_FILENAME)
                finally:
                    send(board, "STOP")
                    time.sleep(COOLDOWN_SECONDS)
                    board.reset_input_buffer()
                    send(board, "LISTEN")
        except KeyboardInterrupt:
            print("\n[종료] 안전하게 정지합니다.")
        finally:
            send(board, "STOP")


if __name__ == "__main__":
    main()
