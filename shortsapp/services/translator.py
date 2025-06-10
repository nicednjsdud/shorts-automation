from googletrans import Translator

# 영어 번역 서비스
# 이 서비스는 Google Translate API를 사용하여 한국어를 영어로 번역합니다.
# 사용하려면 googletrans 라이브러리를 설치해야 합니다.
# 설치 방법: pip install googletrans==4.0.0-rc1
def translate_to_english(text : str):
    translator = Translator()
    result = translator.translate(text, src='ko', dest='en')
    return result.text