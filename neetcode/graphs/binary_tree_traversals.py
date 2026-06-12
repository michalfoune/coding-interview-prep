class Node:
    def __init__(self, value: str):
        self.value = value
        self.left = None
        self.right = None


def preorder(root: Node | None) -> list[str]:
    result = []

    def dfs(node: Node | None) -> None:
        if node is None:
            return

        result.append(node.value)
        dfs(node.left)
        dfs(node.right)

    dfs(root)
    return result


def inorder(root: Node | None) -> list[str]:
    result = []

    def dfs(node: Node | None) -> None:
        if node is None:
            return

        dfs(node.left)
        result.append(node.value)
        dfs(node.right)

    dfs(root)
    return result


def postorder(root: Node | None) -> list[str]:
    result = []

    def dfs(node: Node | None) -> None:
        if node is None:
            return

        dfs(node.left)
        dfs(node.right)
        result.append(node.value)

    dfs(root)
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

    print(f"preorder:  {preorder(A)}")
    print(f"inorder:   {inorder(A)}")
    print(f"postorder: {postorder(A)}")


if __name__ == "__main__":
    main()