import unittest
from main import SlidingTilePuzzle

class TestSlidingTilePuzzle(unittest.TestCase):
    def test_basic_functionality(self):
        # Test basic functionality with a simple puzzle
        size = 3
        start_state = [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        puzzle_instance = SlidingTilePuzzle(size, start_state, goal_state)

        # Solve the puzzle
        solution = puzzle_instance.solve_backtracking()

        # Apply the solution to the start state
        final_state = start_state
        for move in solution:
            final_state = puzzle_instance.successor_state(final_state, move)

        # Assert that the final state matches the goal state
        self.assertEqual(final_state, goal_state)

    def test_edge_cases(self):
        # Test edge cases with minimum and maximum dimensions
        min_size = 2
        max_size = 5
        min_start_state = [[0] * min_size] * min_size
        max_start_state = [[0] * max_size] * max_size
        goal_state = [[1, 2], [3, 0]]  # Example goal state for minimum size

        # Solve the puzzle for minimum size
        puzzle_instance_min = SlidingTilePuzzle(min_size, min_start_state, goal_state)
        solution_min = puzzle_instance_min.solve_backtracking()
        final_state_min = min_start_state
        if solution_min:
            for move in solution_min:
                final_state_min = puzzle_instance_min.successor_state(final_state_min, move)

        # Assert that the final state matches the goal state (if solution exists)
        if solution_min:
            self.assertEqual(final_state_min, goal_state)

        # Solve the puzzle for maximum size
        puzzle_instance_max = SlidingTilePuzzle(max_size, max_start_state, goal_state)
        solution_max = puzzle_instance_max.solve_backtracking()
        final_state_max = max_start_state
        if solution_max:
            for move in solution_max:
                final_state_max = puzzle_instance_max.successor_state(final_state_max, move)

        # No solution expected for maximum size, so final state should remain unchanged
        if solution_max:
            self.assertEqual(final_state_max, max_start_state)

if __name__ == '__main__':
    unittest.main()
