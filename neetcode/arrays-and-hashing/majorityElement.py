"""
Problem: Majority Element
Difficulty: Easy
Pattern: Hash Map / Frequency Count

Time: O(n)
Space: O(n)

Where:
n = number of integers in nums

Idea:
Build a frequency dictionary while iterating through nums.
As soon as any number appears more than n / 2 times, return that number.
The problem guarantees that a majority element always exists.
"""

from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        majority = len(nums) // 2 + 1
        freq = {}
        for n in nums:
            freq[n] = freq.get(n, 0) + 1
            if freq[n] >= majority:
                return n