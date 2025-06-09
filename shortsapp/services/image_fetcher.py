import requests
import os
from time import sleep

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def fetch_unsplash_images(query, save_dir='media', count=4):
    if not query:
        query = "technology"  # 기본 검색어 설정

    url = f"https://api.unsplash.com/photos/random?query={query}&count={count}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsplash API error: {response.status_code}, {response.text}")
    
    data = response.json()
    image_paths = []

    # ✅ 리스트 안에 각 항목에서 urls 키를 찾음
    for i, item in enumerate(data):
        if 'urls' not in item:
            continue  # urls가 없으면 스킵

        image_url = item['urls']['regular']
        image_path = os.path.join(save_dir, f'bg_{i}.jpg')

        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as f:
            f.write(img_data)
        
        print(f"✅ 이미지 저장 완료: {image_path}")
        sleep(0.2)

        image_paths.append(image_path)

    return image_paths
