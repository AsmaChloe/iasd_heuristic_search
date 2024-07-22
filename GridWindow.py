import tkinter as tk

class GridWindow:
    def __init__(self, root, rows, cols, square_scale=20):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.square_scale = square_scale

        self.canvas = tk.Canvas(self.root, width=self.cols * self.square_scale, height=self.rows * self.square_scale, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

    def draw_grid(self, grid_data):
        self.canvas.delete("all")  # Clear previous drawings

        colors = {'empty': 'white', 'robot': 'red', 'destination': 'yellow', 'obstacle': 'black'}

        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * self.square_scale, row * self.square_scale
                x2, y2 = x1 + self.square_scale, y1 + self.square_scale
                cell_color = colors[grid_data[row][col].type]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cell_color, outline="black")

