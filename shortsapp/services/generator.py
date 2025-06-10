from moviepy.editor import ImageClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS
import os
from PIL import Image, ImageDraw, ImageFont
import re

# 이 서비스는 스크립트를 받아서 짧은 동영상을 생성합니다.
# # 필요한 라이브러리:
# - moviepy: 동영상 편집
# - gTTS: 텍스트 음성 변환
# # ## 사용법:
# 1. 스크립트를 입력합니다.
# 2. 스크립트를 여러 부분으로 나눕니다.

VIDEO_SIZE = (720, 1280)  # (width, height)

# 마침표, 물음표, 느낌표, 큰따옴표 등으로 문장을 분할합니다.
#  단, 줄바꿈 문자도 함께 고려합니다.
def split_script_by_sentences(script):

    pattern = r'(?<=[.!?\"\”])\s+'
    sentences = re.split(pattern, script)
    return [s.strip() for s in sentences if s.strip()]


# 동영상 클립을 생성합니다.
def create_slide_clip(text, image_path, duration, font_size=50, font_color="black"):
    # 배경 이미지 클립
    image_clip = ImageClip(image_path).set_duration(duration).resize(VIDEO_SIZE)


    # 줌 효과 (Ken Burns 스타일)
    zoom_clip = image_clip.resize(lambda t: 1 + 0.001 * t).set_position("center")

    # 🆕 텍스트 이미지를 만들어 클립으로 전환
    text_img_path = generate_text_image(text, width=VIDEO_SIZE[0], height=250, font_size=font_size, font_color=font_color)
    text_clip = ImageClip(text_img_path).set_duration(duration).set_position(("center", "bottom"))

    return CompositeVideoClip([zoom_clip, text_clip], size=image_clip.size)

# 텍스트 이미지를 생성합니다.
def generate_text_image(text, width=720, height=250, font_size=40, font_color="black"):
    os.makedirs("media/temp_text", exist_ok=True)  # 폴더 없으면 생성
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 180))
    draw = ImageDraw.Draw(img)

    font_path = os.path.join("shortsapp", "assets", "NanumGothic.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print("⚠️ 폰트 로딩 실패:", e)
        font = ImageFont.load_default()

    wrapped_text = wrap_text(text, font, width)

    draw.text((30, 30), wrapped_text, fill=font_color, font=font)

    filename = f"media/temp_text/temp_text_{hash(text)}.png"
    img.save(filename)
    return filename

# ✅ 이미지 폭 기준으로 줄바꿈 처리
def wrap_text(text, font, max_width):
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)

    lines = []
    words = text.split()
    line = ""

    for word in words:
        test_line = f"{line} {word}".strip()
        line_width, _ = draw.textsize(test_line, font=font)
        if line_width <= max_width - 40:  # 여유 20px padding
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return "\n".join(lines)

# 스크립트를 처리하여 동영상을 생성합니다.
def process_script(script, image_paths, font_color="white", font_size="medium"):
    print("🔨 영상 생성 중...")
    for path in image_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"이미지 경로 없음: {path}")
    
    # 1. 스크립트를 여러 부분으로 나눕니다.
    lines = split_script_by_sentences(script)
    total_lines = len(lines)
    num_images = len(image_paths)
    
    # 2. TTS 전체 음성 생성
    tts = gTTS(text=script, lang='ko')
    audio_path = 'media/audio.mp3'
    tts.save(audio_path)
    audio = AudioFileClip(audio_path)

    # 3. 자막당 시간 계산
    segment_duration = audio.duration / total_lines if total_lines > 0 else 0
    print(f"⏱️ 자막당 시간: {segment_duration:.2f}초")

    # 4. 자막을 이미지에 균등 분배
    clips = []
    lines_per_image = max(1, total_lines // num_images)
    font_pt_size = font_size_to_points(font_size)
    for idx, line in enumerate(lines):
        image_idx = min(idx // lines_per_image, num_images - 1)
        image_path = image_paths[image_idx]

        clip = create_slide_clip(
            line,
            image_path=image_path,
            duration=segment_duration,
            font_size=font_pt_size,
            font_color=font_color
        )
        clips.append(clip)
    
    # 5. 모든 클립을 합칩니다.
    final_video = concatenate_videoclips(clips, method="compose")

    # 🔁 영상 길이와 오디오 길이를 강제로 일치시킴
    final_video = final_video.set_duration(audio.duration).set_audio(audio)

    video_path = "media/final_video.mp4"
    final_video.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        bitrate="1500k",
        threads=4,
        preset="medium"
    )

    print("✅ 영상 생성 완료!")

    # 임시 파일 삭제
    delete_temp_files()

    return video_path

# 글자 크기를 포인트로 변환합니다.
def font_size_to_points(size):
    if size == 'small':
        return 20
    elif size == 'medium':
        return 30
    elif size == 'large':
        return 40
    else:
        raise ValueError("Invalid font size")

# media/temp_text 폴더 정리
def delete_temp_files():
   
    temp_dir = "media/temp_text"
    if os.path.exists(temp_dir):
        for f in os.listdir(temp_dir):
            try:
                os.remove(os.path.join(temp_dir, f))
            except Exception as e:
                print(f"⚠️ {f} 삭제 실패: {e}")
            
