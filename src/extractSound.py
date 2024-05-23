from moviepy.editor import VideoFileClip

def audio(video_src_path, video_path, fps):
    try:
        audio = VideoFileClip(video_src_path).audio
        video = VideoFileClip(video_path)
        
        videoWithsound = video.set_audio(audio)

        
        videoWithsound.write_videofile(video_path, fps =fps, codec='libx264', audio_codec='aac') # 여기서 문제 발생 ( 영상이 멈추는 오류 )
    except Exception as e:
        print(f"Error: {e}")

