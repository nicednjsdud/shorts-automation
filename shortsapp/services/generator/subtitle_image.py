
from PIL import Image, ImageDraw, ImageFont
import os


# 텍스트 이미지를 생성합니다.
def generate_text_image(text, font_path, width=720, height=250, font_size=40, font_color="black"):
    os.makedirs("media/temp_text", exist_ok=True)
    img = Image.new("RGBA", (width, height), color=(0, 0, 0, 180))
    draw = ImageDraw.Draw(img)
    
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

def wrap_text(text, font, max_width):
    dummy_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy_img)
    lines, line = [], ""
    for word in text.split():
        test_line = f"{line} {word}".strip()
        if draw.textsize(test_line, font=font)[0] <= max_width - 40:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return "\n".join(lines)
