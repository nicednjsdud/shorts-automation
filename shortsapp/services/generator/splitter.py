import re

# 마침표, 물음표, 느낌표, 큰따옴표 등으로 문장을 분할합니다.
#  단, 줄바꿈 문자도 함께 고려합니다.
def split_script_by_sentences(script):

    pattern = r'(?<=[.!?\"\”])\s+'
    sentences = re.split(pattern, script)
    return [s.strip() for s in sentences if s.strip()]