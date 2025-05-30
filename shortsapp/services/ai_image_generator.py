import openai
import uuid
import os
import requests
from django.conf import settings


openai.api_key = settings.OPENAI_API_KEY

# DALL·E API를 사용해 배경 이미지를 생성하고 저장
def generate_ai_image(prompt: str) -> str:

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024",
    )
    image_url = response['data'][0]['url']

    # 이미지 다운로드
    image_data = requests.get(image_url).content
    filename = f"{uuid.uuid4().hex}.png"
    save_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(save_path, 'wb') as f:
        f.write(image_data)

    return save_path

