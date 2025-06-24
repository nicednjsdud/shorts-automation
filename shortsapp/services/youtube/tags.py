import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# english stop words
import nltk
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# korean stop words
from konlpy.tag import Okt
okt = Okt()


def extract_keywords(text, max_tags=15):
    if not text:
        return []
    # 공통 전처리
    text = text.lower()  # 소문자로 변환

    # 영어 처리리
    words_en = word_tokenize(text)  # 영어 토큰화
    words_en = [w for w in words_en if w.isalpha()]
    words_en = [w for w in words_en if w not in stopwords.words("english")]

    # 한글 처리
    words_ko = okt.nouns(text)  # 한글 형태소 분석
    stopwords_ko = ["영상"] # 한글 불용어
    words_ko = [w for w in words_ko if len(w) > 1 and w not in stopwords_ko]


    # 합치고 가장 많이 나온 단어 추출
    all_words = words_en + words_ko
    most_common = Counter(all_words).most_common(max_tags)

    return [word for word, _ in most_common] 