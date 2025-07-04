from PIL import Image, ImageDraw, ImageFont
import os

# 타이틀 이미지를 생성하는 함수
# 주어진 텍스트를 지정된 폰트와 크기로 이미지에 렌더링합니다.
# args:
#   text: 렌더링할 텍스트
#   width: 이미지 너비 (기본값: 720)
#   height: 이미지 높이 (기본값: 200)
#   font_size: 폰트 크기 (기본값: 35)
#   font_color: 폰트 색상 (기본값: "white")
# returns:
#   생성된 이미지 파일의 경로
def generate_title_image(text, width=720, height=200, font_size=35, font_color="white"):
    os.makedirs("media/temp_text", exist_ok=True)
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 100))  # 반투명 배경
    draw = ImageDraw.Draw(img)

    font_path = os.path.join("shortsapp", "assets", "MaruBuri-Bold.ttf")
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print("⚠️ 타이틀 폰트 로딩 실패:", e)
        font = ImageFont.load_default()

    # 텍스트 위치 중앙 정렬
    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)

    draw.text(position, text, font=font, fill=font_color)

    filename = f"media/temp_text/title_{hash(text)}.png"
    img.save(filename)
    return filename
