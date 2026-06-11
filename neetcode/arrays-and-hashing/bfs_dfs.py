from collections import deque


class Node:
    def __init__(self, val: str):
        self.val = val
        self.left = None
        self.right = None


def bfs(root: Node | None) -> list[str]:
    if root is None:
        return []

    q = deque([root])
    result = []

    while q:
        node = q.popleft()
        result.append(node.val)

        if node.left is not None:
            q.append(node.left)

        if node.right is not None:
            q.append(node.right)

    return result


def dfs(root: Node | None) -> list[str]:
    if root is None:
        return []

    stack = [root]
    result = []

    while stack:
        node = stack.pop()
        result.append(node.val)

        if node.right is not None:
            stack.append(node.right)

        if node.left is not None:
            stack.append(node.left)

    return result


def main():
    A = Node("A")
    B = Node("B")
    C = Node("C")
    D = Node("D")
    E = Node("E")
    F = Node("F")

    A.left = B
    A.right = C
    B.left = D
    B.right = E
    C.left = F

    print(f"BFS: {bfs(A)}")
    print(f"DFS: {dfs(A)}")


if __name__ == "__main__":
    main()