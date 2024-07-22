from abc import abstractmethod

POSSIBLE_MOVES = [
    (-1, 0, 'UP'),
    (1, 0, 'DOWN'),
    (0, -1, 'LEFT'),
    (0, 1, 'RIGHT')
]

class Solver:
    def __init__(self, environment, constraints=None) -> None:
        self.environment = environment
        self.compute_time = None
        self.constraints = constraints or set()  # Set of constraints (time, pos, agent_id)

    @abstractmethod
    def solve(self):
        pass

    def is_valid(self, pos, time_step = None):
        if 0 <= pos[0] < self.environment.window.rows and \
                0 <= pos[1] < self.environment.window.cols and \
                self.environment.grid_data[pos[0]][pos[1]].type != 'obstacle':

            if self.constraints is not None :
                for (t, p, agent_id) in self.constraints:
                    if t == time_step and p == pos:
                        return False
                return True
        return False