from django.shortcuts import render
from .forms import TextInputForm
from .services.generator import process_script
from .services.background_picker import suggest_backgrounds
from .services.ai_image_generator import generate_ai_imag

def index(request):
    video_path = None
    bg_suggestions = []

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            script = form.cleaned_data['script']
            style_prompt = form.cleaned_data['style_prompt']
            ai_background = form.cleaned_data['ai_background'] # AI 배경 생성 여부
            selected_bg = request.POST.get('selected_background', None)

            # 배경 선택 전이면 추천 목록 먼저 보여줌
            if not selected_bg and not ai_background:
                bg_suggestions = suggest_backgrounds(style_prompt)
            else:
                # ✅ 배경 이미지 선택 처리
                if ai_background:
                    background_path = generate_ai_image(style_prompt)
                else:
                    background_path = os.path.join(
                        settings.BASE_DIR, 'static', 'backgrounds', selected_bg)

                # ✅ 자막 스타일도 나중에 여기서 받아서 넘길 수 있음
                video_path = process_script(script, background_path)
        else:
            form = TextInputForm()

        return render(request, 'index.html',{
            'form' : form,
            'background_suggestions': bg_suggestions,
            'video_path': video_path,
        })    
    else:
        form = TextInputForm()

    return render(request, 'index.html', {
        'form': form,
        'background_suggestions': [],
        'video_path': None,
    })     