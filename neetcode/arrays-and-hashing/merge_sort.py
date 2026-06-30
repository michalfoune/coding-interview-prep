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

Pseudocode:
merge_sort(nums):
    if nums has length 0 or 1:
        return nums

    split nums into left half and right half

    sorted_left = merge_sort(left half)
    sorted_right = merge_sort(right half)

    return merge(sorted_left, sorted_right)

merge(left, right):
    create empty result
    compare first remaining item of left and right
    append the smaller one
    move that pointer forward
    repeat until one side is empty
    append the remaining tail from the non-empty side
    return result

Core model:
Recursion creates sorted small pieces.
Merge builds sorted bigger pieces.
"""

from typing import List

class Solution:
    def merge_sort(self, nums: List[int]) -> List[int]:
        if len(nums) <=1:
            return nums
        mid = len(nums) // 2

        sorted_left = self.merge_sort(nums[:mid])
        sorted_right = self.merge_sort(nums[mid:])

        return self.merge(sorted_left, sorted_right)

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