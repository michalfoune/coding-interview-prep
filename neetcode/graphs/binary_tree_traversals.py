class Node:
    def __init__(self, value: str):
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def preorder(root: Node | None) -> list[str]:
    """
    Preorder depth-first traversal of a binary tree.

    Visit order:
    root -> left -> right

    Time: O(n)
    Space: O(h) recursion stack, O(n) including output

    n = number of nodes in the tree
    h = height of the tree

    Idea:
    Visit the current node first, then recursively traverse the left subtree,
    then recursively traverse the right subtree.
    """
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
    """
    Inorder depth-first traversal of a binary tree.

    Visit order:
    left -> root -> right

    Time: O(n)
    Space: O(h) recursion stack, O(n) including output

    n = number of nodes in the tree
    h = height of the tree

    Idea:
    Recursively traverse the left subtree first, then visit the current node,
    then recursively traverse the right subtree.
    """
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
    """
    Postorder depth-first traversal of a binary tree.

    Visit order:
    left -> right -> root

    Time: O(n)
    Space: O(h) recursion stack, O(n) including output

    n = number of nodes in the tree
    h = height of the tree

    Idea:
    Recursively traverse the left subtree first, then the right subtree,
    then visit the current node last.
    """
    result = []

    def dfs(node: Node | None) -> None:
        if node is None:
            return

        dfs(node.left)
        dfs(node.right)
        result.append(node.value)

    dfs(root)
    return result


def preorder_simple(root: Node | None) -> list[str]:
    """
    Compact recursive preorder traversal.

    Visit order:
    root -> left -> right

    Time: O(n) if ignoring list concatenation cost; can degrade to O(n^2)
    Space: O(h) recursion stack, O(n) including output

    Idea:
    This version is useful as a memory anchor:
    preorder = root + left + right

    It is less efficient than the accumulator version because each `+`
    creates a new list.
    """
    if root is None:
        return []

    return [root.value] + preorder_simple(root.left) + preorder_simple(root.right)


def inorder_simple(root: Node | None) -> list[str]:
    """
    Compact recursive inorder traversal.

    Visit order:
    left -> root -> right

    Time: O(n) if ignoring list concatenation cost; can degrade to O(n^2)
    Space: O(h) recursion stack, O(n) including output

    Idea:
    This version is useful as a memory anchor:
    inorder = left + root + right

    It is less efficient than the accumulator version because each `+`
    creates a new list.
    """
    if root is None:
        return []

    return inorder_simple(root.left) + [root.value] + inorder_simple(root.right)


def postorder_simple(root: Node | None) -> list[str]:
    """
    Compact recursive postorder traversal.

    Visit order:
    left -> right -> root

    Time: O(n) if ignoring list concatenation cost; can degrade to O(n^2)
    Space: O(h) recursion stack, O(n) including output

    Idea:
    This version is useful as a memory anchor:
    postorder = left + right + root

    It is less efficient than the accumulator version because each `+`
    creates a new list.
    """
    if root is None:
        return []

    return postorder_simple(root.left) + postorder_simple(root.right) + [root.value]


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

    print(f"preorder simple:  {preorder_simple(A)}")
    print(f"inorder simple:   {inorder_simple(A)}")
    print(f"postorder simple: {postorder_simple(A)}")


if __name__ == "__main__":
    main()
