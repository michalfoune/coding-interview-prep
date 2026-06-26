from collections import Counter


def longest_normalized_session(events: str, max_replacements: int) -> int:
    """
    Return the length of the longest contiguous session that can be normalized
    to one repeated event type using at most max_replacements replacements.

    Example:
        events = "AABABBA", max_replacements = 1

        The window "AABA" can be normalized to "AAAA" by replacing one "B".
        Therefore the answer is 4.

    Approach:
        Sliding window / two pointers.

        For each window:
            window length - most common event count = replacements needed

        If replacements needed is too high, move the left pointer until the
        window becomes valid again.

    Time: O(n * d), where d is the number of distinct characters in the window,
          because max(counter.values()) scans the counts.
    Space: O(d)
    """
    if not events or max_replacements < 0:
        return 0

    counter = Counter()
    best_length = 0
    left = 0

    for right in range(len(events)):
        right_char = events[right]
        counter[right_char] += 1

        most_common_count = max(counter.values())
        window = right - left + 1

        while window - most_common_count > max_replacements:
            left_char = events[left]
            counter[left_char] -= 1

            if counter[left_char] == 0:
                del counter[left_char]

            left += 1
            window = right - left + 1
            most_common_count = max(counter.values())

        best_length = max(best_length, window)

    return best_length


def main():
    assert longest_normalized_session("", 1) == 0
    assert longest_normalized_session("A", 0) == 1
    assert longest_normalized_session("AAAA", 0) == 4
    assert longest_normalized_session("AABABBA", 1) == 4
    assert longest_normalized_session("AAABBC", 2) == 5
    assert longest_normalized_session("ABC", 0) == 1
    assert longest_normalized_session("ABC", 2) == 3
    assert longest_normalized_session("ABBB", 2) == 4
    assert longest_normalized_session("ABAB", 1) == 3
    assert longest_normalized_session("ABAB", -1) == 0

    print("All tests passed.")


if __name__ == "__main__":
    main()
