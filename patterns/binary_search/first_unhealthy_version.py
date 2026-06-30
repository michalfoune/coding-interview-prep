def make_is_healthy(versions: list[bool]):
    """
    Create an is_healthy(version) function for testing.

    Versions in the main algorithm are 1-based:
        version 1 -> versions[0]
        version 2 -> versions[1]
        ...
    """
    def is_healthy(version: int) -> bool:
        return versions[version - 1]

    return is_healthy


def find_first_unhealthy_version(n: int, is_healthy) -> int:
    """
    Return the first unhealthy version in versions 1..n.

    The health pattern is monotonic:
        healthy, healthy, healthy, unhealthy, unhealthy, ...

    Once a version is unhealthy, every later version is also unhealthy.

    If all versions are healthy, return -1.
    If n <= 0, return -1.

    Approach:
        Binary search for the first False value.

        - If mid is healthy, the first unhealthy version must be to the right.
        - If mid is unhealthy, mid is a candidate answer, but there may be an
          earlier unhealthy version to the left.

    Time: O(log n)
    Space: O(1)
    """
    if n <= 0:
        return -1

    left = 1
    right = n
    first = -1

    while left <= right:
        mid = (left + right) // 2

        if is_healthy(mid):
            left = mid + 1
        else:
            first = mid
            right = mid - 1

    return first


def find_first_unhealthy_version_v2(n: int, is_healthy) -> int:
    if n <= 0:
        return -1

    left = 1
    right = n

    while left < right:
        mid = (left + right) // 2

        if is_healthy(mid):
            # mid is healthy, so first unhealthy must be after mid
            left = mid + 1
        else:
            # mid is unhealthy, so mid could be the first unhealthy
            # keep it as a candidate
            right = mid

    # left == right here
    if is_healthy(left):
        return -1

    return left


def main():
    is_healthy_v1 = make_is_healthy([True, True, False, False])
    is_healthy_v2 = make_is_healthy([True, True, True, True, False, False])
    all_healthy = make_is_healthy([True, True, True, True])
    all_unhealthy = make_is_healthy([False, False, False])
    one_healthy = make_is_healthy([True])
    one_unhealthy = make_is_healthy([False])

    assert find_first_unhealthy_version(4, is_healthy_v1) == 3
    assert find_first_unhealthy_version(2, is_healthy_v1) == -1
    assert find_first_unhealthy_version(6, is_healthy_v2) == 5
    assert find_first_unhealthy_version(4, all_healthy) == -1
    assert find_first_unhealthy_version(3, all_unhealthy) == 1
    assert find_first_unhealthy_version(1, one_healthy) == -1
    assert find_first_unhealthy_version(1, one_unhealthy) == 1
    assert find_first_unhealthy_version(0, is_healthy_v2) == -1
    assert find_first_unhealthy_version(-3, is_healthy_v2) == -1

    print("All tests passed.")


if __name__ == "__main__":
    main()
