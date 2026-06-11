"""
Problem: Merge Intervals
Difficulty: Medium
Pattern: Sorting / Intervals

Time: O(n log n)
Space: O(n)

Where:
n = number of intervals

Idea:
Sort intervals by start.
Keep a list of merged intervals.
If the current interval overlaps with the last merged interval, extend the end.
Otherwise, append it as a new interval.
"""

from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        intervals.sort(key=lambda interval: interval[0])

        merged = [intervals[0]]

        for i in range(1, len(intervals)):
            start = intervals[i][0]
            end = intervals[i][1]

            if start <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], end)
            else:
                merged.append(intervals[i])

        return merged