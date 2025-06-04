from django.shortcuts import render
from .forms import TextInputForm
from .services.generator import process_script
from .services.image_fetcher import fetch_unsplash_image
from shortsapp.services.translator import translate_to_english
import os

def index(request):
    video_path = None
    form = TextInputForm()

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            script = form.cleaned_data['script']
            style_prompt = form.cleaned_data['style_prompt']
            ai_background = form.cleaned_data.get('ai_background', False)

            # 📸 배경 이미지 경로 지정
            image_path = os.path.join('media', 'bg.jpg')

            if ai_background:
                 # ✅ 스타일 프롬프트를 영어로 번역
                style_prompt_en = translate_to_english(style_prompt)

                # ✅ 번역된 영어 키워드로 이미지 자동 가져오기
                fetch_unsplash_image(style_prompt_en, image_path)
            else:
                # 🔁 기본 배경 또는 선택 배경 사용할 경우 (원한다면 수정 가능)
                pass  # 사용자가 직접 업로드한 이미지를 처리하려면 여기에 넣기

            # 🎥 영상 생성 실행
            video_path = process_script(script, image_path)

    return render(request, 'index.html', {
        'form': form,
        'video_path': video_path,
    })
