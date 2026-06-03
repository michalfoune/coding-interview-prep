"""
Problem: Group Anagrams
Difficulty: Medium
Pattern: Hash Map / Sorting

Time: O(n * k log k)
Space: O(n * k)

Where:
n = number of words
k = maximum length of a word

Idea:
Sort each word to create a canonical key.
Words with the same canonical key are anagrams and belong in the same group.
"""

from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groups = defaultdict(list)

        for s in strs:
            canonical_key = ''.join(sorted(s))
            groups[canonical_key].append(s)

        return list(groups.values())