from moviepy.editor import AudioFileClip, concatenate_videoclips
from gtts import gTTS
import os
from .splitter import split_script_by_sentences
from .video_clip import create_slide_clip
from .cleaner import delete_temp_files


# 스크립트를 처리하여 동영상을 생성합니다.
def process_script(script, image_paths, font_color="white", font_size="medium"):
    print("🔨 영상 생성 중...")
    for path in image_paths:
        if not os.path.exists(path):
            raise FileNotFoundError(f"이미지 경로 없음: {path}")
    
    # 1. 스크립트를 여러 부분으로 나눕니다.
    lines = split_script_by_sentences(script)
    total_lines = len(lines)
    num_images = len(image_paths)
    
    # 2. TTS 전체 음성 생성
    tts = gTTS(text=script, lang='ko')
    audio_path = 'media/audio.mp3'
    tts.save(audio_path)
    audio = AudioFileClip(audio_path)

    # 3. 자막당 시간 계산
    segment_duration = audio.duration / total_lines if total_lines > 0 else 0
    print(f"⏱️ 자막당 시간: {segment_duration:.2f}초")

    # 4. 자막을 이미지에 균등 분배
    clips = []
    lines_per_image = max(1, total_lines // num_images)
    font_pt_size = font_size_to_points(font_size)
    for idx, line in enumerate(lines):
        image_idx = min(idx // lines_per_image, num_images - 1)
        image_path = image_paths[image_idx]

        clip = create_slide_clip(
            line,
            image_path=image_path,
            duration=segment_duration,
            font_size=font_pt_size,
            font_color=font_color
        )
        clips.append(clip)
    
    # 5. 모든 클립을 합칩니다.
    final_video = concatenate_videoclips(clips, method="compose")

    # 🔁 영상 길이와 오디오 길이를 강제로 일치시킴
    final_video = final_video.set_duration(audio.duration).set_audio(audio)

    video_path = "media/final_video.mp4"
    final_video.write_videofile(
        video_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        bitrate="1500k",
        threads=4,
        preset="medium"
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


            
