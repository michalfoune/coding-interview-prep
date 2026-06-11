from collections import deque


class Node:
    def __init__(self, val: str):
        self.val = val
        self.left = None
        self.right = None


def bfs(root: Node | None) -> list[str]:
    """
    Breadth-first search / level-order traversal of a binary tree.

    Time: O(n)
    Space: O(n)

    n = number of nodes in the tree

    Idea:
    Use a queue (FIFO). Start with the root. Repeatedly remove the oldest
    discovered node, add its value to the result, then append its left and
    right children if they exist.
    """
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
    """
    Depth-first search / preorder traversal of a binary tree.

    Time: O(n)
    Space: O(n)

    n = number of nodes in the tree

    Idea:
    Use a stack (LIFO). Start with the root. Repeatedly remove the most
    recently discovered node, add its value to the result, then push right
    before left so the left child is processed first.
    """
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