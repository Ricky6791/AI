import json
import heapq # For priority queue


def read_JSON(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        n = data["n"]
        start = data["start"]
        goal = data["goal"]
        return n, start, goal

class Rule:
    def __init__(self, name, puzzle):
        self.name = name
        self.puzzle = puzzle # reference to the puzzle

    # To convert moves to string
    def __str__(self):
        return str(self.name)

    def precondition(self, state):
        if self.name == "up":
            return self.puzzle.can_move_up(state)
        elif self.name == "down":
            return self.puzzle.can_move_down(state)
        elif self.name == "left":
            return self.puzzle.can_move_left(state)
        elif self.name == "right":
            return self.puzzle.can_move_right(state)

    def action(self, state):
        if self.name == "up":
            return self.puzzle.move_up(state)
        elif self.name == "down":
            return self.puzzle.move_down(state)
        elif self.name == "left":
            return self.puzzle.move_left(state)
        elif self.name == "right":
            return self.puzzle.move_right(state)



class SlidingTilePuzzle:
    def __init__(self, size, start_state, goal_state):
        self.size = size
        self.start_state = start_state
        self.goal_state = goal_state
        self.nodes_examined = 0
        self.bound = 26
        self.rules = [Rule(name, self) for name in ["up", "down", "left", "right"]]

    def can_move_up(self, state):
        empty_r, empty_c = self.find_empty_tile(state)
        return empty_r > 0

    def move_up(self, state):
        empty_r, empty_c = self.find_empty_tile(state)
        new_state = [list(row) for row in state]
        # swap
        new_state[empty_r][empty_c], new_state[empty_r - 1][empty_c] = new_state[empty_r - 1][empty_c], new_state[empty_r][empty_c]
        return new_state

    def can_move_down(self, state):
        empty_r, empty_c = self.find_empty_tile(state)
        return empty_r < self.size - 1

    def move_down(self, state):
        empty_r, empty_c = self.find_empty_tile(state)
        new_state = [list(row) for row in state]
        # swap
        new_state[empty_r][empty_c], new_state[empty_r + 1][empty_c] = new_state[empty_r + 1][empty_c], new_state[empty_r][empty_c]
        return new_state

    def can_move_left(self, state):
        empty_r, empty_c = self.find_empty_tile(state)
        return empty_c > 0

    def move_left(self, state):
        empty_r, empty_c = self.find_empty_tile(state)
        new_state = [list(row) for row in state]
        # swap
        new_state[empty_r][empty_c], new_state[empty_r][empty_c - 1] = new_state[empty_r][empty_c - 1], new_state[empty_r][empty_c]
        return new_state

    def can_move_right(self, state):
        empty_r, empty_c = self.find_empty_tile(state)
        return empty_c < self.size - 1

    def move_right(self, state):
        empty_r, empty_c = self.find_empty_tile(state)
        new_state = [list(row) for row in state]
        # swap
        new_state[empty_r][empty_c], new_state[empty_r][empty_c + 1] = new_state[empty_r][empty_c + 1], new_state[empty_r][empty_c]
        return new_state

    def find_empty_tile(self, state):
        for r in range(self.size):
            for c in range(self.size):
                if state[r][c] == 0:
                    return r, c

    def backtracking(self, datalist, bound):
        self.nodes_examined += 1
        data = datalist[-1]
        if data in datalist[:-1]:
            return None
        if data == self.goal_state:
            return []
        if len(datalist) > bound:
            return None

        for rule in self.APPRULES(data):
            rdata = self.successor_state(data, rule)
            rdatalist = datalist + [rdata]
            path = self.backtracking(rdatalist, bound) # Recursive backtrack with new state
            if path is not None:
                return [str(rule)] + path

        return None

    def solve_backtracking(self):
        bound = 1
        cumulative_nodes_examined = 0

        while True:
            self.nodes_examined = 0  # Reset nodes examined
            solution = self.backtracking([self.start_state], bound)
            cumulative_nodes_examined += self.nodes_examined

            if solution is not None:  # If a solution is found
                print(f"Solution found with bound {bound}")
                print(f"Nodes examined at bound {bound}: {self.nodes_examined}")
                print(f"Solution: {solution}")
                print(f"Solution length: {len(solution)}")
                return

            else:  # If no solution is found at the current bound
                print(f"No solution found at bound {bound}. Cumulative nodes examined: {cumulative_nodes_examined}")

            bound += 1  # Increment the depth bound for the next iteration

            if bound > 50:
                print(f"No solution found within maximum bound: 50")
                return

    def APPRULES(self, state):
        return [rule for rule in self.rules if rule.precondition(state)]

    def successor_state(self, state, rule):
        return rule.action(state)

    # uniform cost search from book example page 84
    def ucs_solve(self):
        nodes_generated = 0  # total number of nodes added to frontier
        nodes_examined = 0  # total number of nodes that have been evaluated from frontier
        frontier = [(0, self.start_state, [])]
        explored = set()  # Keep track of explored states

        while frontier:
            path_cost, state, moves = heapq.heappop(frontier)  # creates the priority queue
            nodes_examined += 1
            if state == self.goal_state:
                return moves, path_cost, nodes_generated, nodes_examined

            explored.add(tuple(tuple(row) for row in state))

            for rule in self.APPRULES(state):
                successor = rule.action(state)
                if tuple(map(tuple, successor)) not in explored:
                    new_cost = path_cost + 1  # path cost increases by 1 per step
                    heapq.heappush(frontier, (new_cost, successor, moves + [str(rule)]))
                    nodes_generated += 1

        return [], -1, nodes_generated, nodes_examined  # No solution found

    # Heuristic 1: Number of misplaced tiles compared to goal
    def h1(self, state):
        misplaced = sum(1 for i in range(self.size) for j in range(self.size) if state[i][j] != self.goal_state[i][j])
        return misplaced

    def h2(self, state):
        total_distance = 0
        for i in range(self.size):
            for j in range(self.size):
                value = state[i][j]
                if value != 0:  # Ignore the zero for distance calculating
                    for x in range(self.size):
                        for y in range(self.size):
                            if self.goal_state[x][y] == value:
                                goal_i, goal_j = x, y
                                break
                    total_distance += abs(i - goal_i) + abs(j - goal_j)  # get the distance from current position to the goal position
        return total_distance

    def astar_solve(self, heuristic):
        nodes_generated = 0
        if heuristic == "h1":
            h_func = self.h1
        elif heuristic == "h2":
            h_func = self.h2
        else:
            raise ValueError("Invalid h")

        frontier = [(0, self.start_state, [])]
        explored = set() # Keep track of explored states
        states_explored = 0

        while frontier:
            f_cost, state, moves = heapq.heappop(frontier)  # priority queue for A* search
            states_explored += 1

            if state == self.goal_state:
                return moves, len(moves), states_explored, nodes_generated

            explored.add(tuple(tuple(row) for row in state))

            for rule in self.APPRULES(state):
                successor = rule.action(state)
                if tuple(map(tuple, successor)) not in explored:
                    g_cost = len(moves) + 1  # g(n) = cost so far + 1
                    h_cost = h_func(successor)  # h(n) = heuristic cost
                    f_cost = g_cost + h_cost  # f(n) = g(n) + h(n)
                    heapq.heappush(frontier, (f_cost, successor, moves + [str(rule)]))
                    nodes_generated += 1

        return []  # No solution found


def main():
    puzzle = "problem-1.json"
    size, start_state, goal_state = read_JSON(puzzle)
    puzzle_instance = SlidingTilePuzzle(size, start_state, goal_state)

    print(f"Puzzle size: {size} x {size}")
    print(f"Puzzle start position: {start_state}")
    print(f"Puzzle goal position: {goal_state}")

    puzzle_instance.solve_backtracking()

    ucs_solution, ucs_cost, ucs_nodes_generated, ucs_nodes_examined = puzzle_instance.ucs_solve()

    if ucs_cost >= 0:
        print("\nUniform Cost Search Solution:")
        print("Solution length =", len(ucs_solution))
        print("Nodes generated:", ucs_nodes_generated)
        print("Nodes examined:", ucs_nodes_examined)
        print("Moves:", " -> ".join(ucs_solution))
    else:
        print("No solution found.")

    # Solve using A* search with heuristic h1
    astar_solution_h1, astar_cost_h1, nodes_explored_h1, nodes_generated_h1 = puzzle_instance.astar_solve("h1")

    if astar_cost_h1 >= 0:
        print("\nA* Search with Heuristic misplaced tiles:")
        print("Solution Length:", astar_cost_h1)
        print("Nodes generated:", nodes_generated_h1)
        print("Nodes examined: ", nodes_explored_h1)
        print("Moves:", " -> ".join(astar_solution_h1))
    else:
        print("No solution found with heuristic h1.")

    # Solve using A* search with heuristic h2
    astar_solution_h2, astar_cost_h2, nodes_explored_h2, nodes_generated_h2 = puzzle_instance.astar_solve("h2")

    if astar_cost_h2 >= 0:
        print("\nA* Search with Heuristic manhattan distance:")
        print("Solution Length:", astar_cost_h2)
        print("Nodes generated:", nodes_generated_h2)
        print("Nodes examined:", nodes_explored_h2)
        print("Moves:", " -> ".join(astar_solution_h2))
    else:
        print("No solution found with heuristic h2.")


if __name__ == "__main__":
    main()
