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
    form = TextInputForm()
    generated_tags = []

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

            # 진행 상태 초기화
            request.session["progress"] = 0
            request.session.modified = True

            # 태그 생성
            generated_tags = extract_keywords(script + " " + title_text)

            # 이미지 경로 준비
            if ai_background:
                style_prompt_en = translate_to_english(style_prompt)
                image_paths = fetch_unsplash_images(style_prompt_en, save_dir='media', count=6)
            else:
                image_paths = [os.path.join('media', 'bg.jpg')] * 6

            # 화자별 설정
            speaker_settings = {}
            for speaker in ['A', 'B', 'C']:
                gender = request.POST.get(f"gender_{speaker}")
                lang = request.POST.get(f"lang_{speaker}")
                if gender and lang:
                    voice_name = DEFAULT_VOICES.get((lang, gender), '')
                    speaker_settings[speaker] = {
                        "gender": gender,
                        "lang": lang,
                        "voice": voice_name,
                        'speaking_rate': 1.4,  # 속도 조절
                    }

            # 진행률 예시로 업데이트
            request.session["progress"] = 20
            request.session.modified = True

            # 영상 생성
            video_path = process_script(
                script,
                image_paths,
                font_color,
                font_size,
                speaker_settings=speaker_settings,
                title_text=title_text,
                progress_session=request.session,  # 필요하면 processor에서 progress 갱신
            )

            # 진행 완료
            request.session["progress"] = 100
            request.session["video_path"] = video_path
            request.session["title_text"] = title_text
            request.session["tags"] = generated_tags
            request.session["comment_text"] = comment_text
            request.session.modified = True

    return render(request, 'index.html', {
        'form': form,
        'video_path': request.session.get("video_path"),
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

        # 세션 초기화
        for key in ["video_path", "title_text", "tags", "comment_text"]:
            if key in request.session:
                del request.session[key]
        request.session.modified = True

        return JsonResponse({"success": True, "video_id": video_id})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

def get_progress(request):
    progress = request.session.get("progress", 0)
    return JsonResponse({"progress": progress})
