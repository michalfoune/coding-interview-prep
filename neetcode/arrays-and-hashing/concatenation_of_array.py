"""
Problem: Concatenation of Array
Difficulty: Easy
Pattern: Array

Time: O(n)
Space: O(n)

Where:
n = number of integers in nums

Idea:
Return a new array containing nums followed by another copy of nums.
"""

from typing import List

class Solution:
    def getConcatenation(self, nums: List[int]) -> List[int]:
        return nums + nums