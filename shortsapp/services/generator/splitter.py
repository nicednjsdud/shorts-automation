import re

def split_script_by_sentences(script):
    """
    화자 기준으로 문단을 묶어 (화자, 전체 문장) 튜플 리스트 반환
    """
    lines = script.strip().split("\n")
    results = []
    current_speaker = None
    buffer = []

    for line in lines:
        if not line.strip():
            continue  # 공백 줄 무시

        match = re.match(r'^([A-Z]):\s*(.*)', line.strip())
        if match:
            if current_speaker and buffer:
                # 이전 화자 블록 저장
                results.append((current_speaker, " ".join(buffer)))
                buffer = []
            current_speaker, content = match.groups()
            buffer.append(content)
        else:
            # 동일 화자일 경우 다음 줄 계속 추가
            buffer.append(line.strip())

    # 마지막 화자 블록 저장
    if current_speaker and buffer:
        results.append((current_speaker, " ".join(buffer)))

    return results
