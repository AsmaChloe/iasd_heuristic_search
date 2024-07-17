import tkinter as tk

class GridWindow:
    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols

        self.canvas = tk.Canvas(self.root, width=self.cols * 50, height=self.rows * 50, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

    def draw_grid(self, grid_data):
        self.canvas.delete("all")  # Clear previous drawings

        colors = {'empty': 'white', 'robot': 'red', 'destination': 'yellow', 'obstacle': 'black'}

        for row in range(self.rows):
            for col in range(self.cols):
                x1, y1 = col * 50, row * 50
                x2, y2 = x1 + 50, y1 + 50
                cell_color = colors[grid_data[row][col]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=cell_color, outline="black")

