class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.is_command = False


class Trie:
    """
    Store and query commands using a trie / prefix tree.

    Supports adding commands, checking whether a full command exists, checking
    whether any command starts with a given prefix, and returning all commands
    that match a prefix. If the prefix is empty, return all commands.

    Each node stores its child nodes by character and a flag indicating whether
    a complete command ends at that node.

    add_command:
        Time: O(m)
        Space: O(m)

    has_prefix:
        Time: O(m)
        Space: O(1)

    has_command:
        Time: O(m)
        Space: O(1)
    
    get_commands:
        Time: O(m + k)
        Space: O(k + h)

    m = length of the command or prefix
    k = total size of returned commands
    h = maximum command length / recursion depth
    """

    def __init__(self):
        self.root = TrieNode()

    def add_command(self, command: str) -> None:
        node = self.root

        for char in command:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_command = True

    def has_prefix(self, prefix: str) -> bool:
        node = self.root

        for char in prefix:
            if char not in node.children:
                return False

            node = node.children[char]

        return True

    def has_command(self, command: str) -> bool:
        node = self.root

        for char in command:
            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_command

    def get_commands(self, prefix: str) -> list[str]:
        node = self.root

        for char in prefix:
            if char not in node.children:
                return []

            node = node.children[char]

        result = []

        def dfs(current_node: TrieNode, current_command: str) -> None:
            if current_node.is_command:
                result.append(current_command)

            for character, child in current_node.children.items():
                dfs(child, current_command + character)

        dfs(node, prefix)
        return result


def main():
    trie = Trie()

    commands = [
        "deploy",
        "deploy_canary",
        "deploy_rollback",
        "delete_user",
        "describe_service",
        "restart_service",
        "restore_backup",
    ]

    for command in commands:
        trie.add_command(command)

    print(trie.has_command("deploy"))          # True
    print(trie.has_command("deplo"))           # False
    print(trie.has_prefix("dep"))              # True
    print(trie.has_prefix("backup"))           # False

    print(trie.get_commands("deploy"))
    print(trie.get_commands("de"))
    print(trie.get_commands(""))
    print(trie.get_commands("unknown"))


if __name__ == "__main__":
    main()