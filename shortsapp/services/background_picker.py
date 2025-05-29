
# 입력된 스타일 텍스트에 기반해 추천할 배경 영상/이미지 경로 반환
# - 실제 AI 분석 대신 키워드 매칭으로 시작
def suggest_backgrounds(style_prompt):
    style_prompt = style_prompt.lower()
    suggestions = []

    if "면접" in style_prompt or "비즈니스" in style_prompt:
        suggestions = ["office.mp4", "minimal.jpg"]
    elif "캐주얼" in style_prompt or "밝은" in style_prompt:
        suggestions = ["bright_cafe.mp4", "sunlight.jpg"]
    elif "테크" in style_prompt or "개발" in style_prompt:
        suggestions = ["code_bg.mp4", "tech_grid.jpg"]
    else:
        suggestions = ["default.jpg"]

    # media/static 내부 배경 자원 파일명 리스트 반환
    return suggestions
