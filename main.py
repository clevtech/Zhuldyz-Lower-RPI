import numpy as np
import cv2
from Webcam import Webcam
from Commander import Commander


def gamma_correction(frame, power):
    frame = frame / 255.0
    frame = cv2.pow(frame, power)
    return np.uint8(frame * 255)


def process_frame(frame):
    gamma_frame = gamma_correction(frame, 3)
    gray_frame = cv2.cvtColor(gamma_frame,cv2.COLOR_BGR2GRAY)
    unfloor_mask = cv2.inRange(gray_frame, 100, 255)
    light_frame = cv2.bitwise_and(frame, frame, mask=unfloor_mask)
    edges_frame = cv2.Canny(light_frame,50,150,apertureSize = 3)
    lines = cv2.HoughLines(edges_frame,1,np.pi/180,40)
    if lines is not None:
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 - 1000 * b)
            y1 = int(y0 + 1000 * a)
            x2 = int(x0 + 1000 * b)
            y2 = int(y0 - 1000 * a)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        return rho, theta
    return None


camera = Webcam()
commander = Commander()
lower_bound = np.array([0, 128, 0])
upper_bound = np.array([255, 255, 128])
width_range = (int(0.4 * camera.width), int(0.6 * camera.width))
height1_range = (int(0 * camera.height), int(0.33 * camera.height))
height2_range = (int(0.33 * camera.height), int(0.67 * camera.height))
height3_range = (int(0.67 * camera.height), int(1 * camera.height))
cm_per_pixel = 12 / height1_range[1]


while True:
    frame = camera.get_current_frame()
    upper_frame = frame[height1_range[0]:height1_range[1], width_range[0]:width_range[1]].copy()
    middle_frame = frame[height2_range[0]:height2_range[1], width_range[0]:width_range[1]].copy()
    lower_frame = frame[height3_range[0]:height3_range[1], width_range[0]:width_range[1]].copy()
    cv2.rectangle(frame, (width_range[0], height1_range[0]), (width_range[1], height1_range[1]), (0, 255, 0), 1)
    cv2.rectangle(frame, (width_range[0], height2_range[0]), (width_range[1], height2_range[1]), (0, 255, 0), 1)
    cv2.rectangle(frame, (width_range[0], height3_range[0]), (width_range[1], height3_range[1]), (0, 255, 0), 1)
    line_info = [process_frame(upper_frame), process_frame(middle_frame), process_frame(lower_frame)]
    line_info = [(index, info) for index, info in enumerate(line_info) if info is not None]
    line_info = None if line_info == [] else line_info[0]
    print(line_info)
    cv2.imshow('mainframe', frame)
    cv2.imshow('upperframe', upper_frame)
    cv2.imshow('middleframe', middle_frame)
    cv2.imshow('lowerframe', lower_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
