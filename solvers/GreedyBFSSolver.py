import time

from solvers.parents.SAPFSolver import SAPFSolver
from solvers.parents.Solver import Solver, POSSIBLE_MOVES


class GreedyBFSSolver(SAPFSolver):

    def __init__(self, environment, robot_pos, dest_pos):
        SAPFSolver.__init__(self, environment, robot_pos, dest_pos)

        self.parent = {}
        self.visited = [[False for _ in range(self.environment.window.cols)] for _ in range(self.environment.window.rows)]

    def heuristic(self, pos):
        return abs(pos[0] - self.dest_pos[0]) + abs(pos[1] - self.dest_pos[1])

    def solve(self):
        queue = []
        queue.append((self.heuristic(self.robot_pos), self.robot_pos))
        start_time = time.time_ns()

        while queue:
            _, current_pos = queue.pop(0)

            # End
            if current_pos == self.dest_pos:
                path = [self.dest_pos]
                self.compute_time = (time.time_ns() - start_time)

                while current_pos is not None:
                    path.append(current_pos)
                    current_pos = self.parent.get(current_pos)
                return list(reversed(path)), self.compute_time

            self.visited[current_pos[0]][current_pos[1]] = True

            for move in POSSIBLE_MOVES:
                potential_pos = (current_pos[0] + move[0],
                                 current_pos[1] + move[1])

                # Check if position is valid
                if 0 <= potential_pos[0] < self.environment.window.rows and \
                   0 <= potential_pos[1] < self.environment.window.cols and \
                   self.environment.grid_data[potential_pos[0]][potential_pos[1]] != 'obstacle' and \
                   not self.visited[potential_pos[0]][potential_pos[1]]:

                    queue.append((self.heuristic(potential_pos), potential_pos))
                    self.parent[potential_pos] = current_pos

        return None, None
