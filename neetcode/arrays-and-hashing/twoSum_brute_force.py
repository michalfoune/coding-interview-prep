"""
Problem: Two Sum
Difficulty: Easy
Pattern: Array / Brute Force

Time: O(n²)
Space: O(1)

Where:
n = number of integers in nums

Idea:
Iterate over the array. For each number, compare it with every following number.
When the sum of the two numbers equals the target, return their indices.
Based on the assignment constraints, exactly one valid pair exists.
"""

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]