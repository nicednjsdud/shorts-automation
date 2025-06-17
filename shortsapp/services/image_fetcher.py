from PIL import ImageOps, Image
import requests
import os
from time import sleep

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def pad_to_9_16(image: Image.Image, target_size=(720, 1280)) -> Image.Image:
    return ImageOps.fit(image, target_size, Image.ANTIALIAS, centering=(0.5, 0.5))

def fetch_unsplash_images(query, save_dir='media', count=4):
    if not query:
        query = "technology"  # 기본 검색어 설정

    url = f"https://api.unsplash.com/photos/random?query={query}&count={count}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Unsplash API error: {response.status_code}, {response.text}")

    data = response.json()
    image_paths = []

    for i, item in enumerate(data):
        if 'urls' not in item:
            continue  # urls가 없으면 스킵

        image_url = item['urls']['regular']
        image_path = os.path.join(save_dir, f'bg_{i}.jpg')

        # ✅ 이미지 다운로드 & 열기
        image_response = requests.get(image_url, stream=True)
        img = Image.open(image_response.raw).convert("RGB")

        # ✅ 9:16 패딩
        img = pad_to_9_16(img, (720, 1280))

        # ✅ 저장
        img.save(image_path, format="JPEG")
        print(f"✅ 이미지 저장 완료: {image_path}")

        image_paths.append(image_path)
        sleep(0.2)  # 너무 빠른 호출 방지

    return image_paths
