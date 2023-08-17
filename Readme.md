# Maze Solver using Q-Learning

This project demonstrates a maze solver using the Q-learning reinforcement learning algorithm. The solver learns to navigate through a grid-based environment to reach the goal while avoiding obstacles.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [License](#license)

## Introduction

The Maze Solver uses Q-learning to train an AI agent to find the optimal path from a starting position to a goal in a maze-like environment. The maze is represented as a grid, with walls, aisles, and a goal position. The AI agent learns to make decisions about which actions (up, down, left, right) to take in order to reach the goal while avoiding obstacles.

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/aksshainair/AIMazeExplorer.git
    cd AIMazeExplorer
    ```

2. Install Dependencies

    ```bash
    pip install numpy SimpleGUICS2Pygame
    ```

3. Run the main.py script

    ```bash
    python main.py
    ```

## Usage

1. Upon running the main.py script, a graphical interface will open, displaying the maze environment.
2. You can input the starting coordinates (a, b) for the maze solver using the input box. The solver will find the optimal path from the starting position to the goal.
3. The solver's progress will be displayed on the GUI, where the agent's path is marked in red.

## Screenshot

![Alt Demo Image](https://raw.githubusercontent.com/aksshainair/AIMazeExplorer/main/screenshots/maze.png)



