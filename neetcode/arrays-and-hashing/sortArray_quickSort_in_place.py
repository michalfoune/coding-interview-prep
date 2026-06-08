"""
Problem: Sort Array — Quick Sort
Difficulty: Medium
Pattern: Divide and Conquer / Recursion / In-Place Partitioning

Time: O(n log n) average, O(n^2) worst case
Space: O(log n) average, O(n) worst case

Where:
n = number of integers in nums

Idea:
Choose a pivot value from the current range.
Use two pointers to partition the range in place:
move the left pointer until it finds a value >= pivot,
and move the right pointer until it finds a value <= pivot.
If the pointers have not crossed, swap those values and move both pointers inward.

After partitioning, values on the left side are generally <= pivot,
and values on the right side are generally >= pivot.
The two sides are not fully sorted yet.
Recursively apply the same process to the left and right ranges.
"""   

from typing import List

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        if len(nums) <= 1:
            return nums
        self.quickSort(nums, 0, len(nums) - 1)
        return nums
    
    def quickSort(self, nums: List[int], left: int, right: int):
        if left >= right:
            return
        i = left
        j = right
        pivot = nums[(left + right) // 2]
        while i <= j:
            while nums[i] < pivot:
                i += 1
            while nums[j] > pivot:
                j -= 1
            if i < j:
                temp = nums[i]
                nums[i] = nums[j]
                nums[j] = temp
        self.quickSort(nums, left, j) 
        self.quickSort(nums, i, right)