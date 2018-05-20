import time
from gpiozero import LED
import math
import threading
import RPi.GPIO as GPIO


class MotorController:
    def __init__(self, camera_height):
        GPIO.setmode(GPIO.BCM)
        self.echo_f1 = 16
        self.trig_f1 = 12
        self.echo_f2 = 7
        self.trig_f2 = 8
        self.echo_b1 = 5
        self.trig_b1 = 6
        self.echo_b2 = 13
        self.trig_b2 = 19
        GPIO.setup(self.trig_f1, GPIO.OUT)
        GPIO.setup(self.echo_f1, GPIO.IN)
        GPIO.setup(self.trig_f2, GPIO.OUT)
        GPIO.setup(self.echo_f2, GPIO.IN)
        GPIO.setup(self.trig_b1, GPIO.OUT)
        GPIO.setup(self.echo_b1, GPIO.IN)
        GPIO.setup(self.trig_b2, GPIO.OUT)
        GPIO.setup(self.echo_b2, GPIO.IN)
        self.task = None
        self.right_motor = (LED(20), LED(21))
        self.left_motor = (LED(24), LED(23))
        self.is_forw = LED(18)   
        self.position = 'A'
        self.bc_tr = False
        self.camera_height = camera_height
        self.timer = None
        self.last_access = None
        time.sleep(2)
        
    def receive_state(self, rho, theta):
        if time.time() - self.timer < 3:
            return
##        if self._measure_distance() < 70.0:
##            self.position = 'Obstacle'
##            return
        if self.task == 'Stop':
            self._stop()
        elif self.task == 'ab':
            if self._is_near(True):
                self.position = 'obst'
                return
            if rho > 900:
                self.position = 'B'
                self.task = None
                self._stop()
            else:
                self._forward_line(theta, rho)
        elif self.task == 'bc':
            if self._is_near(True):
                self.position = 'obst'
                return
            if rho > 900:
                if self.bc_tr:
                    self.task = None
                    self._stop()
                else:
                    self._turn_left(150)
                    self._forward()
                    time.sleep(3.5)
                    self._stop()
                    self._turn_right(50)
                    self.bc_tr = True
                    self.set_task('bc2')
        elif self.task == 'bc2':
            if self._is_near(True):
                self.position = 'obst'
                return
            if rho < 900:
                self._forward_line(theta, rho)
            else:
                self._stop()
                self._turn_right(110)
                self._forward()
                time.sleep(1.7)
                self._stop()
                self.position = 'C'
                self.task = None
        elif self.task == 'cd':
            if self._is_near(True):
                self.position = 'obst'
                return
            if rho > 900:
                self.position = 'D'
                self.task = None
                self._stop()
            else:
                self._forward_line(theta, rho)
        elif self.task == 'a':
            if self._is_near(False):
                self.position = 'obst'
                return
            self._backward()
            time.sleep(2)
            self._stop()
            self.set_task('a2')
        elif self.task == 'a2':
            if self._is_near(False):
                self.position = 'obst'
                return
            if rho < 900:
                self._backward_line(theta, rho)
            else:
                self._stop()
                self._turn_left(90)
                self._backward()
                time.sleep(3)
                self._stop()
                self.set_task('a3')
        elif self.task == 'a3':
            if self._is_near(False):
                self.position = 'obst'
                return
            if rho < 900:
                self._backward_line(theta, rho)
            else:
                self._stop()
                self._turn_right(165)
                self._backward()
                time.sleep(2.5)
                self._stop()
                self._turn_left(65)
                self.set_task('a4')
                self.last_access = time.time()
        elif self.task == 'a4':
            if self._is_near(False):
                self.position = 'obst'
                return
            if time.time() - self.last_access > 4:
                self._stop()
                self.position = 'A'
                self.task = None
                return
            self._backward_line(theta, rho)
                    
    def set_task(self, task):
        self.task = task
        self.timer = time.time()
    
    def _forward(self):
        self.is_forw.on()
        self.left_motor[0].off()
        self.left_motor[1].on()
        self.right_motor[0].off()
        self.right_motor[1].on()
                
    def _forward_line(self, theta, rho):
        self.is_forw.on()
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
        self.is_forw.off()
        self.left_motor[0].on()
        self.left_motor[1].off()
        self.right_motor[0].on()
        self.right_motor[1].off()
        
    def _backward_line(self, theta, rho):
        self.is_forw.off()
        theta_thresh = 0.07
        rho_thresh = 10
        rho_ideal = int(self.camera_height / 2)
        if theta < 1.57 - theta_thresh or (1.57 - theta_thresh < theta < 1.57 + theta_thresh and rho < rho_ideal - rho_thresh):
            self.left_motor[0].on()
            self.left_motor[1].off()
            self.right_motor[0].off()
            self.right_motor[1].off()
            time.sleep(0.01)
            self.left_motor[0].on()
            self.left_motor[1].off()
            self.right_motor[0].on()
            self.right_motor[1].off()
        elif theta > 1.57 + theta_thresh or (1.57 - theta_thresh < theta < 1.57 + theta_thresh and rho > rho_ideal + rho_thresh):
            self.left_motor[0].off()
            self.left_motor[1].off()
            self.right_motor[0].on()
            self.right_motor[1].off()
            time.sleep(0.01)
            self.left_motor[0].on()
            self.left_motor[1].off()
            self.right_motor[0].on()
            self.right_motor[1].off()
        else:
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
            
    def _is_near(self, is_frw, thresh=70):
        if is_frw:
            GPIO.output(self.trig_f1, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_f1, False)
            while GPIO.input(self.echo_f1) == 0:
                pulse_start_1 = time.time()         
            while GPIO.input(self.echo_f1) == 1:
                pulse_end_1 = time.time()
            GPIO.output(self.trig_f2, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_f2, False)
            while GPIO.input(self.echo_f2) == 0:
                pulse_start_2 = time.time()         
            while GPIO.input(self.echo_f2) == 1:
                pulse_end_2 = time.time()
            try:
                pulse_duration_1 = pulse_end_1 - pulse_start_1
                distance_1 = round(pulse_duration_1 * 17150, 2)
                pulse_duration_2 = pulse_end_2 - pulse_start_2
                distance_2 = round(pulse_duration_2 * 17150, 2)
            except:
                return False
            print(distance_1)
            print(distance_2)
            return distance_1 < thresh or distance_2 < thresh
        GPIO.output(self.trig_b1, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_b1, False)
        while GPIO.input(self.echo_b1) == 0:
            pulse_start_1 = time.time()         
        while GPIO.input(self.echo_b1) == 1:
            pulse_end_1 = time.time()
        GPIO.output(self.trig_b2, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_b2, False)
        while GPIO.input(self.echo_b2) == 0:
            pulse_start_2 = time.time()         
        while GPIO.input(self.echo_b2) == 1:
            pulse_end_2 = time.time()
        try:
            pulse_duration_1 = pulse_end_1 - pulse_start_1
            distance_1 = round(pulse_duration_1 * 17150, 2)
            pulse_duration_2 = pulse_end_2 - pulse_start_2
            distance_2 = round(pulse_duration_2 * 17150, 2)
        except:
            return False
        return distance_1 < thresh or distance_2 < thresh

if __name__ == '__main__':
    controller = MotorController(200)
    while True:
        controller._is_near(True)
        