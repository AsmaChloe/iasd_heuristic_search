from solvers.Solver import Solver, POSSIBLE_MOVES

class DijkstraSolver(Solver):
    def __init__(self, environment, robot_pos, dest_pos):
        Solver.__init__(self, environment, robot_pos, dest_pos)
        
        self.distances = [[ float('inf') for _ in range(self.environment.window.cols)] for _ in range(self.environment.window.rows)]
        self.previous_step = [[ None for _ in range(self.environment.window.cols)] for _ in range(self.environment.window.rows)]


        self.distances[self.robot_pos[0]][self.robot_pos[1]] = 0

    def solve(self):
        queue = [self.robot_pos]

        while queue :
            current_pos = queue.pop(0)

            for move in POSSIBLE_MOVES :
                potential_pos = (current_pos[0]+move[0], current_pos[1]+move[1])

                #Check if position is valid
                if potential_pos[0] >=0 and potential_pos[0]<self.environment.window.rows \
                    and potential_pos[1]>=0 and potential_pos[1]<self.environment.window.cols \
                    and self.environment.grid_data[potential_pos[0]][potential_pos[1]] != 'obstacle' :

                    distance = self.distances[current_pos[0]][current_pos[1]] + 1
                    if distance < self.distances[potential_pos[0]][potential_pos[1]]:
                        self.distances[potential_pos[0]][potential_pos[1]] = distance
                        self.previous_step[potential_pos[0]][potential_pos[1]] = current_pos

                        queue.append(potential_pos)

        path = [self.dest_pos]
        current_pos = self.dest_pos

        while self.previous_step[current_pos[0]][current_pos[1]] :
            path.append(self.previous_step[current_pos[0]][current_pos[1]])
            current_pos = self.previous_step[current_pos[0]][current_pos[1]]

        return list(reversed(path))