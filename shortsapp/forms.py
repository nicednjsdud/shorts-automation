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

    
