"""
Problem: Majority Element
Difficulty: Easy
Pattern: Boyer-Moore Voting Algorithm

Time: O(n)
Space: O(1)

Where:
n = number of integers in nums

Idea:
Maintain a candidate and a counter. When the counter reaches 0, choose the
current number as the new candidate. If the current number matches the
candidate, increment the counter; otherwise decrement it.

Because the problem guarantees that a majority element exists, the final
candidate is the majority element.

Logic: "Only the winner can sustain the subtractions" or 
Boyer-Moore works because the true majority element is the only value that can survive all the “cancellations.”
"""

from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        candidate = None
        count = 0

        for num in nums:
            if count == 0:
                candidate = num

            if num == candidate:
                count += 1
            else:
                count -= 1

        return candidate