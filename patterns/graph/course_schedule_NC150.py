"""
Problem: Course Schedule
Source: NeetCode 150 rapid review
Difficulty: Medium
Pattern: Directed graph + DFS cycle detection
Status: Correct final implementation

Prompt:
    You are given:
        num_courses: int
        prerequisites: list[list[int]]

    Each prerequisite pair has the shape:

        [course, prerequisite]

    Meaning:
        To take `course`, you must first take `prerequisite`.

    Return True if it is possible to finish all courses.
    Return False if the prerequisite graph contains a cycle.

Core idea:
    Model the courses as a directed graph.

    This implementation uses the direction:

        course -> prerequisites

    That means DFS asks:

        "Can I finish all prerequisites of this course without hitting a cycle?"

DFS states:
    visiting:
        Nodes currently on the active DFS path.

    visited:
        Nodes that have already been fully processed and proven safe.

    If DFS reaches a node already in `visiting`, we found a cycle.

    If DFS reaches a node already in `visited`, it is safe to return True
    immediately because that node and everything below it were already checked.

Why num_courses is needed:
    num_courses gives the full universe of courses:

        0, 1, 2, ..., num_courses - 1

    We run DFS from every course to handle disconnected components.

Time:
    O(V + E)

Space:
    O(V + E)
"""

from collections import defaultdict


def can_finish(
    num_courses: int,
    prerequisites: list[list[int]]
) -> bool:
    """
    Return True if all courses can be finished; otherwise return False.

    Uses DFS cycle detection on a directed graph.

    Graph direction:
        course -> prerequisites

    Cycle detection:
        - `visiting` means the node is currently on the DFS path.
        - `visited` means the node and all its prerequisites are already safe.
    """
    graph: dict[int, set[int]] = defaultdict(set)
    visiting = set()
    visited = set()

    for dependent, dependency in prerequisites:
        graph[dependent].add(dependency)

    def dfs(node: int) -> bool:
        if node in visiting:
            return False

        if node in visited:
            return True

        visiting.add(node)

        for prereq in graph.get(node, set()):
            if not dfs(prereq):
                return False

        visiting.discard(node)
        visited.add(node)

        return True

    for course in range(num_courses):
        if not dfs(course):
            return False

    return True


def main():
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False
    assert can_finish(4, [[1, 0], [2, 1], [3, 2]]) is True
    assert can_finish(4, [[1, 0], [2, 1], [1, 2]]) is False
    assert can_finish(4, [[1, 0], [2, 3], [3, 2]]) is False
    assert can_finish(4, [[1, 0]]) is True
    assert can_finish(3, []) is True
    assert can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True

    print("All tests passed.")


if __name__ == "__main__":
    main()
