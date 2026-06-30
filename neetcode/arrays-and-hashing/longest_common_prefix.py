"""
Problem: Longest Common Prefix
Difficulty: Easy
Pattern: Arrays / Strings

Time: O(n * k)
Space: O(1)

Where:
n = number of strings
k = length of the shortest string

Idea:
Use the shortest string length as the maximum possible prefix length.
Compare characters at the same index across all strings.
At the first mismatch, return the prefix before that index.
If no mismatch is found, the shortest string is the common prefix.
"""

from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        min_len = min(len(s) for s in strs)

        for i in range(min_len):
            char = strs[0][i]

            for s in strs:
                if s[i] != char:
                    return strs[0][:i]

        return strs[0][:min_len]