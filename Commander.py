

class Commander(object):
    def __init__(self, segment_h, votes=5):
        self.votes = votes
        self.segment_h = segment_h
        self.last_states = []
        self.last_commands = []
        self.cm_per_pixel = 12 / height1_range[1]
        self.sec_per_rad = 0.1
        self.sec_per_cm = 0.1
        
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
            # calculate average state
            self._execute_command(top_command, state)
            
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
            self._turn_right(0.4)
            self._forward(((self.segment_h - state[1]) * self.cm_per_pixel + self.segment_h / 2) * 1.41)
            self._turn_left(0.4)
        if command == 1:
            self._forward(state[1])
        if command == 2:
            self._turn_right(state[2])
            self._forward(state[1])
            self._turn_left(state[2] / 2)
        if command == 3:
            self._backward(state[1])
            self._turn_left(state[2])
    
    def _forward(self, rho):
        return
    
    def _turn_left(self, theta):
        return
    
    def _turn_right(self, theta):
        return
    
    def _backward(self, rho):
        return
                
            