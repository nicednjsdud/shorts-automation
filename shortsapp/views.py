from django.shortcuts import render
from .forms import TextInputForm
from .services.generator import process_script
from .services.image_fetcher import fetch_unsplash_image
import os

def index(request):
    video_path = None

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            script = form.cleaned_data['script']
            style_prompt = form.cleaned_data['style_prompt']

            # 1. 무료 이미지 가져오기
            image_path = os.path.join("media", "bg.jpg")
            fetch_unsplash_image(style_prompt, image_path)

            # 2. 영상 생성
            video_path = process_script(script, image_path)
    else:
        form = TextInputForm()

    return render(request, 'index.html', {
        'form': form,
        'video_path': video_path,
    })
