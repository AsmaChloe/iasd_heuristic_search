import tkinter as tk
import random

class GridWindow:
    def __init__(self, root, rows, cols, num_robots = 1):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.num_robots = num_robots

        self.canvas = tk.Canvas(self.root, width=self.cols * 50, height=self.rows * 50, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

        self.grid_data = [['empty' for _ in range(self.cols)] for _ in range(self.rows)]
        self.robot_positions = []
        self.destination_positions = []
        self.robot_found_destination = []

        self.place_obstacles()
        self.place_robots_and_destinations()
        self.draw_grid()

        # Start moving robots
        self.move_robots()

    def place_robots_and_destinations(self):
        for _ in range(self.num_robots):
            self.robot_found_destination.append(False)
            
            while True:
                robot_row = random.randint(0, self.rows - 1)
                robot_col = random.randint(0, self.cols - 1)
                if self.grid_data[robot_row][robot_col] == 'empty':
                    self.grid_data[robot_row][robot_col] = 'robot'
                    self.robot_positions.append((robot_row, robot_col))
                    break

            while True:
                dest_row = random.randint(0, self.rows - 1)
                dest_col = random.randint(0, self.cols - 1)
                if self.grid_data[dest_row][dest_col] == 'empty':
                    self.grid_data[dest_row][dest_col] = 'destination'
                    self.destination_positions.append((dest_row, dest_col))
                    break

    def place_obstacles(self):
        num_obstacles = int(self.rows * self.cols * 0.2)  # 20% de la taille de la grille en obstacles

        for _ in range(num_obstacles):
            while True:
                obstacle_row = random.randint(0, self.rows - 1)
                obstacle_col = random.randint(0, self.cols - 1)
                if self.grid_data[obstacle_row][obstacle_col] == 'empty':
                    self.grid_data[obstacle_row][obstacle_col] = 'obstacle'
                    break

    def draw_grid(self):
        self.canvas.delete("all")  # Clear previous drawings

        colors = {'empty': 'white', 'robot': 'red', 'destination': 'yellow', 'obstacle': 'black'}

        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                cell_color = colors[self.grid_data[row][col]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cell_color, outline="black")

    def move_robots(self):
        for i, (robot_row, robot_col) in enumerate(self.robot_positions):
            if self.robot_found_destination[i]:
                continue
                
            dest_row, dest_col = self.destination_positions[i]

            # Randomly move the robot
            possible_moves = []
            if robot_row > 0 and self.grid_data[robot_row - 1][robot_col] != 'obstacle':  # Up
                possible_moves.append((-1, 0, 'UP'))
            if robot_row < self.rows - 1 and self.grid_data[robot_row + 1][robot_col] != 'obstacle':  # Down
                possible_moves.append((1, 0, 'DOWN'))
            if robot_col > 0 and self.grid_data[robot_row][robot_col - 1] != 'obstacle':  # Left
                possible_moves.append((0, -1, 'LEFT'))
            if robot_col < self.cols - 1 and self.grid_data[robot_row][robot_col + 1] != 'obstacle':  # Right
                possible_moves.append((0, 1, 'RIGHT'))

            if possible_moves:
                move_row, move_col, direction = random.choice(possible_moves)
                self.grid_data[robot_row][robot_col] = 'empty'
                self.robot_positions[i] = (robot_row + move_row, robot_col + move_col)
                self.grid_data[robot_row + move_row][robot_col + move_col] = 'robot'

                #Check if it has reached its destination
                if self.robot_positions[i] == self.destination_positions[i] :
                    self.robot_found_destination[i] = True

        self.draw_grid()

        # Check if all robot has reached its destination
        if all(self.robot_found_destination):
            print("All robots reached their destination!")
        else:
            self.root.after(100, self.move_robots)
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    grid_window = GridWindow(root, 10, 10)
    grid_window.run()