from moviepy.editor import VideoFileClip

def audio(video_src_path, video_path, fps):
    try:
        audio = VideoFileClip(video_src_path).audio
        video = VideoFileClip(video_path)
        
        videoWithsound = video.set_audio(audio)

        new_videoPath = "./BluredVideo/[blur]" + video_path.split("]")[1]
        videoWithsound.write_videofile(new_videoPath, fps =fps, codec='libx264', audio_codec='aac')
    except Exception as e:
        print(f"Error: {e}")

