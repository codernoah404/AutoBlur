from ultralytics import YOLO
import torch

def LoadModel(model_path='./model/yolov8m-face.pt'): #에러문 추가하기
    model = YOLO(model_path)
    mps = torch.backends.mps.is_available() #for m1 mac
    
    return model, mps

