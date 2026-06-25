from collections import defaultdict


def longest_stable_session(events: str, max_distinct: int) -> int:
    """
    Return the length of the longest contiguous session with at most
    max_distinct distinct event types.

    Assignment:
    You are given a string where each character represents one event type.
    A stable session is a contiguous substring containing at most max_distinct
    distinct characters.

    Rules:
    - The substring must be contiguous.
    - Return only the length, not the substring itself.
    - If events is empty, return 0.
    - If max_distinct <= 0, return 0.
    - Treat characters as case-sensitive.

    Approach:
    Use a sliding window with left/right pointers.
    Expand the window with right.
    If the window has too many distinct characters, move left forward until
    the window is valid again.

    Time: O(n)
    Space: O(k), where k is the number of distinct characters in the window.
    """
    if not events or max_distinct <= 0:
        return 0

    counts = defaultdict(int)
    left = 0
    max_length = 0

    for right in range(len(events)):
        right_char = events[right]
        counts[right_char] += 1

        while len(counts) > max_distinct:
            left_char = events[left]
            counts[left_char] -= 1

            if counts[left_char] == 0:
                del counts[left_char]

            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length


def main():
    assert longest_stable_session("ABAC", 2) == 3
    assert longest_stable_session("ABAABABABABA", 2) == 12
    assert longest_stable_session("", 2) == 0
    assert longest_stable_session("ABAC", 0) == 0
    assert longest_stable_session("ABCSAAAAAEEEAAAVVV", 3) == 14

    print("All tests passed.")


if __name__ == "__main__":
    main()