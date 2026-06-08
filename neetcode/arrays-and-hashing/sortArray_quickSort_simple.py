"""
Problem: Sort Array — Quick Sort
Difficulty: Medium
Pattern: Divide and Conquer / Recursion

Time: O(n log n) average, O(n^2) worst case
Space: O(n) average, O(n^2) worst case due to recursion/list allocation behavior

Where:
n = number of integers in nums

Idea:
Choose a pivot from the current list.
Partition the elements into three groups: smaller than, equal to, and greater than the pivot.
Recursively sort the smaller and greater groups.
Combine the sorted left group, equal group, and sorted right group.
"""

from typing import List

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums
        
        pivot = nums[len(nums) // 2]

        left = [x for x in nums if x < pivot]
        middle = [x for x in nums if x == pivot]
        right = [x for x in nums if x > pivot]

        return self.sortArray(left) + middle + self.sortArray(right)