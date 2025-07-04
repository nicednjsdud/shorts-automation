from django.shortcuts import render
from django.http import JsonResponse
from .forms import TextInputForm
from shortsapp.services.generator.processor import process_script
from shortsapp.services.image_fetcher import fetch_unsplash_images
from shortsapp.services.translator import translate_to_english
from shortsapp.services.youtube.uploader import upload_video
from shortsapp.services.youtube.comments import post_comment
from shortsapp.services.youtube.tags import extract_keywords
from shortsapp.services.youtube.auth import get_authenticated_service
import os

DEFAULT_VOICES = {
    ('ko-KR', 'FEMALE'): 'ko-KR-Wavenet-A',
    ('ko-KR', 'MALE'): 'ko-KR-Wavenet-B',
    ('en-US', 'FEMALE'): 'en-US-Wavenet-C',
    ('en-US', 'MALE'): 'en-US-Wavenet-D',
}

def index(request):
    video_path = None
    generated_tags = []
    form = TextInputForm()

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            script = form.cleaned_data['script']
            style_prompt = form.cleaned_data['style_prompt']
            ai_background = form.cleaned_data['ai_background']
            font_color = form.cleaned_data['font_color']
            font_size = form.cleaned_data['font_size']
            title_text = form.cleaned_data['title_text']
            comment_text = form.cleaned_data['comment_text']

            # 태그 생성
            generated_tags = extract_keywords(script + " " + title_text)

            # 이미지 경로 준비
            image_paths = os.path.join('media', 'bg.jpg')
            if ai_background:
                style_prompt_en = translate_to_english(style_prompt)
                image_paths = fetch_unsplash_images(style_prompt_en, save_dir='media', count=6)

            # 화자별 음성 설정
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

            # 영상 생성
            video_path = process_script(
                script, image_paths, font_color, font_size,
                speaker_settings=speaker_settings, title_text=title_text,
            )
            print("comment_text:", comment_text)
            # 세션 저장
            request.session["video_path"] = video_path
            request.session["title_text"] = title_text
            request.session["tags"] = generated_tags
            request.session["comment_text"] = comment_text

    return render(request, 'index.html', {
        'form': form,
        'video_path': video_path,
        'tags': generated_tags,
    })

def upload_to_youtube(request):
    video_path = request.session.get("video_path")
    title_text = request.session.get("title_text")
    tags = request.session.get("tags", [])
    comment_text = request.session.get("comment_text", "")

    if not video_path or not os.path.exists(video_path):
        return JsonResponse({"error": "영상이 생성되지 않았습니다."}, status=400)

    try:
        video_id = upload_video(
            file_path=video_path,
            title=title_text,
            description="유튜브 쇼츠",
            tags=tags,
            category_id="22",
        )

        youtube = get_authenticated_service()

        if comment_text:
            post_comment(youtube, video_id, comment_text)
            

        print("✅ 유튜브 업로드 성공:", video_id)
        # 세션에서 비디오 경로 제거
        del request.session["video_path"]
        del request.session["title_text"]
        del request.session["tags"]
        del request.session["comment_text"]

        return JsonResponse({"success": True, "video_id": video_id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
