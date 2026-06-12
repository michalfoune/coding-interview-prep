class Node:
    """Represents a service in a reversed dependency graph."""

    def __init__(self, value: str):
        self.value = value
        self.children: list["Node"] = []


def impacted_services(root: Node | None) -> list[str]:
    """
    Return all services impacted by a failed service.

    The graph is assumed to be reversed:
    each node points to services that depend on it.

    Example:
        database -> inventory -> checkout -> frontend

    If database fails, inventory, checkout, and frontend are impacted.

    The failed service itself is not included in the result.

    Time: O(V + E)
    Space: O(V)

    V = number of reachable services
    E = number of dependency edges among reachable services
    """
    if root is None:
        return []

    result = []
    seen = set()
    failed_service = root

    def dfs(node: Node) -> None:
        if node in seen:
            return

        seen.add(node)

        if node is not failed_service:
            result.append(node.value)

        for child in node.children:
            dfs(child)

    dfs(root)
    return result


def main():
    frontend = Node("Frontend")
    auth = Node("Auth")
    checkout = Node("Checkout")
    payments = Node("Payments")
    inventory = Node("Inventory")
    database = Node("Database")
    recommendations = Node("Recommendations")
    admin = Node("Admin")

    # Create a reversed graph from the dependency graph:
    # dependency -> services that depend on it
    database.children.extend([inventory, recommendations])
    inventory.children.append(checkout)
    checkout.children.append(frontend)
    payments.children.append(checkout)
    auth.children.extend([frontend, admin])

    print(f"Impacted services: {impacted_services(database)}")


if __name__ == "__main__":
    main()