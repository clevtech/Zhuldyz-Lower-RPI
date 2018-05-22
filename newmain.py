import numpy as np
import cv2
from Webcam import Webcam
from MotorController import MotorController
from UpperHost import UpperHost


def gamma_correction(frame, power):
    frame = frame / 255.0
    frame = cv2.pow(frame, power)
    return np.uint8(frame * 255)


def process_frame(frame):
    lower_bound_color = np.array([0, 0, 100])
    upper_bound_color = np.array([100, 100, 255])
    lower_bound_floor = np.array([0,0,0])
    upper_bound_floor = np.array([150,150,150])
    gamma_frame = gamma_correction(frame, 5)
    unfloor_mask = cv2.inRange(gamma_frame, lower_bound_floor, upper_bound_floor)
    unfloor_mask = cv2.bitwise_not(unfloor_mask)
    light_frame = cv2.bitwise_and(gamma_frame, gamma_frame, mask=unfloor_mask)
    color_mask = cv2.inRange(light_frame, lower_bound_color, upper_bound_color)
    line_frame = cv2.bitwise_and(light_frame, light_frame, mask=color_mask)
    edges_frame = cv2.Canny(line_frame, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges_frame,1,np.pi/180,90)
    if lines is not None:
        for rho,theta in lines[0]:
            if not 1.2 < theta < 1.94:
                return (1000, 1000), line_frame
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
##tasks = ['ab', 'bc', 'cd', 'a']
##index = 0
##control.set_task(tasks[index])
#host = UpperHost()
control.set_task('ab')

while True:
    print(control.position)
    if control.task is None:
        _ = host.send('ok')
        cmd = host.read()
        control.set_task(cmd)
    frame = camera.get_current_frame()
    line_info, processed_frame = process_frame(frame)
    cv2.imshow('procframe', processed_frame)
    cv2.imshow('mainframe', frame)
    control.receive_state(line_info[0], line_info[1])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

