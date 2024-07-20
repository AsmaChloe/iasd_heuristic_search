import tkinter as tk

from Environment import Environment
from GridWindow import GridWindow
from solvers.SolverTypeEnum import SolverTypeEnum

if __name__ == "__main__":
    root = tk.Tk()
    grid_window = GridWindow(root, 30, 30)
    env = Environment(grid_window, SolverTypeEnum.GreedyBFSSolver, 1)
    env.launch()