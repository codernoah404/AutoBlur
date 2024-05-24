import cv2
import numpy as np

def rect_blur(box, origin_pic):
    left_x = int(box.xyxy.tolist()[0][0])
    left_y = int(box.xyxy.tolist()[0][1])
    right_x = int(box.xyxy.tolist()[0][2])
    right_y = int(box.xyxy.tolist()[0][3])
    
    face = origin_pic[left_y:right_y, left_x:right_x]
    
    origin_pic[left_y:right_y, left_x:right_x] = cv2.blur(face, (40, 40))
    
    return origin_pic


def ellipse_blur(box, origin_pic):
    left_x = int(box.xyxy.tolist()[0][0])
    left_y = int(box.xyxy.tolist()[0][1])
    right_x = int(box.xyxy.tolist()[0][2])
    right_y = int(box.xyxy.tolist()[0][3])
    
    # 타원형 중심과 축 길이 계산
    center_x = (left_x + right_x) // 2
    center_y = (left_y + right_y) // 2
    axis_major = (right_x - left_x) // 2
    axis_minor = (right_y - left_y) // 2
    
    # 타원형 마스크 생성
    mask = np.zeros_like(origin_pic)
    cv2.ellipse(mask, (center_x, center_y), (axis_major, axis_minor), 0, 0, 360, (255, 255, 255), -1)
    
    # 원본 이미지 * 타원형 영역 -> 얼굴
    face_with_ellipse = cv2.bitwise_and(origin_pic, mask)
    blurred_face = cv2.blur(face_with_ellipse, (40, 40))
    
    # !(타원형 마스크)
    inverse_mask = cv2.bitwise_not(mask)
    
    # 원본 이미지 * !(타원형 마스크) -> 배경
    background = cv2.bitwise_and(origin_pic, inverse_mask)
    result_image = cv2.add(blurred_face, background)
    
    return result_image