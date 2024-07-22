import random

from GridCell import GridCell
from solvers.SolverTypeEnum import SolverTypeEnum

class Environment:

    def __init__(self, window, solver_class, num_robots = 1, obstacle_density=None):
        assert (num_robots == 1 and solver_class.agent_limit == "single") or (num_robots >= 1 and solver_class.agent_limit == "multiple"), "Agent number has to respect Solver agent limit."

        self.window = window

        self.solver_class = solver_class
        self.optimal_path = []
        self.algorithm_step = 0
        self.compute_time = None
        self.num_robots = num_robots

        self.grid_data = [[GridCell() for _ in range(self.window.cols)]
                          for _ in range(self.window.rows)]

        self.robot_positions = []
        self.destination_positions = []
        self.robot_found_destination = []

        if obstacle_density is None:
            obstacle_density = self.window.rows / 100.0
        self.place_obstacles(obstacle_density)
        self.place_robots_and_destinations()

        self.window.draw_grid(self.grid_data)
        # Start moving robots
        self.move_robots()

    def place_obstacles(self, obstacle_density=0.2):
        num_obstacles = int(self.window.rows * self.window.cols * obstacle_density)

        for _ in range(num_obstacles):
            while True:
                obstacle_row = random.randint(0, self.window.rows - 1)
                obstacle_col = random.randint(0, self.window.cols - 1)
                if self.grid_data[obstacle_row][obstacle_col].type == 'empty':
                    self.grid_data[obstacle_row][obstacle_col].type = 'obstacle'
                    self.grid_data[obstacle_row][obstacle_col].original_type = 'obstacle'
                    break

    def place_robots_and_destinations(self):
        for _ in range(self.num_robots):
            self.robot_found_destination.append(False)

            while True:
                robot_row = random.randint(0, self.window.rows - 1)
                robot_col = random.randint(0, self.window.cols - 1)
                if self.grid_data[robot_row][robot_col].type == 'empty':
                    self.grid_data[robot_row][robot_col].type = 'robot'
                    self.robot_positions.append((robot_row, robot_col))
                    break

            while True:
                dest_row = random.randint(0, self.window.rows - 1)
                dest_col = random.randint(0, self.window.cols - 1)
                if self.grid_data[dest_row][dest_col].type == 'empty':
                    self.grid_data[dest_row][dest_col].type = 'destination'
                    self.grid_data[dest_row][dest_col].original_type = 'destination'
                    self.destination_positions.append((dest_row, dest_col))
                    break

    def move_robots(self):
        for i, (robot_row, robot_col) in enumerate(self.robot_positions):
            if self.robot_found_destination[i]:
                continue

            dest_row, dest_col = self.destination_positions[i]

            move_row, move_col, direction = None, None, None

            if self.solver_class == SolverTypeEnum.PRIORITY_BASED or self.solver_class == SolverTypeEnum.CONFLICT_BASED:
                agents = [(robot_pos, dest_pos, i+1) for i, (robot_pos, dest_pos) in enumerate(zip(self.robot_positions, self.destination_positions))]
                solver = self.solver_class.solver_class(self, agents)

                # Change variables bc of MAPF
                if self.algorithm_step == 0 :
                    self.algorithm_step = [0 for _ in range(self.num_robots)]
                    self.optimal_path = [None for _ in range(self.num_robots)]


                if type(self.algorithm_step) == list :
                    # If first time, solve for all robots
                    if all([i == 0 for i in self.algorithm_step]) :
                        self.optimal_path = solver.solve()

                    if(not self.robot_found_destination[i]) :
                        move_row, move_col = self.optimal_path[i][self.algorithm_step[i]]
                        self.algorithm_step[i] += 1
                    else:
                        continue
            else :
                # Solve by using the solver class
                solver = self.solver_class.solver_class(self, (robot_row, robot_col), (dest_row, dest_col))

                if self.solver_class == SolverTypeEnum.RANDOM :
                    move_row, move_col, direction = solver.solve()
                else :
                    if self.algorithm_step == 0 :
                        self.optimal_path, self.compute_time = solver.solve()
                        if self.optimal_path is None:
                            print("No path found")
                            return
                        print(f"Compute time: {self.compute_time} ns")
                    move_row, move_col = self.optimal_path[self.algorithm_step]
                    self.algorithm_step+=1

            original_type = self.grid_data[robot_row][robot_col].original_type
            if self.grid_data[robot_row][robot_col].blocked_state:
                #Its a destination & corresponding robot has found it
                original_type = 'robot'
            self.grid_data[robot_row][robot_col].type = original_type
            self.robot_positions[i] = (move_row, move_col)
            self.grid_data[move_row][move_col].type = 'robot'

            #Check if it has reached its destination
            if self.robot_positions[i] == self.destination_positions[i]:
                self.robot_found_destination[i] = True
                self.grid_data[move_row][move_col].blocked_state = True

        self.window.draw_grid(self.grid_data)

        # Check if all robot has reached its destination
        if all(self.robot_found_destination):
            print("All robots reached their destination!")
        else:
            self.window.root.after(600, self.move_robots)

    def launch(self):
        self.window.root.mainloop()
