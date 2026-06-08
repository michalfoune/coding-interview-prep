"""
Problem: Sort Array — Merge Sort
Difficulty: Medium
Pattern: Divide and Conquer / Recursion

Time: O(n log n)
Space: O(n)

Where:
n = number of integers in nums

Idea:
Recursively divide the array into two halves.
Sort each half.
Merge the two sorted halves by repeatedly taking the smaller front element.
"""

from typing import List

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <=1:
            return nums
        mid = len(nums) // 2

        left = self.sortArray(nums[:mid])
        right = self.sortArray(nums[mid:])

        return self.merge(left, right)

    def merge(self, left: List[int], right: List[int]) -> List[int]:
        i = 0
        j = 0
        result = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result