import cv2
import numpy as np


def findline():
    cap = cv2.VideoCapture(0)
    cap.set(3, 400) #WIDTH
    cap.set(4, 200) #HEIGHT

    ret, frame = cap.read()
    cv2.imshow('mainwindow', frame)
    img = frame
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    minLineLength = 200
    maxLineGap = 0
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
    try:
        for x1,y1,x2,y2 in lines[0]:
            line = lines[0][0]
    except:
        line = None

    cap.release()
    return line



while True:
    line = findline()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if line!=None:
        if line[1]>line[3]:
            print("Turn left")
        elif line[3]>line[1]:
            print("Turn right")
        if line[1]==line[3]:
            print("Forward")
    else:
        print("no line")
        

