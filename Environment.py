import random

from solvers.SolverTypeEnum import SolverTypeEnum

class Environment:

    def __init__(self, window, solver_class, num_robots):
        self.window = window

        self.solver_class = solver_class
        self.optimal_path = []
        self.dijkstra_step = 0
        self.num_robots = num_robots

        self.grid_data = [['empty' for _ in range(self.window.cols)]
                          for _ in range(self.window.rows)]

        self.robot_positions = []
        self.destination_positions = []
        self.robot_found_destination = []

        self.place_obstacles()
        self.place_robots_and_destinations()

        self.window.draw_grid(self.grid_data)
        # Start moving robots
        self.move_robots()

    def place_obstacles(self):
        num_obstacles = int(self.window.rows * self.window.cols *
                            0.2)  # 20% de la taille de la grille en obstacles

        for _ in range(num_obstacles):
            while True:
                obstacle_row = random.randint(0, self.window.rows - 1)
                obstacle_col = random.randint(0, self.window.cols - 1)
                if self.grid_data[obstacle_row][obstacle_col] == 'empty':
                    self.grid_data[obstacle_row][obstacle_col] = 'obstacle'
                    break

    def place_robots_and_destinations(self):
        for _ in range(self.num_robots):
            self.robot_found_destination.append(False)

            while True:
                robot_row = random.randint(0, self.window.rows - 1)
                robot_col = random.randint(0, self.window.cols - 1)
                if self.grid_data[robot_row][robot_col] == 'empty':
                    self.grid_data[robot_row][robot_col] = 'robot'
                    self.robot_positions.append((robot_row, robot_col))
                    break

            while True:
                dest_row = random.randint(0, self.window.rows - 1)
                dest_col = random.randint(0, self.window.cols - 1)
                if self.grid_data[dest_row][dest_col] == 'empty':
                    self.grid_data[dest_row][dest_col] = 'destination'
                    self.destination_positions.append((dest_row, dest_col))
                    break

    def move_robots(self):
        for i, (robot_row, robot_col) in enumerate(self.robot_positions):
            if self.robot_found_destination[i]:
                continue

            dest_row, dest_col = self.destination_positions[i]

            # Solve by using the solver class
            solver = self.solver_class.value(self, (robot_row, robot_col), (dest_row, dest_col))

            move_row, move_col, direction = None, None, None
            
            if self.solver_class == SolverTypeEnum.RANDOM :
                move_row, move_col, direction = solver.solve()
            
            else : #Dijkstra & A*
                if self.dijkstra_step == 0 :
                    self.optimal_path = solver.solve()
                    print(self.optimal_path)
                move_row, move_col = self.optimal_path[self.dijkstra_step]
                self.dijkstra_step+=1
                
            self.grid_data[robot_row][robot_col] = 'empty'
            self.robot_positions[i] = (move_row, move_col)
            self.grid_data[move_row][move_col] = 'robot'

            #Check if it has reached its destination
            if self.robot_positions[i] == self.destination_positions[i]:
                self.robot_found_destination[i] = True

        self.window.draw_grid(self.grid_data)

        # Check if all robot has reached its destination
        if all(self.robot_found_destination):
            print("All robots reached their destination!")
        else:
            self.window.root.after(100, self.move_robots)

    def launch(self):
        self.window.root.mainloop()
