from pytube import YouTube
import os
def download_video(url, path="../Video/"):
    try:
        if ("Video" in os.listdir("..")):
            pass
        else:
            os.mkdir("../Video") # 저장될 디렉터리
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=path)
        print("다운로드 완료 필요시 파일명을 바꾸십시오.")
        
    except Exception as e:
        print(f"Error: {e}")
        
        

# if __name__ == "__main__":
#     download_video("https://www.youtube.com/[URL you want]")