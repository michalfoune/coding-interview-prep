from collections import defaultdict


def can_reach(
    calls: list[tuple[str, str]],
    start_service: str,
    target_service: str,
) -> bool:
    """
    Return True if target_service is reachable from start_service.

    Each tuple in calls is (caller, callee), meaning caller can call callee.
    The search follows directed edges from caller to callee.

    A service is considered reachable from itself.

    Uses DFS with a visited set to avoid infinite loops in graphs with cycles.

    Time: O(V + E)
    Space: O(V + E)

    V = number of services
    E = number of call relationships
    """
    graph = defaultdict(list)

    for caller, callee in calls:
        graph[caller].append(callee)

    visited = set()

    def dfs(service: str) -> bool:
        if service == target_service:
            return True

        if service in visited:
            return False

        visited.add(service)

        for neighbor in graph.get(service, []):
            if dfs(neighbor):
                return True

        return False

    return dfs(start_service)


def main():
    calls = [
        ("frontend", "checkout"),
        ("frontend", "auth"),
        ("checkout", "payments"),
        ("checkout", "inventory"),
        ("inventory", "database"),
        ("recommendations", "database"),
        ("admin", "auth"),
    ]

    test_cases = [
        ("frontend", "database", True),
        ("auth", "database", False),
        ("recommendations", "database", True),
        ("frontend", "frontend", True),
    ]

    for start_service, target_service, expected in test_cases:
        actual = can_reach(calls, start_service, target_service)
        print(
            f"{start_service} can reach {target_service}: "
            f"{actual} | expected: {expected}"
        )


if __name__ == "__main__":
    main()