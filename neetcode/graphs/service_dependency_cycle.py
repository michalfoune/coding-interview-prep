from collections import defaultdict


def has_cycle_defaultdict(dependencies: list[tuple[str, str]]) -> bool:
    """
    Detect circular service dependencies using DFS and a defaultdict adjacency list.

    Each pair is (service, dependency), meaning service depends on dependency.

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)

    for service, dependency in dependencies:
        graph[service].append(dependency)

    visiting = set()
    visited = set()

    def dfs(service: str) -> bool:
        if service in visiting:
            return True

        if service in visited:
            return False

        visiting.add(service)

        for dependency in graph[service]:
            if dfs(dependency):
                return True

        visiting.remove(service)
        visited.add(service)
        return False

    for service in graph:
        if dfs(service):
            return True

    return False


def has_cycle_standard_dict(dependencies: list[tuple[str, str]]) -> bool:
    """
    Detect circular service dependencies using DFS and a standard dict adjacency list.

    Each pair is (service, dependency), meaning service depends on dependency.

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = {}

    for service, dependency in dependencies:
        if service not in graph:
            graph[service] = []
        graph[service].append(dependency)

    visiting = set()
    visited = set()

    def dfs(service: str) -> bool:
        if service in visiting:
            return True

        if service in visited:
            return False

        visiting.add(service)

        for dependency in graph.get(service, []):
            if dfs(dependency):
                return True

        visiting.remove(service)
        visited.add(service)
        return False

    for service in graph:
        if dfs(service):
            return True

    return False


def main():
    dependencies1 = [
        ("frontend", "checkout"),
        ("frontend", "auth"),
        ("checkout", "payments"),
        ("checkout", "inventory"),
        ("inventory", "database"),
        ("recommendations", "database"),
        ("admin", "auth"),
    ]

    dependencies2 = [
        ("frontend", "checkout"),
        ("checkout", "inventory"),
        ("inventory", "database"),
        ("database", "checkout"),
    ]

    print(f"1st scenario has cycle: {has_cycle_defaultdict(dependencies1)}")
    print(f"2nd scenario has cycle: {has_cycle_defaultdict(dependencies2)}")

    print(f"1st scenario has cycle, standard dict: {has_cycle_standard_dict(dependencies1)}")
    print(f"2nd scenario has cycle, standard dict: {has_cycle_standard_dict(dependencies2)}")


if __name__ == "__main__":
    main()