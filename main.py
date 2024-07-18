import tkinter as tk

from Environment import Environment, Solver
from GridWindow import GridWindow

if __name__ == "__main__":
    root = tk.Tk()
    grid_window = GridWindow(root, 10, 10)
    env = Environment(grid_window, Solver.DIJKSTRA, 1)
    env.launch()
