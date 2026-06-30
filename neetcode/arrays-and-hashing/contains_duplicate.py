"""
Problem: Contains Duplicate
Difficulty: Easy
Pattern: Array / Hash Set

Time: O(n)
Space: O(n)

Where:
n = number of integers in nums

Idea:
Maintain a set of seen numbers. If a number is already in the set,
return True. Otherwise, add it to the set and continue.
"""

from typing import List

class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False