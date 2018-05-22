import time
from gpiozero import LED
import math
import threading
import RPi.GPIO as GPIO


class MotorController:
    def __init__(self, camera_height):
        GPIO.setmode(GPIO.BCM)
        self.echo_f = 16
        self.trig_f = 12
        self.echo_b = 7
        self.trig_b = 8
        GPIO.setup(self.trig_f, GPIO.OUT)
        GPIO.setup(self.echo_f, GPIO.IN)
        GPIO.setup(self.trig_b, GPIO.OUT)
        GPIO.setup(self.echo_b, GPIO.IN)
        self.task = None
        self.right_motor = (LED(21), LED(20))
        self.left_motor = (LED(23), LED(24))
        self.position = 'A'
        self.bc2_timer = None
        self.camera_height = camera_height
        self.timer = time.time()
        self.last_access = None
        time.sleep(2)
        
    def receive_state(self, rho, theta):
        if time.time() - self.timer < 1.5:
            return
        if self.task == 'Stop':
            self._stop()
            self._is_near(False)
        elif self.task == 'ab':
            if self._is_near(True, thresh=70):
                self.position = 'obst'
                self._stop()
                time.sleep(3)
                if self._is_near(True, thresh=70):
                    self.position = 'B'
                    self.task = None
                    self._stop()
                return
            if rho > 900:
                self._forward()
            else:
                self._forward_line(theta, rho)
        elif self.task == 'bc':
            self.bc2_timer = time.time()
            self.set_task('bc15')
        elif self.task == 'bc15':
            if time.time() - self.bc2_timer > 4:
                self._stop()
                self.set_task('bc18')
                return
            if self._is_near(False):
                stop_time = time.time()
                self.position = 'obst'
                self._stop()
                time.sleep(3)
                self.bc2_timer += time.time() - stop_time + 0.325
                return
            self._backward()
        elif self.task == 'bc18':
            self._turn_left(210)
            self.set_task('bc2')
            self.bc2_timer = time.time()
        elif self.task == 'bc2':
            if time.time() - self.bc2_timer > 15:
                self.position = 'C'
                self.task = None
                self._stop()
                return
            if self._is_near(True):
                stop_time = time.time()
                self.position = 'obst'
                self._stop()
                time.sleep(3)
                self.bc2_timer += time.time() - stop_time + 0.325
                return
            if rho < 900:
                self._forward_line(theta, rho)
            else:
                self._forward()
        elif self.task == 'a':
            self.bc2_timer = time.time()
            self.task = 'a2'
        elif self.task == 'a2':
            if time.time() - self.bc2_timer > 14:
                self.position = 'B'
                self._stop()
                self._turn_right(120)
                self.task = 'a3'
                self.bc2_timer = time.time()
                return
            if self._is_near(False):
                stop_time = time.time()
                self.position = 'obst'
                self._stop()
                time.sleep(3)
                self.bc2_timer += time.time() - stop_time + 0.325
                return
            if rho < 900:
                self._backward_line(theta, rho)
            else:
                self._backward()
        elif self.task == 'a3':
            if time.time() - self.bc2_timer > 2.15:
                self.position = 'A'
                self.task = None
                self._stop()
                return
            if self._is_near(False):
                stop_time = time.time()
                self.position = 'obst'
                self._stop()
                time.sleep(3)
                self.bc2_timer += time.time() - stop_time + 0.325
                return
            if rho < 900:
                self._backward_line(theta, rho)
            else:
                self._backward()
                    
    def set_task(self, task):
        self.task = task
        self.timer = time.time()
    
    def _forward(self):
        self.left_motor[0].off()
        self.left_motor[1].on()
        self.right_motor[0].off()
        self.right_motor[1].on()
                
    def _forward_line(self, theta, rho):
        theta_thresh = 0.07
        rho_thresh = 10
        rho_ideal = int(self.camera_height / 2)
        if theta < 1.57 - theta_thresh or (1.57 - theta_thresh < theta < 1.57 + theta_thresh and rho > rho_ideal + rho_thresh):
            self.left_motor[0].off()
            self.left_motor[1].off()
            self.right_motor[0].off()
            self.right_motor[1].on()
            time.sleep(0.025)
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].off()
            self.right_motor[1].on()
        elif theta > 1.57 + theta_thresh or (1.57 - theta_thresh < theta < 1.57 + theta_thresh and rho < rho_ideal - rho_thresh):
            self.left_motor[0].off()
            self.left_motor[1].on()
            self.right_motor[0].off()
            self.right_motor[1].off()
            time.sleep(0.012)
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
        
    def _backward_line(self, theta, rho):
        theta_thresh = 0.07
        rho_thresh = 10
        rho_ideal = int(self.camera_height / 2)
        if theta < 1.57 - theta_thresh or (1.57 - theta_thresh < theta < 1.57 + theta_thresh and rho < rho_ideal - rho_thresh):
            self.left_motor[0].on()
            self.left_motor[1].off()
            self.right_motor[0].off()
            self.right_motor[1].off()
            time.sleep(0.015)
            self.left_motor[0].on()
            self.left_motor[1].off()
            self.right_motor[0].on()
            self.right_motor[1].off()
        elif theta > 1.57 + theta_thresh or (1.57 - theta_thresh < theta < 1.57 + theta_thresh and rho > rho_ideal + rho_thresh):
            self.left_motor[0].off()
            self.left_motor[1].off()
            self.right_motor[0].on()
            self.right_motor[1].off()
            time.sleep(0.015)
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
            
    def _is_near(self, is_frw, thresh=100):
        if is_frw:
            GPIO.output(self.trig_f, True)
            time.sleep(0.00001)
            GPIO.output(self.trig_f, False)
            loop_start = time.time()
            while GPIO.input(self.echo_f) == 0:
                pulse_start = time.time()
                if time.time() - loop_start > 0.007:
                    break
            while GPIO.input(self.echo_f) == 1:
                pulse_end = time.time()
                if time.time() - loop_start > 0.007:
                    break
            try:
                pulse_duration = pulse_end - pulse_start
                distance = round(pulse_duration * 17150, 2)
            except:
                return False
            print(distance)
            return distance < thresh
        GPIO.output(self.trig_b, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_b, False)
        loop_start = time.time()
        while GPIO.input(self.echo_b) == 0:
            pulse_start = time.time()
            if time.time() - loop_start > 0.007:
                break
        while GPIO.input(self.echo_b) == 1:
            pulse_end = time.time()
            if time.time() - loop_start > 0.007:
                break
        try:
            pulse_duration = pulse_end - pulse_start
            distance = round(pulse_duration * 17150, 2)
        except:
            return False
        print(distance)
        return distance < thresh

if __name__ == '__main__':
    controller = MotorController(200)
    controller._backward()
    time.sleep(2)
    controller._stop()
        