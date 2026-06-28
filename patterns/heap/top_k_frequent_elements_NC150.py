"""
Problem: Top K Frequent Elements
Source: NeetCode 150 rapid review
Difficulty: Medium
Mode: Rapid-fire implementation
Authorship: Written by me after discussing the approach; heap version corrected to return only values.
Date: 2026-06-27
Pattern: Counter + sorting / Counter + heap
Status: Correct 10/10 after one small fix in the heap version

Prompt:
    Given a list of strings, return the k most frequent strings.

Sorting rule:
    1. Higher frequency first
    2. Alphabetical order for ties

Examples:
    ["api", "db", "api", "auth", "db", "api"], k=2
    -> ["api", "db"]

    ["b", "a", "c", "a", "b", "c"], k=2
    -> ["a", "b"]
"""

import heapq
from collections import Counter


def top_k_frequent_sort(values: list[str], k: int) -> list[str]:
    """
    Simple and interview-readable solution.

    Count values, then sort unique values by:
    - frequency descending
    - value ascending

    Time:
        O(n + u log u)

    Space:
        O(u)

    where:
        n = total number of values
        u = number of unique values
    """
    if not values or k <= 0:
        return []

    counts = Counter(values)

    sorted_items = sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0]),
    )

    return [value for value, count in sorted_items[:k]]


def top_k_frequent_heap(values: list[str], k: int) -> list[str]:
    """
    Heap-based solution.

    Python heapq is a min-heap, so we store (-count, value).

    Why:
        - lower negative count means higher real count
        - value gives alphabetical tie-break

    Example:
        count 3 -> -3
        count 2 -> -2

        -3 is smaller than -2, so count 3 pops first.

    Time:
        O(n + u log u + k log u) with repeated heappush

    Space:
        O(u)

    Note:
        This version builds a heap of all unique values. It is useful for
        understanding the heap pattern, though for this exact tie-break rule
        the sorting solution is often simpler and just as defensible.
    """
    if not values or k <= 0:
        return []

    counts = Counter(values)
    heap = []
    result = []

    for value, count in counts.items():
        heapq.heappush(heap, (-count, value))

    for _ in range(min(k, len(heap))):
        count, value = heapq.heappop(heap)
        result.append(value)

    return result


def main():
    test_cases = [
        (
            ["api", "db", "api", "auth", "db", "api"],
            2,
            ["api", "db"],
        ),
        (
            ["b", "a", "c", "a", "b", "c"],
            2,
            ["a", "b"],
        ),
        (
            [],
            3,
            [],
        ),
        (
            ["api"],
            0,
            [],
        ),
        (
            ["api", "api"],
            5,
            ["api"],
        ),
        (
            ["z", "x", "z", "a", "a", "x", "b"],
            3,
            ["a", "x", "z"],
        ),
        (
            ["db", "api", "cache", "db", "api", "api", "cache", "cache"],
            2,
            ["api", "cache"],
        ),
    ]

    for values, k, expected in test_cases:
        assert top_k_frequent_sort(values, k) == expected
        assert top_k_frequent_heap(values, k) == expected

    print("All tests passed.")


if __name__ == "__main__":
    main()
