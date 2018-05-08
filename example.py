import cv2
import numpy as np
import sys
import re

def houghCircles(img):
	img = cv2.medianBlur(img, 5)
	cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
	
	if ((re.compile("3*")).match(cv2.__version__)):
		circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 
				1, 20,param1=70,param2=50,minRadius=0, maxRadius=0)
	else:
		circles = cv2.HoughCircles(img, cv2.cv.CV_HOUGH_GRADIENT, 
				1, 20,param1=70,param2=50,minRadius=0, maxRadius=0)

	if(circles!=None):
		circles = np.uint16(np.around(circles))
		for i in circles[0,:]:
		    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
		    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
	return cimg

def eulerToCoordinateTransform(line):
	for rho, theta in line:
		a = np.cos(theta)
		b = np.sin(theta)
		x0 = a*rho
		y0 = b*rho
		x1 = int(x0 + 1000*(-b))
		y1 = int(y0 + 1000*(a))
		x2 = int(x0 - 1000*(-b))
		y2 = int(y0 - 1000*(a))
	return [(x1,y1),(x2,y2)]

def getIntersection(line_1, line_2):
	line1 = eulerToCoordinateTransform(line_1)
	line2 = eulerToCoordinateTransform(line_2)
	
	s1 = np.array(line1[0])
	e1 = np.array(line1[1])

	s2 = np.array(line2[0])
	e2 = np.array(line2[1])

	a1 = (s1[1] - e1[1]) / (s1[0] - e1[0])
	b1 = s1[1] - (a1 * s1[0])

	a2 = (s2[1] - e2[1]) / (s2[0] - e2[0])
	b2 = s2[1] - (a2 * s2[0])

	if abs(a1 - a2) < sys.float_info.epsilon:
		return False

	x = (b2 - b1) / (a1 - a2)
	y = a1 * x + b1
	return (x, y)

def houghLines(img):
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)

	lines = cv2.HoughLines(edges, 1.75, np.pi/180,150)

	if lines!=None:

		for line in lines:
			for rho,theta in line:
				line_transform = eulerToCoordinateTransform(line)
				cv2.line(img,line_transform[0],line_transform[1],(0,0,255),2)

		for i in range(len(lines)):
			for j in range(i+1,len(lines)):
				if getIntersection(lines[i], lines[j]):
					center = getIntersection(lines[i], lines[j])
					cv2.circle(img,(center[0],center[1]),2,(0,255,0),3)
	return img
	
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    cap.set(3, 200)
    cap.set(4, 100)

    if not cap.isOpened():
		print('Exiting with state 1...')
		exit(1)
    while(True):
		ret, frame = cap.read()
		if not ret:
			break
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		houghCircleImage = houghCircles(gray)
		houghLineImage = houghLines(houghCircleImage)

		cv2.imshow('Circles and Lines', houghLineImage)	

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

    cv2.waitKey(0)
    cv2.destroyAllWindows()