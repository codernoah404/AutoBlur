from moviepy.editor import VideoFileClip

def extract_audio(video_path, output_audio_path, codec='libmp3lame'):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(output_audio_path, codec=codec)

        print(f"Audio extracted and saved to: {output_audio_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    video_path = input("Enter the path to the video file: ")
    output_audio_path = input("Enter the output path for the audio file (e.g., output.mp3): ")
    extract_audio(video_path, output_audio_path)
