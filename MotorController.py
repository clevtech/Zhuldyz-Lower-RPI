import time
from gpiozero import LED
import math

class MotorController:
    def __init__(self):
        self.task = None
        self.right_motor = (LED(20), LED(21))
        self.left_motor = (LED(24), LED(23))
        self.position = None
        self.task = None
        self.bc_tr = False
        
    def receive_state(self, rho, theta):
        if self.task == 'Stop': self._stop()
        elif self.task == 'Align':
            self._align(theta)
            self.task = None
        elif self.task == 'A-B':
            if rho > 900:
                self.position = 'B'
                self.task = None
                self._stop()
            else:
                self._forward(theta)
        elif self.task == 'B-C':
            if rho > 900:
                if self.bc_tr:
                    self.position = 'C'
                    self.task = None
                    self._stop()
                else:
                    self._turn_left(135)
                    time.sleep(1)
                    self._forward(theta)
                    time.sleep(3)
                    self._turn_right(45)
                    time.sleep(1)
                    self.bc_tr = True
        elif self.task == 'C-D':
            if rho < 900:
                self._forward(theta)
            else:
                self._forward(theta)
                time.sleep(0.7)
                self._turn_right(90)
                self._forward(theta)
                time.sleep(2.5)
                self._stop()
                self.position = 'D'
                self.task = None
        elif self.task == 'D-E':
            if rho > 900:
                self.position = 'E'
                self.task = None
                self.stop()
            else:
                self._forward(theta)
                
    def _forward(self, theta):
        thresh = 0.07
        if theta < 1.57 - thresh:
            self.left_motor[0].off()
            self.left_motor[1].off()
            self.right_motor[0].off()
            self.right_motor[1].on()
            time.sleep(0.02)
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].off()
            self.right_motor[1].on()
        elif theta > 1.57 + thresh:
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].off()
            self.right_motor[1].off()
            time.sleep(0.02)
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].off()
            self.right_motor[1].on()
        else:
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].off()
            self.right_motor[1].on()
        
    def _backward(self):
        self.left_motor[0].on()
        self.left_motor[1].off()
        self.right_motor[0].on()
        self.right_motor[1].off()
        
    def _stop(self):
        self.left_motor[0].off()
        self.left_motor[1].off()
        self.right_motor[0].off()
        self.right_motor[1].off()
        
    def _turn_left(self, degree):
        self.left_motor[0].on()
        self.left_motor[1].off()
        self.right_motor[0].off()
        self.right_motor[1].on()
        if degree == 90:
            time.sleep(0.6)
        elif degree == 45:
            time.sleep(0.31)
        elif degree == 135:
            time.sleep(0.874)
        self.left_motor[0].off()
        self.left_motor[1].off()
        self.right_motor[0].off()
        self.right_motor[1].off()
        
    def _turn_right(self, degree):
        self.left_motor[0].off()
        self.left_motor[1].on()
        self.right_motor[0].on()
        self.right_motor[1].off()
        if degree == 90:
            time.sleep(0.66)
        elif degree == 45:
            time.sleep(0.4)
        self.left_motor[0].off()
        self.left_motor[1].off()
        self.right_motor[0].off()
        self.right_motor[1].off()
#    def _stop(self):
if __name__ == '__main__':
    controller = MotorController()
    controller._turn_right(45)
        