import tkinter as tk
from tkinter import filedialog
import cv2
import PIL.Image, PIL.ImageTk
import os
from model import LoadModel

class VideoApp:
    def __init__(self, window, window_title):
        self.model, self.mps = LoadModel()
        if ("BluredVideo" in os.listdir(".")):
            pass
        else:
            os.mkdir("./BluredVideo") # 저장될 디렉터리
            
        self.window = window
        self.window.title(window_title)
        
        self.video_source = None
        
        self.canvas = tk.Canvas(window)
        self.canvas.pack()
        
        self.btn_open = tk.Button(window, text="Open Video", width=15, command=self.open_video)
        self.btn_open.pack(anchor=tk.CENTER, expand=True)
        
        self.delay = 15
        self.window.mainloop()
        


    def open_video(self):
        self.video_source = filedialog.askopenfilename()
        if self.video_source:
            self.vid = cv2.VideoCapture(self.video_source)
            
            self.fps = round(self.vid.get(cv2.CAP_PROP_FPS))
            self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            self.saveVideo = cv2.VideoWriter("../BluredVideo/[blur]" + self.video_source.split('/')[-1], # 저장 경로 
                                        self.fourcc, self.fps, (round(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                                    round(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))))
            self.retval, self.frame = self.vid.read()

            self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            self.save()

    def save(self):
        retval, frame = self.vid.read()
        
        while(True):
            if not(retval):	# 프레임정보를 정상적으로 읽지 못하면
                break  # while문을 빠져나가기
            
            else:
                if (self.mps):
                    results = self.model(frame, device='mps')
                else:
                    results = self.model(frame)
                boxes = results[0].boxes
                
                for box in boxes:
                    left_x = int(box.xyxy.tolist()[0][0])
                    left_y = int(box.xyxy.tolist()[0][1])
                    right_x = int(box.xyxy.tolist()[0][2])
                    right_y = int(box.xyxy.tolist()[0][3])
                    
                    face = frame[left_y:right_y, left_x:right_x]
                    
                    frame[left_y:right_y, left_x:right_x] = cv2.blur(face, (40, 40))
                    self.saveVideo.write(frame)
    
        if self.vid.isOpened():	# 영상 파일(카메라)이 정상적으로 열렸는지(초기화되었는지) 여부
            self.vid.release()	# 영상 파일(카메라) 사용을 종료
            self.saveVideo.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoApp(root, "Video Player")
    root.mainloop()
