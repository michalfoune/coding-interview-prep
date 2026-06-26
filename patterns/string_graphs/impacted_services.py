from collections import defaultdict


def impacted_services(rules: list[str], changed_service: str) -> list[str]:
    """
    Return all services transitively impacted by a changed service.

    Each rule has the form:
        "dependent -> dependency"

    Example:
        "api -> auth" means api depends on auth.
        If auth changes, api may be impacted.

    Approach:
        Build a reverse dependency graph:
            dependency -> list of dependents

        Then run DFS from changed_service to find all reachable dependents.

    The returned list:
        - excludes changed_service itself
        - contains each impacted service once
        - is sorted alphabetically for deterministic output

    Time: O(V + E + R log R), where R is the number of impacted services.
    Space: O(V + E)
    """
    if not rules or not changed_service:
        return []

    graph: dict[str, list[str]] = defaultdict(list)

    for rule in rules:
        dependent, dependency = [part.strip() for part in rule.split("->")]
        graph[dependency].append(dependent)

    visited = {changed_service}
    impacted = set()

    def dfs(service: str) -> None:
        for dependent in graph.get(service, []):
            if dependent in visited:
                continue

            visited.add(dependent)
            impacted.add(dependent)
            dfs(dependent)

    dfs(changed_service)

    return sorted(impacted)


def main():
    rules = [
        "api -> auth",
        "auth -> db",
        "frontend -> api",
        "worker -> queue",
    ]

    assert impacted_services(rules, "db") == ["api", "auth", "frontend"]
    assert impacted_services(rules, "auth") == ["api", "frontend"]
    assert impacted_services(rules, "queue") == ["worker"]
    assert impacted_services(rules, "worker") == []
    assert impacted_services([], "db") == []
    assert impacted_services(rules, "") == []

    rules_with_spaces = [
        "api->auth",
        "frontend   ->   api",
        "auth -> db",
    ]

    assert impacted_services(rules_with_spaces, "db") == [
        "api",
        "auth",
        "frontend",
    ]

    rules_with_cycle = [
        "api -> auth",
        "auth -> api",
        "frontend -> api",
    ]

    assert impacted_services(rules_with_cycle, "auth") == ["api", "frontend"]

    rules_with_multiple_paths = [
        "api -> db",
        "worker -> db",
        "frontend -> api",
        "frontend -> worker",
    ]

    assert impacted_services(rules_with_multiple_paths, "db") == [
        "api",
        "frontend",
        "worker",
    ]

    print("All tests passed.")


if __name__ == "__main__":
    main()
