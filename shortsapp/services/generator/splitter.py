import re

def split_script_by_sentences(script):
    """
    입력 스크립트를 화자별 문장으로 나누어 [(화자, 문장)] 형태로 반환
    예: A: 안녕하세요. 오늘 날씨 좋네요! → [('A', '안녕하세요.'), ('A', '오늘 날씨 좋네요!')]
    """
    result = []
    current_speaker = 'A'  # 기본값

    # 줄 단위로 분할
    lines = script.strip().splitlines()

    # 문장 단위 정규표현식 (마침표, 느낌표, 물음표, 큰따옴표 뒤에서 분리)
    sentence_splitter = re.compile(r'(?<=[.!?\"\”])\s+')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 화자 구분 (예: A: 내용)
        match = re.match(r'^([A-Z]):\s*(.+)', line)
        if match:
            speaker, content = match.groups()
            current_speaker = speaker
        else:
            content = line
            speaker = current_speaker

        # 문장 단위로 다시 분할
        sentences = sentence_splitter.split(content)
        for sentence in sentences:
            if sentence.strip():
                result.append((speaker, sentence.strip()))

    return result
