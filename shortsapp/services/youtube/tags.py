import yake
import nltk
from konlpy.tag import Okt
from nltk.corpus import stopwords

# 불용어 다운로드 (처음 한번만)
nltk.download("stopwords", quiet=True)

okt = Okt()

KOREAN_STOP_WORDS = [
    "의",
    "가",
    "이",
    "은",
    "는",
    "을",
    "를",
    "에",
    "에서",
    "과",
    "와",
    "으로",
    "로",
    "도",
    "만",
    "의해",
    "에게",
    "한테",
    "께서",
    "그",
    "저",
    "이것",
    "그것",
    "저것",
    "이런",
    "저런",
    "그런",
    "있다",
    "되다",
    "하다",
]


def extract_keywords(text, max_tags=10, lang="ko"):
    # 불용어 목록 로드 (한글은 별도 정의)
    if lang == "en":
        stop_words = set(stopwords.words("english"))
    elif lang == "ko":
        stop_words = set(KOREAN_STOP_WORDS)
    else:
        stop_words = set()

    # YAKE 설정
    kw_extractor = yake.KeywordExtractor(
        lan=lang,
        n=1,  # 단어 단위 추출
        dedupLim=0.9,  # 중복 제거 임계값
        top=max_tags * 3,  # 최대 추출 개수 (태그 수의 3배)
        features=None,  # 기본 설정 사용
        stopwords=stop_words,  # 불용어 적용
    )

    # 키워드 추출
    raw_keywords = kw_extractor.extract_keywords(text)

    # 🔍 명사 필터링 (한글일 때만)
    if lang == "ko":
        candidate_keywords = []
        for word, score in raw_keywords:
            nouns = okt.nouns(word)
            for noun in nouns:
                if noun not in stop_words and len(noun) > 1:
                    candidate_keywords.append((noun, score))
    else:
        candidate_keywords = [
            (word, score)
            for word, score in raw_keywords
            if word.lower() not in stop_words
        ]

    # 🔽 중복 제거 + 점수 기준 정렬
    seen = set()
    filtered = []
    for word, score in sorted(candidate_keywords, key=lambda x: x[1]):
        if word not in seen:
            filtered.append(word)
            seen.add(word)
        if len(filtered) >= max_tags:
            break

    return filtered
