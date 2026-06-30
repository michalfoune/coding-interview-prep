"""
Problem: Remove Element
Difficulty: Easy
Pattern: Array / Two Pointers

Time: O(n)
Space: O(1)

Where:
n = number of integers in nums

Idea:
Use k as the position where the next kept value should be written.
Iterate through nums. Whenever nums[i] is different from val, copy it to
nums[k] and increment k. After the loop, the first k elements contain the
values that should remain.
"""

from typing import List

class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        k = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[k] = nums[i]
                k += 1
        return k