from moviepy.editor import AudioFileClip, concatenate_videoclips, concatenate_audioclips
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
    progress_session=None,
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
            speaker, {"lang": "ko-KR", "gender": "FEMALE", "voice": "ko-KR-Wavenet-A", "speaking_rate": 1.3}
        )

        audio_path = synthesize_speech(
            text=content,
            lang_code=voice_info["lang"],
            gender=voice_info["gender"],
            voice_name=voice_info["voice"],
            speaking_rate=voice_info.get("speaking_rate", 1.3),
        )
        time.sleep(0.5)
        temp_audio_paths.append(audio_path)

        audio_clip = AudioFileClip(audio_path)
        audio_clips.append(audio_clip)

        if progress_session:
            progress_session["progress"] = int(30 * (idx + 1) / len(lines))
            progress_session.modified = True

    final_audio = concatenate_audioclips(audio_clips)
    total_audio_duration = final_audio.duration
    image_change_interval = total_audio_duration / len(image_paths)

    # 3️⃣ 영상 클립 생성
    elapsed_time = 0
    for idx, ((speaker, content), audio_clip) in enumerate(zip(lines, audio_clips)):
        clean_content = re.sub(r"^[A-Z]:\s*", "", content)
        image_idx = min(int(elapsed_time // image_change_interval), len(image_paths) - 1)

        video_clip = create_slide_clip(
            clean_content,
            image_path=image_paths[image_idx],
            duration=audio_clip.duration,
            font_size=font_size_to_points(font_size),
            font_color=font_color,
            title_text=title_text if title_text else "",
        )

        clips.append(video_clip.set_duration(audio_clip.duration))
        elapsed_time += audio_clip.duration

        if progress_session:
            progress_session["progress"] = 30 + int(40 * (idx + 1) / len(lines))
            progress_session.modified = True

    final_video = concatenate_videoclips(clips, method="compose").set_audio(final_audio)

    if progress_session:
        progress_session["progress"] = 90
        progress_session.modified = True

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

    # 최종 진행률 100%
    if progress_session:
        progress_session["progress"] = 100
        progress_session.modified = True

    # 7️⃣ 임시 파일 정리
    delete_temp_files()
    for path in temp_audio_paths:
        if os.path.exists(path):
            os.remove(path)

    return video_path

def font_size_to_points(size):
    sizes = {"small": 30, "medium": 35, "large": 40}
    if size in sizes:
        return sizes[size]
    raise ValueError("Invalid font size")
