"""
Problem: Valid Palindrome II
Difficulty: Easy
Pattern: String / Two Pointers

Time: O(n)
Space: O(1)

Where:
n = length of the string

Idea:
Use two pointers from both ends of the string.
While the characters match, move both pointers inward.
At the first mismatch, we may delete one character, so try skipping either the left
character or the right character.
If either remaining range is a palindrome, return True.
Otherwise, return False.
"""

class Solution:
    def validPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            if s[left] == s[right]:
                left += 1
                right -= 1
            else:
                return (
                    self.isPalindrome(s, left, right - 1) or
                    self.isPalindrome(s, left + 1, right)
                )

        return True

    def isPalindrome(self, s: str, left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False

            left += 1
            right -= 1

        return True