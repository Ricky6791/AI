# AI
CSCI 4202 introduction to AI
\# Sliding Tile Puzzle Solver

## Overview

This project implements a Sliding Tile Puzzle Solver using various algorithms and heuristics. The solver is designed to find the optimal solution to a given puzzle configuration, considering different search strategies.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Usage](#usage)
- [Algorithms](#algorithms)
- [Heuristics](#heuristics)
- [Code Structure](#code-structure)
- [How to Run](#how-to-run)
- [Sample Output](#sample-output)
- [Contributing](#contributing)
- [License](#license)

## Features

- Backtracking algorithm for exploring possible state transitions within a specified depth bound.
- Uniform Cost Search (UCS) for optimal path finding.
- A* Search algorithm with heuristics including misplaced tiles and Manhattan distance.
- Python implementation with JSON input for puzzle configuration.

## Technologies Used

- Python
- JSON
- Priority Queue (Heapq)

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/sliding-tile-puzzle-solver.git

2. cd sliding-tile-puzzle-solver

3. python sliding_tile_solver.py

## Algorithms
Backtracking: Explores possible state transitions within a specified depth bound.
Uniform Cost Search (UCS): Finds the optimal path using cost-based exploration.
A Search:* Uses heuristics for informed search, including misplaced tiles and Manhattan distance.
## Heuristics
Misplaced Tiles: Counts the number of tiles in the wrong position compared to the goal state.
Manhattan Distance: Calculates the sum of the distances of each tile to its goal position.
## Code Structure
sliding_tile_solver.py: Main script containing the SlidingTilePuzzle class and the algorithms.
problem-1.json: Sample JSON file containing puzzle configuration.
## How to Run
Ensure you have Python installed.

Clone the repository and navigate to the project directory.

Run the solver script:
python sliding_tile_solver.py
