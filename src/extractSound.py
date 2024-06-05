#만일 mac os를 사용하고 있지 않다면 다음 두 줄의 명령어는 제거하십시오.
#mac os를 사용한다면 brew 명령어로 ffmpeg를 설치하고 위치를 지정하십시오
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/bin/ffmpeg"

from moviepy.editor import VideoFileClip

def audio(video_src_path, video_path, fps):
    try:
        audio = VideoFileClip(video_src_path).audio
        video = VideoFileClip(video_path)
        
        videoWithsound = video.set_audio(audio)

        new_videoPath = "../BluredVideo/[blur]" + video_path.split("]")[1]
        videoWithsound.write_videofile(new_videoPath, fps =fps, codec='libx264', audio_codec='aac')
    except Exception as e:
        print(f"Error: {e}")