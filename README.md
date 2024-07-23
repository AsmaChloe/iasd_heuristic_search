# Multi-Agent Path Finding Simulator

This project is a multi-agent pathfinding simulation designed for the Heuristic Search course taught by Tristan Cazenave at Université Paris-Dauphine, PSL Master 2 IASD. The simulator uses various search algorithms to solve navigation puzzles on a grid and provides a graphical interface to visualize the results.

## Prerequisites and Running Experiments

To run the multi-agent pathfinding simulations described in this project, you need to set up your development environment and install the necessary dependencies. Follow these steps:

### Prerequisites

1. **Python**: This project has been developed with Python 3.12. Ensure that Python 3.12 is installed on your system.
   
   Check your Python version with:
   ```bash
   python --version
    ```

2. **Python Libraries**: You need to install the required Python libraries to run the project. 
    ```bash
    pip install -r requirements.txt
    ```

### Running an Experiment

The project uses a command-line interface to configure the simulation parameters. Here are the available options:

- `--size`: Size of the grid (default: 10)
- `--solver`: Solver algorithm to use (`RANDOM`, `DIJKSTRA`, `ASTAR`, `BFS`, `GREEDY_BFS`, `PRIORITY_BASED`, `CONFLICT_BASED`)
- `--num_agents`: Number of agents in the environment (default: 1)
- `--obstacle_density`: Density of obstacles in the grid, expressed as a percentage of obstacles relative to the grid size. This should be given as a floating-point value. If not specified, the obstacle percentage will be equal to the grid size. For example, if the grid size is 10, then 10% of the grid will be filled with obstacles.

For example, to run a simulation with a 15x15 grid using the A* algorithm, with 1 agent and an obstacle density of 0.2, you can execute the following command:

```bash
python main.py --size 15 --solver ASTAR --num_agents 1 --obstacle_density 0.2
