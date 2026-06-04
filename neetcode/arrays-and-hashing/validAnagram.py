"""
Problem: Valid Anagram
Difficulty: Easy
Pattern: Hash Map / Frequency Count

Time: O(n)
Space: O(n)

Where:
n = length of the strings

Idea:
If the strings have different lengths, return False.
Otherwise, count the characters in the first string, then subtract counts
while iterating over the second string. If a character is missing or its
count becomes negative, return False. Otherwise, return True.
"""

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        counts = {}
        for ch in s:
            counts[ch] = counts.get(ch, 0) + 1

        for ch in t:
            if ch not in counts:
                return False
            counts[ch] -= 1
            if counts[ch] < 0:
                return False

        return True