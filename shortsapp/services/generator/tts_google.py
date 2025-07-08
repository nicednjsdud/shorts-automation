import os
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-credentials.json"

# Google TTS 클라이언트
client = texttospeech.TextToSpeechClient()


# 음성 생성 함수
def synthesize_speech(
    text,
    lang_code="ko-KR",
    gender="FEMALE",
    voice_name=None,
    out_path="media/output.mp3",
    speaking_rate=1.4,
):

    # 입력
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # 화자 설정
    gender_map = {
        "MALE": texttospeech.SsmlVoiceGender.MALE,
        "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
        "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL,
    }

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang_code,
        name=voice_name or "",
        ssml_gender=gender_map.get(
            gender.upper(), texttospeech.SsmlVoiceGender.NEUTRAL
        ),
    )

    # 출력포맷
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
    )

    # 요청
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    #  저장
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as out:
        out.write(response.audio_content)
        print(f"✅ 음성 저장 완료: {out_path}")

    return out_path


# 사용 예시

synthesize_speech(
    text="안녕하세요. 구글 클라우드 텍스트 투 스피치입니다.",
    lang_code="ko-KR",
    gender="FEMALE",
    voice_name="ko-KR-Wavenet-A",
    out_path="media/test_audio.mp3",
)
