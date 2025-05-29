from django.shortcuts import render
from .forms import TextInputForm
from .services.generator import process_script
from .services.background_picker import suggest_backgrounds

def index(request):
    video_path = None
    bg_suggestions = []

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            script = form.cleaned_data['script']
            style_prompt = form.cleaned_data['style_prompt']
            selected_bg = request.POST.get('selected_background', None)

            # 배경 선택 전이면 추천 목록 먼저 보여줌
            if not selected_bg:
                bg_suggestions = suggest_backgrounds(style_prompt)
            else:
                # 영상 생성 실행
                video_path = process_script(script, selected_bg)
        else:
            form = TextInputForm()

        return render(request, 'index.html',{
            'form' : form,
            'background_suggestions': bg_suggestions,
            'video_path': video_path,
        })    