import tkinter as tk

from Environment import Environment
from GridWindow import GridWindow
from solvers.SolverTypeEnum import SolverTypeEnum

if __name__ == "__main__":
    root = tk.Tk()
    grid_window = GridWindow(root, 10, 10)
    env = Environment(grid_window, SolverTypeEnum.PRIORITY_BASED, 3, obstacle_density=0.2)
    env.launch()

