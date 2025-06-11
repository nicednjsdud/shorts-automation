from moviepy.editor import ImageClip, CompositeVideoClip
from .subtitle_image import generate_text_image
import os

VIDEO_SIZE = (720, 1280)

# 동영상 클립을 생성합니다.
def create_slide_clip(text, image_path, duration, font_size=50, font_color="black"):
    # 배경 이미지 클립
    image_clip = ImageClip(image_path).set_duration(duration).resize(VIDEO_SIZE)

    # 폰트 경로 설정
    font_path = os.path.join("shortsapp", "assets", "NanumGothic.ttf")

    # 줌 효과 (Ken Burns 스타일)
    zoom_clip = image_clip.resize(lambda t: 1 + 0.0002 * t).set_position("center")

    # 🆕 텍스트 이미지를 만들어 클립으로 전환
    text_img_path = generate_text_image(text, font_path=font_path, width=VIDEO_SIZE[0], height=250, font_size=font_size, font_color=font_color)
    text_clip = ImageClip(text_img_path).set_duration(duration).set_position(("center", "bottom"))

    return CompositeVideoClip([zoom_clip, text_clip], size=image_clip.size)
