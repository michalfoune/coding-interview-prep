"""
Problem: Majority Element
Difficulty: Easy
Pattern: Sorting

Time: O(n log n)
Space: O(1) or O(n), depending on how Python's sort internals are counted

Where:
n = number of integers in nums

Idea:
Sort the array in ascending order. Since the majority element appears more
than n / 2 times, it must occupy the middle index after sorting.
"""

from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        nums.sort()
        return nums[len(nums) // 2]