import tkinter as tk
import argparse

from Environment import Environment
from GridWindow import GridWindow
from solvers.SolverTypeEnum import SolverTypeEnum

def parse_args():
    parser = argparse.ArgumentParser(description="Multi-Agent Path Finding Simulator")
    parser.add_argument("--size", type=int, default=10, help="Side size of the grid")
    parser.add_argument("--solver",
                        type=str,
                        choices=["RANDOM", "DIJKSTRA", "ASTAR", "BFS", "GREEDY_BFS", "PRIORITY_BASED", "CONFLICT_BASED"],
                        default="DIJKSTRA",
                        help="Solver algorithm to use")
    parser.add_argument("--num_agents", type=int, default=1, help="Number of agents in the environment")
    parser.add_argument("--obstacle_density", type=float, default=None, help="Density of obstacles in the grid")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    solver_mapping = {
        "RANDOM": SolverTypeEnum.RANDOM,
        "DIJKSTRA": SolverTypeEnum.DIJKSTRA,
        "ASTAR": SolverTypeEnum.ASTAR,
        "BFS": SolverTypeEnum.BFS,
        "GREEDY_BFS": SolverTypeEnum.GREEDY_BFS,
        "PRIORITY_BASED": SolverTypeEnum.PRIORITY_BASED,
        "CONFLICT_BASED": SolverTypeEnum.CONFLICT_BASED
    }
    selected_solver = solver_mapping[args.solver]

    root = tk.Tk()
    grid_window = GridWindow(root, args.size, args.size)
    env = Environment(grid_window, selected_solver, args.num_agents, obstacle_density=args.obstacle_density)
    env.launch()

