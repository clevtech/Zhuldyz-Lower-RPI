import numpy as np
import cv2
from Webcam import Webcam
from MotorController import MotorController


def gamma_correction(frame, power):
    frame = frame / 255.0
    frame = cv2.pow(frame, power)
    return np.uint8(frame * 255)


def process_frame(frame):
    lower_bound = np.array([30, 70, 200])
    upper_bound = np.array([180, 230, 255])
    gamma_frame = gamma_correction(frame, 3)
    gray_frame = cv2.cvtColor(gamma_frame,cv2.COLOR_BGR2GRAY)
    unfloor_mask = cv2.inRange(gray_frame, 50, 200)
    light_frame = cv2.bitwise_and(frame, frame, mask=unfloor_mask)
    color_mask = cv2.inRange(light_frame, lower_bound, upper_bound)
    line_frame = cv2.bitwise_and(light_frame, light_frame, mask=color_mask)
    edges_frame = cv2.Canny(line_frame,50,150,apertureSize = 3)
    lines = cv2.HoughLines(edges_frame,1,np.pi/180,130)
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
        return (rho, theta), line_frame
    return (1000, 1000), line_frame

camera = Webcam()
control = MotorController(camera.height)
control.position = 'A'
##tasks = ['A-B', 'B-C', 'C-D', 'D-E']
##index = 0
##control.set_task(tasks[index])
control.set_task('D-B')


while True:
##    if control.task is None:
##        index += 1
##        control.set_task(tasks[index])
    frame = camera.get_current_frame()
    line_info, processed_frame = process_frame(frame)
    cv2.imshow('procframe', processed_frame)
    cv2.imshow('mainframe', frame)
    control.receive_state(line_info[0], line_info[1])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

