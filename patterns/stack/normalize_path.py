def normalize_path(path: str) -> str:
    """
    Normalize a Unix-like absolute path.

    Rules:
    - "." means current directory and is ignored.
    - ".." means move up one directory.
    - Multiple slashes are treated as one slash.
    - Going above root stays at root.
    - The result always starts with "/".
    - The result does not end with "/" unless it is root.

    Approach:
    Use a list as a stack of valid path components.

    Time: O(n), where n is the length of the path.
    Space: O(k), where k is the number of path components kept in the stack.
    """
    stack = []

    for part in path.split("/"):
        if not part or part == ".":
            continue

        if part == "..":
            if stack:
                stack.pop()
            continue

        stack.append(part)

    return "/" + "/".join(stack)


def main():
    assert normalize_path("/services/api/../auth/./v1") == "/services/auth/v1"
    assert normalize_path("/a//b////c") == "/a/b/c"
    assert normalize_path("/a/b/../../..") == "/"
    assert normalize_path("/") == "/"
    assert normalize_path("/../") == "/"
    assert normalize_path("/././.") == "/"
    assert normalize_path("//oracle///security/./api/") == "/oracle/security/api"
    assert normalize_path("/services/api/../../auth//v2") == "/auth/v2"

    print("All tests passed.")


if __name__ == "__main__":
    main()
