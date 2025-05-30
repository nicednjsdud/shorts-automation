from django import forms

# 영상 생성에 필요한 입력 폼 정의
# 이 폼은 사용자가 영상 스크립트와 스타일을 입력할 수 있도록 합니다.
# # 스크립트는 화자별로 "화자: 대사" 형태로 입력되어야 하며,
# 스타일은 영상의 분위기나 톤을 설명하는 선택적 필드입니다.
class TextInputForm(forms.Form):
    script = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        label='영상 스크립트'
    )
    style_prompt = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '예: 면접 분위기, IT 컨퍼런스, 밝고 캐주얼한 느낌'}),
        label='원하는 영상 스타일 (설명)',
        required=False
    )
    ai_background = forms.BooleanField(
        required=False,
        label='AI 추천 배경 사용',
        help_text='선택 시 AI가 추천하는 배경을 사용합니다.'
    )
    font_color = forms.ChoiceField(
        choices=[
            ('black', '검정'),
            ('white', '흰색'),
            ('red', '빨강'),
            ('blue', '파랑'),
            ('green', '초록'),
        ],
        label='자막 글자 색상',
        initial='white',
    )
    font_size = forms.ChoiceField(
        choices=[
            ('small', '작게'),
            ('medium', '보통'),
            ('large', '크게'),
        ],
        label='자막 글자 크기',
        initial='medium',
    )

    
