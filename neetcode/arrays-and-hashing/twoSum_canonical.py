"""
Problem: Two Sum
Difficulty: Easy
Pattern: Hash Map

Time: O(n)
Space: O(n)

Where:
n = number of integers in nums

Idea:
Iterate over nums and store each number with its index in a hash map.
For each number, compute the needed complement: target - num.
If the complement already exists in the map, return both indices.
"""

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i