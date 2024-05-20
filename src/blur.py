from ultralytics import YOLO


def LoadModel(model_path='./model/yolov8m-face.pt'): #에러문 추가하기
    model = YOLO(model_path)
    return model

