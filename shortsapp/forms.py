from django import forms

# 영상 생성에 필요한 입력 폼 정의
# 이 폼은 사용자가 영상 스크립트와 스타일을 입력할 수 있도록 합니다.
# # 스크립트는 화자별로 "화자: 대사" 형태로 입력되어야 하며,
# 스타일은 영상의 분위기나 톤을 설명하는 선택적 필드입니다.


class TextInputForm(forms.Form):
    script = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        label='영상 스크립트',
        initial="""
A: 면접에서 캐시 스탬피드를 물어본다면?

A: 캐시 스탬피드 현상에 대해 설명해보시겠어요?

B: 트래픽이 급증하던 어느 날,
사용자들이 몰리면서 서비스가 갑자기 느려졌습니다.

B: 그 원인은 바로, '캐시 스탬피드'였습니다.

B: 이건 다수의 요청이 동시에 캐시 미스를 일으켜
한꺼번에 데이터베이스를 두드리는 현상입니다.
결과적으로 DB는 과부하에 걸려버렸죠.

B: 실제 서비스 운영에서도 종종 발생하는 이슈입니다.

B: 이 문제를 해결하기 위해 세 가지 전략을 사용했습니다.

B: 첫째, Locking.
하나의 요청만 DB에 접근하고,
나머지는 캐시가 갱신될 때까지 대기합니다.

B: 둘째, 백그라운드 갱신.
캐시 만료 전에 주기적으로 데이터를 미리 채워놓는 방식입니다.

B: 셋째, 확률적 조기 갱신.
만료 직전의 일부 요청이
새로운 데이터를 갱신하도록 유도합니다.

B: 이러한 전략 덕분에
캐시가 만료되더라도 DB는 더 이상 부담을 느끼지 않습니다.
서비스 속도도 안정적으로 유지되었죠.

B: 면접에서는 단순히 개념만 설명하기보다,
실제로 왜 그 전략을 택했는지 말할 수 있어야 합니다.

B: 실무형 답변, 캐시 스탬피드로 자신 있게 어필해보세요.
"""

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

