from moviepy.editor import AudioFileClip, concatenate_videoclips, concatenate_audioclips
from gtts import gTTS
import os
from .splitter import split_script_by_sentences
from .video_clip import create_slide_clip
from .cleaner import delete_temp_files
import re

# 스크립트를 처리하여 동영상을 생성합니다.
def process_script(script, image_paths, font_color="white", font_size="medium", speaker_settings=None):
    print("🎙️ 화자별 음성 설정:", speaker_settings)
    print("🔨 영상 생성 중...")
    for path in image_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"이미지 경로 없음: {path}")
    
    # 1. 스크립트를 여러 부분으로 나눕니다.
    lines = split_script_by_sentences(script)  
    clips = []
    audio_clips = []
    
 
    for idx, line in enumerate(lines):
        # 🧠 화자 구분 (예: A: ~~)
        match = re.match(r'^([A-Z]):\s*(.+)', line)
        if match:
            speaker, content = match.groups()
        else:
            speaker, content = 'A', line  # 기본값

        voice_info = speaker_settings.get(speaker, {'lang': 'ko', 'gender': 'female'})

        # 🗣️ 개별 gTTS 생성
        tts = gTTS(text=content, lang=voice_info['lang'])  # gender 사용 불가 (gTTS 제한)
        audio_path = f"media/audio_line_{idx}.mp3"
        tts.save(audio_path)
        audio_clip = AudioFileClip(audio_path)
        audio_clips.append(audio_clip)

        # 🎞️ 영상 클립
        image_idx = idx % len(image_paths)
        video_clip = create_slide_clip(
            content,
            image_path=image_paths[image_idx],
            duration=audio_clip.duration,
            font_size=font_size_to_points(font_size),
            font_color=font_color
        )
        clips.append(video_clip.set_duration(audio_clip.duration))
    
    # 5. 모든 클립을 합칩니다.
    
    # 🔊 오디오 클립 하나로 합치기
    final_audio = concatenate_audioclips(audio_clips)
    final_video = concatenate_videoclips(clips, method="compose")

    # 🔁 영상 길이와 오디오 길이를 강제로 일치시킴
    final_video = final_video.set_duration(final_audio.duration).set_audio(final_audio)

    video_path = "media/final_video.mp4"
    final_video.write_videofile(
        video_path,
        fps=15,
        codec="libx264",
        audio_codec="aac",
        bitrate="1200k", 
        threads=4,
        preset="ultrafast",  # ✅ 렌더링 속도 최우선
        temp_audiofile="media/temp-audio.m4a",  # 임시 파일 경로 지정
        remove_temp=True,
    )

    print("✅ 영상 생성 완료!")

    # 임시 파일 삭제
    delete_temp_files()

    return video_path

# 글자 크기를 포인트로 변환합니다.
def font_size_to_points(size):
    if size == 'small':
        return 20
    elif size == 'medium':
        return 30
    elif size == 'large':
        return 40
    else:
        raise ValueError("Invalid font size")


            
