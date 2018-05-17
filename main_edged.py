import numpy as np
import cv2
from Webcam import Webcam
from CommanderEdged import CommanderEdged
import math


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
    lines = cv2.HoughLines(edges_frame,1,np.pi/180,70)
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

def left_wheel(theta):
    if theta > 1.57: return 1.0
    return 0.636 * theta

def right_wheel(theta):
    if theta < 1.57: return 1.0
    return -0.636 * theta + 1.99

camera = Webcam()
lower_bound = np.array([0, 128, 0])
upper_bound = np.array([255, 255, 128])
width_range = (int(0.4 * camera.width), int(0.6 * camera.width))
height_range = (int(0 * camera.height), int(1 * camera.height))
map = {'A-B': ['l', 'l', 'l', 'l','l', 'l', 'l', 'l',
               'l', 'l', 'l', 'l','l', 'l', 'l', 'l',
               'l', 'l', 'l', 'l','l', 'l', 'l', 'l',
               'l', 'l', 'l', 'l','l', 'l', 'l', 'l',], 'B-C': ['l', 'r', 'l']}
cur_map = 'A-B'
cur_turn = 0
commander = CommanderEdged(map, camera.height)
current_task = 'angle'


while True:
    print(current_task)
    frame = camera.get_current_frame()
    important_frame = frame[height_range[0]:height_range[1], width_range[0]:width_range[1]].copy()
    cv2.rectangle(frame, (width_range[0], height_range[0]), (width_range[1], height_range[1]), (0, 255, 0), 1)
    line_info = process_frame(important_frame)
    if line_info is not None:
        if current_task == 'angle':
            commander.angle_calibration(line_info[1])
        if current_task == 'position':
            commander.position_calibration(line_info[0])
        if current_task == 'moving':
            commander.move()
    elif current_task == 'moving':
        commander.stop()
        try:
            commander.turn('r')
            #commander.turn(map[cur_map][cur_turn])
        except:
            print('suka')
            print(cur_turn)
        cur_turn += 1
        current_task == 'angle'
    if line_info is not None:
        if math.fabs(line_info[1] - 1.57) < 0.25: current_task = 'position'
        if math.fabs(line_info[0] - camera.height / 2) < 50:
            current_task = 'moving'
    cv2.imshow('mainframe', frame)
    cv2.imshow('importantframe', important_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


