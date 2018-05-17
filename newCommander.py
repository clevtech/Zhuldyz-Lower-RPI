import serial, time
import numpy as np


class Commander(object):
    def __init__(self):
        self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
        self.current_index = 0
        self.task = None
        self.position = 'A'
        self.bc_tr = False
        time.sleep(1)
        
    def receive_state(self, rho, theta):
        if self.task == 'Stop': self._stop()
        elif self.task == 'Align':
            self._align(theta)
            self.task = None
        elif self.task == 'A-B':
            if self.position == 'A':
                if rho > 900:
                    self.position = 'B'
                    self.task = None
                    self._stop()
                else:
                    self._forward()
                return True
            else: return False
        elif self.task == 'B-C':
            if rho > 900:
                if self.bc_tr:
                    self.position = 'C'
                    self.task = None
                    self._stop()
                self._turn_left_angle(135 + (1.57 - theta) * 57.3)
                time.sleep(1)
                self._forward()
                time.sleep(1)
                self._align(theta)
                self.bc_tr = True
            else:
                self._forward()
        elif self.task == 'C-D':
            if rho > 900:
                self.position = 'D'
                self.task = None
                self.stop()
            else:
                self._turn_right()
                time.sleep(1)
                self._forward()
                time.sleep(0.5)
                self._stop()
                time.sleep(1)
                self._align(theta)
                time.sleep(1)
                self.forward()
                
    def get_position(self):
        return self.position
    
    def get_responce(self):
        try:
            return self.arduino.readline().decode('ascii')
        except:
            return 'nothing'
               
    def set_task(self, task):
        self.task = task
            
    def _align(self, theta):
        difference = int((theta - 1.57) * 57.3)
        if difference < 0:
            self.arduino.write(("l_" + '{0:0>4}'.format(np.abs(difference))).encode("utf8"))
            print("ss: ", ("l_" + '{0:0>4}'.format(np.abs(difference))))
        else:
            self.arduino.write(("r_" + '{0:0>4}'.format(np.abs(difference))).encode("utf8"))
            print("ss: ", ("r_" + '{0:0>4}'.format(np.abs(difference))))
    def _forward(self):
        self.arduino.write('f_____'.encode("utf8"))
        
    def _stop(self):
        self.arduino.write('ssssss'.encode("utf8"))
        
    def _turn_left(self):
        self.arduino.write('q_____'.encode("utf8"))
        
    def _turn_right(self):
        self.arduino.write('e_____'.encode("utf8"))
        
    def _turn_left_angle(self, angle):
        self.arduino.write(("l_" + '{0:0>4}'.format(angle)).encode("utf8"))
        
    def _turn_right_angle(self, angle):
        self.arduino.write(("r_" + '{0:0>4}'.format(angle)).encode("utf8"))

        
    