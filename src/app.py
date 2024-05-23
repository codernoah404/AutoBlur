import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, simpledialog
import cv2
import PIL.Image, PIL.ImageTk
import os
from model import LoadModel
from tkinter import DoubleVar
from dwnloadVdio import download_video
from extractSound import audio

class VideoApp:
    def __init__(self, window, window_title):
        self.model, self.mps = LoadModel()
        if ("BluredVideo" in os.listdir(".")):
            pass
        else:
            os.mkdir("./BluredVideo") # 저장될 디렉터리
            
        self.window = window
        self.window.title(window_title)
        
        
        la = tk.Label(root, text = "Progress...\n")
        la.config(font =("Courier", 14)) 
        la.pack(anchor="sw")
        
        self.video_source = None
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProgressbar", background="green", thickness=25)  # 색상 및 굵기 설정
        
        self.p_var = DoubleVar()
        self.progressbar = ttk.Progressbar(window, style="TProgressbar", maximum=100, length=150, variable=self.p_var)
        self.progressbar.pack()
        
        self.btn_open = tk.Button(window, text="Open Video", width=15, command=self.open_video)
        self.btn_open.pack(anchor=tk.CENTER, expand=True)
        
        self.btn_DownLoad = tk.Button(window, text="DownLoad Video", width=15, command=self.downLoad_video)
        self.btn_DownLoad.pack(anchor=tk.CENTER, expand=True)
        
        self.btn_interrupt = tk.Button(window, text="Stop Blurring", width=15, command=self.stop_interrupt)
        self.btn_interrupt.pack(anchor=tk.CENTER, expand=True)
        
        self.delay = 15
        self.window.mainloop()
        
        
    def open_video(self):
        self.video_source = filedialog.askopenfilename()
        self.savePoint = "./BluredVideo/[blur]" + self.video_source.split('/')[-1]
        if self.video_source:
            self.vid = cv2.VideoCapture(self.video_source)
            self.fps = round(self.vid.get(cv2.CAP_PROP_FPS))
            self.total_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
            self.progressbar.config(maximum=self.total_frames)
            
            self.fourcc = cv2.VideoWriter_fourcc(*'X264') # *'DIVX'
            self.saveVideo = cv2.VideoWriter(self.savePoint, # 저장 경로 
                                        self.fourcc, self.fps, (round(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                                    round(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))

            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            self.save()

    def save(self):
        kwargs = {
            'stream': True,
            'verbose': False,
            'show_labels': False
        }

        if self.mps:
            kwargs['device'] = 'mps'
            
        results = self.model(self.video_source, **kwargs)
        for progress, result in enumerate(results):
            ori = result.orig_img
            for box in result.boxes:
                        left_x = int(box.xyxy.tolist()[0][0])
                        left_y = int(box.xyxy.tolist()[0][1])
                        right_x = int(box.xyxy.tolist()[0][2])
                        right_y = int(box.xyxy.tolist()[0][3])
                        
                        face = ori[left_y:right_y, left_x:right_x]
                        
                        ori[left_y:right_y, left_x:right_x] = cv2.blur(face, (40, 40))
            
            self.saveVideo.write(ori)
            self.p_var.set(progress)
            self.window.update_idletasks()
    
        if self.vid.isOpened():	# 영상 파일(카메라)이 정상적으로 열렸는지(초기화되었는지) 여부
            self.vid.release()	# 영상 파일(카메라) 사용을 종료
            self.saveVideo.release()
            
        audio(self.video_source, self.savePoint, self.fps)
        
        
            
    def downLoad_video(self):
        self.url = simpledialog.askstring(title = "원하시는 영상의 URL을 입력하세요",
                                    prompt = "https://www.youtube.com/[URL you want]:")
        self.savePoint = filedialog.askdirectory()
        
        kwargs = {
            'url': self.url,
        }

        if self.savePoint != "":
            kwargs['path'] = self.savePoint
            
        download_video( **kwargs )
    
    def stop_interrupt(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root, "AutoBlur")
    root.mainloop()
