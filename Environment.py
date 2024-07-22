import random

from Agent import Agent
from GridCell import GridCell
from solvers.SolverTypeEnum import SolverTypeEnum


class Environment:

    def __init__(self, window, solver_class, num_robots=1, obstacle_density=None):
        assert (num_robots == 1 and solver_class.agent_limit == "single") or (
                    num_robots >= 1 and solver_class.agent_limit == "multiple"), "Agent number has to respect Solver agent limit."

        self.window = window

        self.solver_class = solver_class
        self.solver = None
        self.optimal_path = []
        self.algorithm_step = 0
        self.compute_time = None
        self.agents = []

        self.grid_data = [[GridCell() for _ in range(self.window.cols)]
                          for _ in range(self.window.rows)]

        if obstacle_density is None:
            obstacle_density = self.window.rows / 100.0
        self.place_obstacles(obstacle_density)
        self.place_robots_and_destinations(num_robots)

        self.window.draw_grid(self.grid_data)

        # Compute paths
        if self.solver_class == SolverTypeEnum.PRIORITY_BASED or self.solver_class == SolverTypeEnum.CONFLICT_BASED:
            self.solver = self.solver_class.solver_class(self, self.agents)

            optimal_paths = self.solver.solve()
            for i, agent in enumerate(self.agents):
                agent.optimal_path = optimal_paths[i]
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

    def place_robots_and_destinations(self, num_robots):
        for i in range(num_robots):

            while True:
                robot_row = random.randint(0, self.window.rows - 1)
                robot_col = random.randint(0, self.window.cols - 1)
                if self.grid_data[robot_row][robot_col].type == 'empty':
                    self.grid_data[robot_row][robot_col].type = 'robot'
                    break

            while True:
                dest_row = random.randint(0, self.window.rows - 1)
                dest_col = random.randint(0, self.window.cols - 1)
                if self.grid_data[dest_row][dest_col].type == 'empty':
                    self.grid_data[dest_row][dest_col].type = 'destination'
                    self.grid_data[dest_row][dest_col].original_type = 'destination'
                    break

            self.agents.append(Agent((robot_row, robot_col), (dest_row, dest_col), i + 1))

    def move_robots(self):
        for agent in self.agents:
            if agent.found_destination:
                continue

            robot_row, robot_col = agent.pos
            dest_row, dest_col = agent.dest

            move_row, move_col, direction = None, None, None

            if self.solver_class == SolverTypeEnum.PRIORITY_BASED or self.solver_class == SolverTypeEnum.CONFLICT_BASED:

                if not agent.found_destination:
                    move_row, move_col = agent.optimal_path[agent.algorithm_step]
                    agent.algorithm_step += 1
                else:
                    continue
            else:
                # Solve by using the solver class
                solver = self.solver_class.solver_class(self, (robot_row, robot_col), (dest_row, dest_col))

                if self.solver_class == SolverTypeEnum.RANDOM:
                    move_row, move_col, direction = solver.solve()
                else:
                    if agent.algorithm_step == 0:
                        agent.optimal_path, self.compute_time = solver.solve()
                        if agent.optimal_path is None:
                            print("No path found")
                            return
                        print(f"Compute time: {self.compute_time} ns")
                    move_row, move_col = agent.optimal_path[agent.algorithm_step]
                    agent.algorithm_step += 1

            original_type = self.grid_data[robot_row][robot_col].original_type
            if self.grid_data[robot_row][robot_col].blocked_state:
                # Its a destination & corresponding robot has found it
                original_type = 'robot'
            self.grid_data[robot_row][robot_col].type = original_type
            agent.pos = (move_row, move_col)
            self.grid_data[move_row][move_col].type = 'robot'

            # Check if it has reached its destination
            if agent.pos == agent.dest:
                agent.found_destination = True
                self.grid_data[move_row][move_col].blocked_state = True

        self.window.draw_grid(self.grid_data)

        # Check if all robot has reached its destination
        if all([agent.found_destination for agent in self.agents]):
            print("All robots reached their destination!")
        else:
            self.window.root.after(600, self.move_robots)

    def launch(self):
        self.window.root.mainloop()
