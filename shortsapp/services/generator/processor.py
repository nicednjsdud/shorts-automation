from moviepy.editor import AudioFileClip, concatenate_videoclips, concatenate_audioclips
from gtts import gTTS
import os
from .splitter import split_script_by_sentences
from .video_clip import create_slide_clip
from .cleaner import delete_temp_files
from .tts_google import synthesize_speech
import re

# 스크립트를 처리하여 동영상을 생성합니다.
def process_script(script, image_paths, font_color="white", font_size="medium", speaker_settings=None):
    print("🔨 영상 생성 중...")
    for path in image_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"이미지 경로 없음: {path}")
    
    # 1. 스크립트를 여러 부분으로 나눕니다.
    lines = split_script_by_sentences(script)  
    clips = []
    audio_clips = []
    
    current_speaker = 'A'  # 기본 화자
    temp_audio_paths = [] # 오디오 총 길이를 알기위한 temp

    for idx, line in enumerate(lines):
        # 🧠 화자 구분 (예: A: ~~)
        match = re.match(r'^([A-Z]):\s*(.+)', line)
        if match:
            speaker, content = match.groups()
            current_speaker = speaker
        else:
            content = line
            speaker = current_speaker  # 이전 화자 유지


        voice_info = speaker_settings.get(speaker, {
            'lang': 'ko-KR',
            'gender': 'FEMALE',
            'voice': 'ko-KR-Wavenet-A'
        })

        # 🗣️ 개별 gTTS 생성
        # tts = gTTS(text=content, lang=voice_info['lang'])
        # audio_path = f"media/audio_line_{idx}.mp3"
        # tts.save(audio_path)

        # 🔊 Google TTS 사용
        audio_path = synthesize_speech(
            text=content,
            lang_code=voice_info['lang'],  # 언어 코드
            gender=voice_info['gender'],
            voice_name=voice_info['voice'],
            
        )
        temp_audio_paths.append(audio_path)

        audio_clip = AudioFileClip(audio_path)
        audio_clips.append(audio_clip)

    # 🔊 오디오 클립 하나로 합치기 (합치기 전 총 길이 계산)
    final_audio = concatenate_audioclips(audio_clips)
    total_audio_duration = final_audio.duration
    image_change_interval = total_audio_duration / len(image_paths)

    # 🎞️ 영상 클립 생성
    elapsed_time = 0
    for idx, (line, audio_clip) in enumerate(zip(lines, audio_clips)):
        content = re.sub(r'^[A-Z]:\s*', '', line)  # 자막에서 화자 제거
        image_idx = int(elapsed_time // image_change_interval)
        image_idx = min(image_idx, len(image_paths) - 1)  # index overflow 방지

        video_clip = create_slide_clip(
            content,
            image_path=image_paths[image_idx],
            duration=audio_clip.duration,
            font_size=font_size_to_points(font_size),
            font_color=font_color
        )
        clips.append(video_clip.set_duration(audio_clip.duration))
        elapsed_time += audio_clip.duration
 
    # 🔁 오디오와 영상 결합
    final_video = concatenate_videoclips(clips, method="compose")
    final_video = final_video.set_duration(final_audio.duration).set_audio(final_audio)

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


            
