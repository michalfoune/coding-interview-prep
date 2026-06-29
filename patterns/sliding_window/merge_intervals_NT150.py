"""
Problem: Merge Intervals
Rapid Pattern Drill Problem 3
Pattern: Intervals / sort then merge
Status: Green review item

Prompt:
    Given a list of intervals, merge all overlapping intervals.
    Touching intervals count as overlapping:
        [1, 4] and [4, 5] -> [1, 5]

Core idea:
    Sort intervals by start.
    Keep a result list of merged intervals.
    For each interval:
        - if it starts after the last merged interval ends, append it
        - otherwise merge by extending the last merged end
"""


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    intervals = sorted(intervals, key=lambda item: item[0])
    merged = []

    for start, end in intervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)

    return merged


def main():
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6], [8, 10], [15, 18]
    ]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge_intervals([]) == []
    assert merge_intervals([[5, 7]]) == [[5, 7]]
    assert merge_intervals([[5, 7], [1, 3], [2, 4]]) == [[1, 4], [5, 7]]
    print("All tests passed.")


if __name__ == "__main__":
    main()
