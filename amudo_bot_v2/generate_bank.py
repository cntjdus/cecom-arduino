"""팀의 말투 예시 -> LLM 대사 -> Gemini TTS 음성 파일을 사전 생성합니다.

실행: python generate_bank.py --count 8
Windows/Python 3.11 권장. 실제 API 호출 및 비용/쿼터가 발생할 수 있습니다.
"""
import argparse
import base64
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv()

STYLE_FILE = Path("style_samples.txt")
VOICE_DIR = Path("voices")


def extract_lines(raw: str, count: int) -> list[str]:
    result = []
    seen = set()
    for row in raw.splitlines():
        # 번호/불릿/따옴표 정리
        row = re.sub(r"^\s*(?:[-*]|\d+[.)])\s*", "", row).strip().strip('"“”')
        row = " ".join(row.split())
        if not row or row in seen or len(row) > 70:
            continue
        seen.add(row)
        result.append(row)
        if len(result) >= count:
            break
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=8, help="생성할 대사 개수 (첫 테스트는 5~8개)")
    args = parser.parse_args()
    count = max(1, min(args.count, 50))

    examples = STYLE_FILE.read_text(encoding="utf-8").strip()
    if not examples:
        raise RuntimeError("style_samples.txt에 말투 예시를 적어 주세요.")

    # Client는 환경변수 GEMINI_API_KEY를 자동으로 읽습니다.
    client = genai.Client()
    import os
    llm_model = os.getenv("LLM_MODEL", "gemini-3.8-flash")
    tts_model = os.getenv("TTS_MODEL", "gemini-3.8-flash-lite-tts")
    voice = os.getenv("TTS_VOICE", "Puck")

    prompt = f"""당신은 짧은 코미디 공연의 '불쑥 끼어드는 로봇' 캐릭터 대사를 씁니다.
다음 말투 예시의 어휘, 호흡, 뻔뻔한 훈수·빈정거림 느낌을 참고하되
같은 문장을 반복하지 말고 새 한국어 대사 {count}개를 만들어 주세요.
한 줄당 대사 하나. 번호, 설명, 이모지, 따옴표 금지. 12~40자 권장.
특정 실존 인물이나 집단의 정체성을 비하하거나 위협하지 말고 가벼운 풍자로 제한.
말투 예시:\n{examples}\n"""
    print("[1/2] LLM 대사 생성 중...")
    response = client.models.generate_content(model=llm_model, contents=prompt)
    lines = extract_lines(response.text or "", count)
    if not lines:
        raise RuntimeError("대사가 생성되지 않았습니다. 모델명과 API 키를 확인해 주세요.")

    VOICE_DIR.mkdir(exist_ok=True)
    (VOICE_DIR / "lines.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"[생성] {len(lines)}개 대사 준비됨")

    ok = 0
    for idx, line in enumerate(lines, 1):
        path = VOICE_DIR / f"{idx:03d}.wav"
        print(f"[2/2] TTS {idx}/{len(lines)}: {line}")
        try:
            # Gemini 3.8 TTS uses the Interactions API.
            # Non-streaming output contains a complete WAV file as base64.
            interaction = client.interactions.create(
                model=tts_model,
                input=[{
                    "type": "user_input",
                    "content": [{
                        "type": "text",
                        "text": line,
                        "annotations": [{
                            "type": "speech_metadata",
                            "style": "dry, smug, teasing; conversational Korean with brisk pacing",
                        }],
                    }],
                }],
                response_format={"type": "audio"},
                generation_config={
                    "speech_config": [{"voice": voice}],
                },
            )
            if not interaction.output_audio or not interaction.output_audio.data:
                print("  -> 음성 데이터 없음: 해당 대사 건너뜀")
                continue
            data = base64.b64decode(interaction.output_audio.data)
            if not data.startswith(b"RIFF"):
                print("  -> WAV(RIFF) 형식이 아님: 응답 형식을 확인해 주세요")
                continue
            path.write_bytes(data)
            ok += 1
        except Exception as exc:
            print("  -> 오류:", exc)
    print(f"\n완료: {ok}개 WAV 저장. 위치: {VOICE_DIR.resolve()}")
    if not ok:
        raise RuntimeError("음성 파일 생성 실패. TTS 모델 접근·응답 형식·쿼터를 확인해 주세요.")


if __name__ == "__main__":
    main()
