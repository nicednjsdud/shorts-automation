from PIL import Image, ImageDraw, ImageFont
import os


# 텍스트 이미지를 생성합니다.
# 주어진 텍스트를 지정된 폰트와 크기로 이미지에 렌더링합니다.
# args:
#   text: 렌더링할 텍스트
#   font_path: 사용할 폰트 파일 경로
#   width: 이미지 너비 (기본값: 720)
#   height: 이미지 높이 (기본값: 250)
#   font_size: 폰트 크기 (기본값: 40)
#   font_color: 폰트 색상 (기본값: "black")
# returns:
#   생성된 이미지 파일의 경로
def generate_subtitle_text_image(
    text, font_path, width=720, height=500, font_size=55, font_color="black"
):
    os.makedirs("media/temp_text", exist_ok=True)
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 10))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print("⚠️ 폰트 로딩 실패:", e)
        font = ImageFont.load_default()

    wrapped_text = wrap_text(text, font, width - 80)

    text_width, text_height = draw.multiline_textsize(wrapped_text, font=font, spacing=10)
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 240  
    
    draw.text((x, y), text, font=font, fill=font_color)
    filename = f"media/temp_text/temp_text_{hash(text)}.png"
    img.save(filename)
    return filename


def wrap_text(text, font, max_width):
    from PIL import Image, ImageDraw

    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    lines, line = [], ""

    for word in text.split():
        test_line = f"{line} {word}".strip()
        if draw.textsize(test_line, font=font)[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word

    lines.append(line)
    return "\n".join(lines)
