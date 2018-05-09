import serial, time, struct


class Commander(object):
    def __init__(self, segment_h, segment_w, votes=5):
        self.votes = votes
        self.segment_h = segment_h
        self.segment_w = segment_w
        self.last_states = []
        self.last_commands = []
        self.cm_per_pixel = 12 / segment_h
        self.sec_per_rad = 0.1
        self.sec_per_cm = 0.1
        self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
        time.sleep(2)
        
    def receive_state(self, state):
        self.last_states.append(state)
        self.last_commands.append(self._command_id(state))
        if len(self.last_commands) > 2 * self.votes:
            self.last_states.pop(0)
            self.last_commands.pop(0)
        top_command = max(self.last_commands, key=last_commands.count)
        n_top_command = self.last_commands.count(top_command)
        if n_top_command >= self.votes:
            indices_top_command = [i for i, _ in enumerate(self.last_commands) if x == top_command]
            top_states = [st for index, st in enumerate(self.last_states) if index in indices_top_command]
            rho = 0
            theta = 0
            for state in top_states:
                rho += state[1]
                theta += state[2]
            self._execute_command(top_command, (0, rho / len(top_states), theta / len(top_states)))
            
    def _command_id(self, state, tolerance=0.39):
        if state[0] == 0:
            if (1.57 - tolerance) <= state[2] <= (1.57 + tolerance): return 0
            if (0.79 - tolerance) <= state[2] <= (0.79 + tolerance): return 1
            if (2.36 - tolerance) <= state[2] <= (2.36 + tolerance): return 2
            if (3.14 - tolerance) <= state[2] <= 3.14 or 0 <= state[2] <= tolerance: return 3
        if state[0] == 1:
            if (1.57 - tolerance) <= state[2] <= (1.57 + tolerance): return 4
            if (0.79 - tolerance) <= state[2] <= (0.79 + tolerance): return 5
            if (2.36 - tolerance) <= state[2] <= (2.36 + tolerance): return 6
            if (3.14 - tolerance) <= state[2] <= 3.14 or 0 <= state[2] <= tolerance: return 7
        if state[0] == 2:
            if (1.57 - tolerance) <= state[2] <= (1.57 + tolerance): return 8
            if (0.79 - tolerance) <= state[2] <= (0.79 + tolerance): return 9
            if (2.36 - tolerance) <= state[2] <= (2.36 + tolerance): return 10
            if (3.14 - tolerance) <= state[2] <= 3.14 or 0 <= state[2] <= tolerance: return 11
            
    def _execute_command(self, command, state):
        if command == 0:
            self._turn_right(0.8 + state[2] - 1.57)
            self._forward((self.segment_h - state[1] + self.segment_h / 2) * self.cm_per_pixel * 1.41)
            self._turn_left(0.8)
        elif command == 1:
            self._forward((self.segment_w * 0.7) * self.cm_per_pixel)
        elif command == 2:
            self._turn_right(0.8)
        elif command == 3:
            self._backward((rho + self.segment_w) * self.cm_per_pixel)
            self._turn_left(1.57)
        elif command == 4:
            self._forward((self.segment_w * 2) * self.cm_per_pixel)
        elif command == 5:
            self._turn_left(2 * 0.79 - state[2])
        elif command == 6:
            self._turn_right(0.79 + state[2] - 2.36)
        elif command == 7:
            self._backward((rho + self.segment_w) * self.cm_per_pixel)
            self._turn_left(1.57)
        elif command == 8:
            self._turn_left(0.8 - state[2] + 1.57)
            self._forward((self.segment_h - state[1] + self.segment_h / 2) * self.cm_per_pixel * 1.41)
            self._turn_right(0.8)
        elif command == 9:
            self._turn_left(2 * 0.79 - state[2])
        elif command == 10:
            self._forward((self.segment_w * 0.7))
        elif command == 11:
            self._backward((rho + self.segment_w) * self.cm_per_pixel)
            self._turn_left(1.57)
    
    def _forward(self, dist):
        self.arduino.write(("f_" + '0:0>4'.format(int(dist * self.sec_per_cm * 1000))).encode("utf8"))
    
    def _turn_left(self, theta):
        self.arduino.write(("l_" + '0:0>4'.format(int(theta * self.sec_per_rad * 1000))).encode("utf8"))
    
    def _turn_right(self, theta):
        self.arduino.write(("r_" + '0:0>4'.format(int(theta * self.sec_per_rad * 1000))).encode("utf8"))
    
    def _backward(self, dist):
        elf.arduino.write(("b_" + '0:0>4'.format(int(dist * self.sec_per_cm * 1000))).encode("utf8"))
        
if __name__ == "__main__":
    commander = Commander(5,6)
    commander._turn_right(1)
