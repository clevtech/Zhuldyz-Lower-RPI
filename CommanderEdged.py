import serial, time, struct, math


class CommanderEdged:
    def __init__(self, map, cap_h):
        self.map = map
        self.current_index = 0
        self.cap_h = cap_h
        self.sec_per_rad = 1.0 / 5.93
        self.sec_per_cm = 1.0 / 63
        self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
        time.sleep(2)
        
    def angle_calibration(self, theta):
        print(theta - 1.57)
        if (theta - 1.57) > 0:
            self._turn_right(theta - 1.57)
        else:
            self._turn_left(1.57 - theta)
            
            
    def position_calibration(self, rho):
        if (rho - self.cap_h / 2) > 0:
            self._turn_right(0.3)
            self._forward(math.fabs(rho - self.cap_h / 2))
            self._turn_left(0.3)
        else:
            self._turn_left(0.3)
            self._forward(math.fabs(rho - self.cap_h / 2))
            self._turn_right(0.3)
            
    def move(self):
        self.arduino.write(("iiiiii").encode('utf8'))
        
    def stop(self):
        self.arduino.write(("tttttt").encode('utf8'))
        
    def turn(self, side):
        if side == 'r':
            self.arduino.write(("eeeeee").encode('utf8'))
        else:
            self.arduino.write(("qqqqqq").encode('utf8'))
            
    def _forward(self, dist):
        self.arduino.write(("f_" + '{0:0>4}'.format(int(dist * self.sec_per_cm * 1000))).encode("utf8"))
	#print(int(dist * self.sec_per_cm * 1000))
        time.sleep(dist * self.sec_per_cm)
    
    def _turn_left(self, theta):
        self.arduino.write(("l_" + '{0:0>4}'.format(int(theta * self.sec_per_rad * 1000))).encode("utf8"))
        #print(int(theta * self.sec_per_rad * 1000))
        time.sleep(int(theta * self.sec_per_rad))
    
    def _turn_right(self, theta):
        self.arduino.write(("r_" + '{0:0>4}'.format(int(theta * self.sec_per_rad * 1000))).encode("utf8"))
        #print(int(theta * self.sec_per_rad * 1000))
        time.sleep(int(theta * self.sec_per_rad))
    
    def _backward(self, dist):
        self.arduino.write(("b_" + '{0:0>4}'.format(int(dist * self.sec_per_cm * 1000))).encode("utf8"))
        #print(int(dist * self.sec_per_cm * 1000))
        time.sleep(int(dist * self.sec_per_cm))