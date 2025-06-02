import requests
import os

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def fetch_unsplash_image(query, save_path):
    if not query:
        query = "technology"  # 기본 검색어 설정

    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsplash API error: {response.status_code}, {response.text}")
    
    data = response.json()

    # 안전하게 키 접근
    if 'urls' not in data:
        raise KeyError(f"Expected 'urls' in response, got: {data}")

    image_url = data['urls']['regular']
    img_data = requests.get(image_url).content

    with open(save_path, 'wb') as f:
        f.write(img_data)

    return save_path
