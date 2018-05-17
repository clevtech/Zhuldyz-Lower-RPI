import time
from gpiozero import LED
import math

class MotorController:
    def __init__(self, camera_height):
        self.task = None
        self.right_motor = (LED(20), LED(21))
        self.left_motor = (LED(24), LED(23))
        self.position = None
        self.task = None
        self.bc_tr = False
        self.camera_height = camera_height
        
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
                self._forward_line(theta, rho)
        elif self.task == 'B-C':
            if rho > 900:
                if self.bc_tr:
                    self.position = 'C'
                    self.task = None
                    self._stop()
                else:
                    self._turn_left(150)
                    self._forward()
                    time.sleep(2.5)
                    self._stop()
                    self._turn_right(50)
                    self.bc_tr = True
        elif self.task == 'C-D':
            if rho < 900:
                self._forward_line(theta, rho)
            else:
                self._forward()
                time.sleep(0.7)
                self._stop()
                self._turn_right(90)
                self._forward()
                time.sleep(2.5)
                self._stop()
                self.position = 'D'
                self.task = None
        elif self.task == 'D-E':
            if rho > 900:
                self.position = 'E'
                self.task = None
                self._stop()
            else:
                self._forward_line(theta, rho)
                
    def _forward(self):
        self.left_motor[0].off()
        self.left_motor[1].on()
        self.right_motor[0].off()
        self.right_motor[1].on()
                
    def _forward_line(self, theta, rho):
        theta_thresh = 0.07
        rho_thresh = 10
        rho_ideal = int(self.camera_height / 2)
        if theta < 1.57 - theta_thresh or rho > rho_ideal + rho_thresh:
            self.left_motor[0].off()
            self.left_motor[1].off()
            self.right_motor[0].off()
            self.right_motor[1].on()
            time.sleep(0.01)
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].off()
            self.right_motor[1].on()
        elif theta > 1.57 + theta_thresh or rho < rho_ideal - rho_thresh:
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].off()
            self.right_motor[1].off()
            time.sleep(0.01)
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
        for i in range(int(degree / 4)):
            self.left_motor[0].on()
            self.left_motor[1].off()
            self.right_motor[0].off()
            self.right_motor[1].on()
            time.sleep(0.0494)
            self.left_motor[0].off()
            self.left_motor[1].off()
            self.right_motor[0].off()
            self.right_motor[1].off()
            time.sleep(0.15)
            
    def _turn_right(self, degree):
        for i in range(int(degree / 4)):
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].on()
            self.right_motor[1].off()
            time.sleep(0.0465)
            self.left_motor[0].off()
            self.left_motor[1].off()
            self.right_motor[0].off()
            self.right_motor[1].off()
            time.sleep(0.15)

if __name__ == '__main__':
    controller = MotorController(200)
    controller._stop()
        