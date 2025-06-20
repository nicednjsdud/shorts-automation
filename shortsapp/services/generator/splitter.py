import re

import re

def split_script_by_sentences(script):
    """
    스크립트를 화자 + 문장 단위로 분리합니다.
    줄바꿈(\n), 마침표(.), 물음표(?), 느낌표(!) 등 기준으로 쪼갬.
    결과: [("A", "문장1"), ("A", "문장2"), ("B", "문장3"), ...]
    """
    results = []
    current_speaker = "A"  # 기본 화자

    # 줄 단위로 처리
    lines = script.strip().splitlines()

    for line in lines:
        # 화자 추출 (예: A: 내용)
        match = re.match(r"^([A-Z]):\s*(.*)", line)
        if match:
            speaker, content = match.groups()
            current_speaker = speaker
        else:
            content = line.strip()

        # 문장 단위로 쪼개기 (마침표, 물음표, 느낌표 + \n 포함)
        # ⚠️ 정규식에서 lookbehind와 split 사용
        sentences = re.split(r'(?<=[.?!])\s+|\n+', content)
        for sentence in sentences:
            clean = sentence.strip()
            if clean:
                results.append((current_speaker, clean))

    return results

