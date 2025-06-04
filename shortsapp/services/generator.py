from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, vfx, AudioFileClip, concatenate_videoclips, VideoFileClip
from gtts import gTTS
import textwrap
import os
from PIL import Image, ImageDraw, ImageFont

# 이 서비스는 스크립트를 받아서 짧은 동영상을 생성합니다.
# # 필요한 라이브러리:
# - moviepy: 동영상 편집
# - gTTS: 텍스트 음성 변환
# # ## 사용법:
# 1. 스크립트를 입력합니다.
# 2. 스크립트를 여러 부분으로 나눕니다.
def split_script(script, part=3):
    lines = script.strip().split('\n')
    chunk_size = max(1,len(lines) // part)
    return ['\n'.join(lines[i:i + chunk_size]).strip() for i in range(0, len(lines), chunk_size)]

# 동영상 클립을 생성합니다.
def create_slide_clip(text, image_path, duration, font_size=50, font_color="red"):
    # 배경 이미지 클립
    image_clip = ImageClip(image_path).set_duration(duration).resize(height=1080)

    # 줌 효과 (Ken Burns 스타일)
    zoom_clip = image_clip.resize(lambda t: 1 + 0.03 * t)

    # 🆕 텍스트 이미지를 만들어 클립으로 전환
    text_img_path = generate_text_image(text, width=1080, height=300, font_size=font_size, font_color=font_color)
    text_clip = ImageClip(text_img_path).set_duration(duration)
    text_clip = text_clip.set_position(("center", "bottom"))

    return CompositeVideoClip([zoom_clip, text_clip])

# 텍스트 이미지를 생성합니다.
def generate_text_image(text, width=1080, height=300, font_size=40, font_color="red"):
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 180))  # 반투명 배경
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
        raise

    # 줄바꿈 적용
    wrapped_text = textwrap.fill(text, width=40)
    draw.text((50, 50), wrapped_text, fill=font_color, font=font)

    path = "temp_text.png"
    img.save(path)
    return path

# 스크립트를 처리하여 동영상을 생성합니다.
def process_script(script, image_path):
    print("🔨 영상 생성 중...")
    # 1. 스크립트를 여러 부분으로 나눕니다.
    segments = split_script(script, part= 4)

    # 2. TTS 오디오 생성
    tts = gTTS(script, lang='ko')
    audio_path = "media/audio.mp3"
    tts.save(audio_path)
    audio = AudioFileClip(audio_path)

    # 3. 구간별 영상 생성
    segment_duration = audio.duration / len(segments)
    clips = []
    for segment in segments:
        clip = create_slide_clip(
            segment, image_path, duration=segment_duration,
            font_size=60, font_color='white'
        )
        clips.append(clip)

    # 4. 모든 클립을 합칩니다.
    final_video = concatenate_videoclips(clips).set_audio(audio)
    video_path = "media/final_video.mp4"
    final_video.write_videofile(video_path, fps=24)

    print("✅ 영상 생성 완료!")

    return video_path
