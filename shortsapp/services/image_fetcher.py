import requests
import os

UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')

def fetch_unsplash_image(query, save_path):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    data = response.json()

    image_url = data['urls']['regular']
    img_data = requests.get(image_url).content

    with open(save_path, 'wb') as handler:
        handler.write(img_data)
    
    return save_path