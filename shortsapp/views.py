from django.shortcuts import render
from django.http import JsonResponse
from shortsapp.services.youtube import upload_video
from .forms import TextInputForm
from .services.generator.processor import process_script
from .services.image_fetcher import fetch_unsplash_images
from shortsapp.services.translator import translate_to_english
from shortsapp.services.youtube.uploader import upload_video
from shortsapp.services.youtube.tags import extract_keywords
import os

DEFAULT_VOICES = {
    ('ko-KR', 'FEMALE'): 'ko-KR-Wavenet-A',
    ('ko-KR', 'MALE'): 'ko-KR-Wavenet-B',
    ('en-US', 'FEMALE'): 'en-US-Wavenet-C',
    ('en-US', 'MALE'): 'en-US-Wavenet-D',
}

def index(request):
    video_path = None
    form = TextInputForm()

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            script = form.cleaned_data['script']
            style_prompt = form.cleaned_data['style_prompt']
            ai_background = form.cleaned_data.get('ai_background', False)
            font_color = form.cleaned_data['font_color']
            font_size = form.cleaned_data['font_size']
            title_text = form.cleaned_data["title_text"]

            # 🎯 태그 추출
            generated_tags = extract_keywords(script + " " + title_text)
            
            # 📸 배경 이미지 경로 지정
            image_paths = os.path.join('media', 'bg.jpg')

            # 화자 설정 수집
            speaker_settings = {}
            for speaker in ['A', 'B', 'C']:
                gender = request.POST.get(f"gender_{speaker}")
                lang = request.POST.get(f"lang_{speaker}")
                if gender and lang:
                    voice_name = DEFAULT_VOICES.get((lang, gender), '')
                    speaker_settings[speaker] = {
                        "gender": gender,
                        "lang": lang,
                        "voice": voice_name
                    }

            if ai_background:
                 # ✅ 스타일 프롬프트를 영어로 번역
                style_prompt_en = translate_to_english(style_prompt)

                # ✅ 번역된 영어 키워드로 이미지 자동 가져오기
                image_paths = fetch_unsplash_images(style_prompt_en, save_dir='media', count=6)
            else:
                # 🔁 기본 배경 또는 선택 배경 사용할 경우 (원한다면 수정 가능)
                pass  # 사용자가 직접 업로드한 이미지를 처리하려면 여기에 넣기

            # 🎥 영상 생성 실행
            video_path = process_script(
                script, 
                image_paths, 
                font_color, 
                font_size,
                speaker_settings=speaker_settings,
                title_text=title_text,
            )

            # ✅ 세션 저장 (유튜브 업로드용)
            request.session["video_path"] = video_path
            request.session["title_text"] = title_text
            request.session["tags"] = generated_tags

    return render(request, 'index.html', {
        'form': form,
        'video_path': video_path,
        'title' : title_text,
        'tags': generated_tags
    })


# 유튜브 업로드 뷰
def upload_to_youtube(request):
    video_path = request.session.get("video_path")
    title_text = request.session.get("title_text")
    tags = request.session.get("generated_tags", [])

    if not video_path or  not os.path.exists(video_path):
        return JsonResponse({"error": "영상이 생성되지 않았습니다."}, status=400)
    
    video_id = upload_video(
        file_path=video_path,
        title=title_text,
        description="유튜브 쇼츠",
        tags=tags,
        category_id="22",  # People & Blogs
    )

    return JsonResponse({"success": True, "video_id": video_id})