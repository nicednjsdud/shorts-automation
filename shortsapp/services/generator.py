import os
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip
from django.conf import settings

# 화자별 TTS 속성 정의 (간단한 스타일 차이용, 추후 교체 가능)
VOICE_PROFILES = {
    "면접관": {"lang": "ko", "slow": False},
    "면접자": {"lang": "ko", "slow": True},
}

# 기본 배경 이미지 경로 (고정 배경 사용, 나중에 영상으로 교체 가능)
BACKGROUND_IMAGE = os.path.join(settings.BASE_DIR, 'static', 'bg.jpg')

# 기본 폰트 경로 (한글 지원 폰트 사용 필요)
FONT_PATH = os.path.join(settings.BASE_DIR, 'static', 'NanumGothic.ttf')


# 전체 스크립트를 줄 단위로 파싱
# 각 줄은 "화자: 대사" 형태로 되어 있어야 함
def parse_script(script_text):  
    lines = script_text.strip().split('\n')
    parsed = []
    for line in lines:
        if ":" in line:
            speaker, text = line.split(":", 1)
            parsed.append((speaker.strip(), text.strip()))
    return parsed

# gTTS를 사용해 화자별 음성을 mp3로 생성
def generate_tts(speaker, text, output_path):
    voice = VOICE_PROFILES.get(speaker, {"lang": "ko", "slow": False})
    tts = gTTS(text=text, lang=voice["lang"], slow=voice["slow"])
    tts.save(output_path)

# 한 줄의 텍스트와 음성을 받아서 영상 클립으로 생성
# - 배경 이미지 사용
# - 자막 텍스트 오버레이
# - 음성 오디오 결합

def create_subclip(text, audio_path):
# 음성 길이 측정
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration

    # 배경 이미지 → 영상 클립으로 변환
    bg_clip = ImageClip(BACKGROUND_IMAGE).set_duration(duration).resize(height=1080).set_position("center")

    # 자막 텍스트 클립
    text_clip = TextClip(
        text,
        font= FONT_PATH,
        fontsize=48,
        color='white',
        size=(1080, None),
        method = 'caption',
    ).set_duration(duration).set_position(("center", "bottom"))

    # 오디오 결합
    video = CompositeVideoClip([bg_clip, text_clip])
    video = video.set_audio(audio_clip)

    return video

# 전체 스크립트를 처리하여 영상(mp4) 파일 생성
# - 줄마다 TTS 생성
# - 줄마다 영상 클립 생성
# - 모든 클립 이어붙여 최종 영상 저장
def process_script(script, background_path):
    # 텍스트 → 음성
    tts = gTTS(script, lang='ko')
    audio_path = "media/voice.mp3"
    tts.save(audio_path)

    # 이미지 + 음성 → 영상
    clip = ImageClip(background_path).set_duration(5)
    clip = clip.set_audio(AudioFileClip(audio_path))
    clip = clip.resize(height=720)

    output_path = "media/final_video.mp4"
    clip.write_videofile(output_path, fps=24)

    return output_path