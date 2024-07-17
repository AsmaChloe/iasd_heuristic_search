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
        
        self.place_obstacles()
        self.place_robots_and_destinations()
        self.draw_grid()
        
    def place_robots_and_destinations(self):
        for _ in range(self.num_robots):
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
        colors = {'empty': 'white', 'robot': 'red', 'destination': 'yellow', 'obstacle': 'black'}
        
        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                cell_color = colors[self.grid_data[row][col]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cell_color, outline="black")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    grid_window = GridWindow(root, 10, 10)
    grid_window.run()
