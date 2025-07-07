from moviepy.editor import (
    AudioFileClip,
    AudioClip,
    concatenate_videoclips,
    concatenate_audioclips,
)
import os
import re
import time
import numpy as np

from .splitter import split_script_by_sentences
from .video_clip import create_slide_clip
from .cleaner import delete_temp_files
from .tts_google import synthesize_speech


def process_script(
    script,
    image_paths,
    font_color="white",
    font_size="medium",
    speaker_settings=None,
    title_text="",
):
    print("🔨 영상 생성 중...")

    # 🔍 이미지 경로 유효성 검사
    for path in image_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"이미지 경로 없음: {path}")

    # 1️⃣ 스크립트 문장 단위로 분할
    lines = split_script_by_sentences(script)
    if not lines:
        raise ValueError("스크립트에 문장이 없습니다.")

    clips = []
    audio_clips = []
    temp_audio_paths = []

    # 2️⃣ 각 문장에 대해 음성 생성 및 오디오 클립 준비
    for idx, (speaker, content) in enumerate(lines):

        # 🗣️ 화자 설정 불러오기
        voice_info = speaker_settings.get(
            speaker, {"lang": "ko-KR", "gender": "FEMALE", "voice": "ko-KR-Wavenet-A"}
        )

        # 🔊 Google TTS로 오디오 생성
        audio_path = synthesize_speech(
            text=content,
            lang_code=voice_info["lang"],
            gender=voice_info["gender"],
            voice_name=voice_info["voice"],
            speaking_rate=voice_info.get('speaking_rate', 1.3)
        )
        time.sleep(0.5)
        temp_audio_paths.append(audio_path)

        audio_clip = AudioFileClip(audio_path)
        audio_clips.append(audio_clip)

    # 3️⃣ 전체 오디오 길이 계산 및 이미지 전환 간격 설정
    # segments = [
    #     clip for pair in zip(audio_clips, [make_silence()] * len(audio_clips)) for clip in pair
    # ][:-1]  # 마지막 무음 제거
    final_audio = concatenate_audioclips(audio_clips)

    total_audio_duration = final_audio.duration
    image_change_interval = total_audio_duration / len(image_paths)

    # 4️⃣ 각 문장에 대응하는 영상 클립 생성 (시간 기준으로 이미지 할당)
    elapsed_time = 0
    for (speaker, content), audio_clip in zip(lines, audio_clips):
        clean_content = re.sub(r"^[A-Z]:\s*", "", content)
        image_idx = min(
            int(elapsed_time // image_change_interval), len(image_paths) - 1
        )

        video_clip = create_slide_clip(
            clean_content,
            image_path=image_paths[image_idx],
            duration=audio_clip.duration,
            font_size=font_size_to_points(font_size),
            font_color=font_color,
            title_text=(
                title_text if title_text else ""
            ),  # 타이틀 텍스트가 주어지면 전달
        )

        clips.append(video_clip.set_duration(audio_clip.duration))
        elapsed_time += audio_clip.duration

    # 5️⃣ 클립 합치고 오디오 연결
    final_video = concatenate_videoclips(clips, method="compose").set_audio(final_audio)

    # 6️⃣ 최종 영상 렌더링
    video_path = "media/final_video.mp4"
    final_video.write_videofile(
        video_path,
        audio=True,
        fps=15,
        codec="libx264",
        audio_codec="aac",
        bitrate="1200k",
        threads=4,
        preset="ultrafast",
        temp_audiofile="media/temp-audio.m4a",
        remove_temp=True,
    )

    print("✅ 영상 생성 완료!")

    # 7️⃣ 임시 자막 이미지 및 오디오 파일 정리
    delete_temp_files()
    for path in temp_audio_paths:
        if os.path.exists(path):
            os.remove(path)

    return video_path


# 글자 크기를 pt 단위로 변환
def font_size_to_points(size):
    sizes = {"small": 20, "medium": 30, "large": 40}
    if size in sizes:
        return sizes[size]
    raise ValueError("Invalid font size")


# 무음 오디오 클립 생성 함수
def make_silence(duration=0.2):
    return AudioClip(
        lambda t: np.zeros((1, 1)) if np.isscalar(t) else np.zeros((len(t), 1)),
        duration=duration,
        fps=44100,
    )
