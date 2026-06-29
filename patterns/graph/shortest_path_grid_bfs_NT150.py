"""
Problem: Shortest Path in a Grid
Rapid Pattern Drill Problem 2
Pattern: BFS shortest path / levels
Status: Yellow-red review item

Prompt:
    Given a grid of 0s and 1s:
        0 = open cell
        1 = wall

    Find the shortest path from the top-left cell to the bottom-right cell,
    moving up, down, left, or right.

Core idea:
    A grid is a graph:
        each cell is a node
        valid neighboring cells are edges

    Shortest path in an unweighted graph/grid should use BFS, not DFS.

Main traps:
    - Check bounds before indexing into grid.
    - Mark visited when enqueueing, not only when dequeueing.
    - Queue stores row, col, and distance.
"""

from collections import deque


def shortest_path(grid: list[list[int]]) -> int:
    if not grid or not grid[0]:
        return -1

    rows = len(grid)
    cols = len(grid[0])

    if grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return -1

    queue = deque([(0, 0, 0)])  # row, col, distance
    visited = {(0, 0)}

    directions = [
        (1, 0),    # down
        (-1, 0),   # up
        (0, 1),    # right
        (0, -1),   # left
    ]

    while queue:
        row, col, distance = queue.popleft()

        if row == rows - 1 and col == cols - 1:
            return distance

        for row_delta, col_delta in directions:
            next_row = row + row_delta
            next_col = col + col_delta

            in_bounds = (
                0 <= next_row < rows
                and 0 <= next_col < cols
            )

            if not in_bounds:
                continue

            if grid[next_row][next_col] == 1:
                continue

            if (next_row, next_col) in visited:
                continue

            visited.add((next_row, next_col))
            queue.append((next_row, next_col, distance + 1))

    return -1


def main():
    assert shortest_path([[0]]) == 0
    assert shortest_path([[1]]) == -1
    assert shortest_path([[0, 0], [0, 0]]) == 2
    assert shortest_path([[0, 1], [1, 0]]) == -1
    assert shortest_path([[0, 0, 0], [1, 1, 0], [0, 0, 0]]) == 4
    print("All tests passed.")


if __name__ == "__main__":
    main()
