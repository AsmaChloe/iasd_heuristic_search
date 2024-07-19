import time

from solvers.Solver import Solver, POSSIBLE_MOVES

class DijkstraSolver(Solver):

    def __init__(self, environment, robot_pos, dest_pos):
        Solver.__init__(self, environment, robot_pos, dest_pos)

        self.parent = {}
        self.g_cost = {self.robot_pos: 0}
        self.visited = [[False for _ in range(self.environment.window.cols)]
                        for _ in range(self.environment.window.rows)]

    def solve(self):
        queue = []
        queue.append(self.robot_pos)
        start_time = time.time_ns()
        while queue:
            current_pos = queue.pop(0)

            # End - Retracing path
            if current_pos == self.dest_pos:
                self.compute_time = time.time_ns() - start_time

                path = [self.dest_pos]
                while current_pos is not None:
                    path.append(current_pos)
                    current_pos = self.parent.get(current_pos)
                return list(reversed(path)), self.compute_time

            self.visited[current_pos[0]][current_pos[1]] = True

            for move in POSSIBLE_MOVES:
                potential_pos = (current_pos[0] + move[0], current_pos[1] + move[1])

                #If valid position
                if 0 <= potential_pos[0] < self.environment.window.rows and \
                   0 <= potential_pos[1] < self.environment.window.cols and \
                   self.environment.grid_data[potential_pos[0]][potential_pos[1]] != 'obstacle' and \
                   not self.visited[potential_pos[0]][potential_pos[1]]:

                    tentative_g_cost = self.g_cost[current_pos] + 1

                    if potential_pos not in self.g_cost or tentative_g_cost < self.g_cost[potential_pos]:
                        self.g_cost[potential_pos] = tentative_g_cost
                        queue.append(potential_pos)
                        self.parent[potential_pos] = current_pos

        return None, None