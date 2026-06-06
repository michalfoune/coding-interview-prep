"""
Problem: Design HashMap
Difficulty: Easy
Pattern: Hash Table / Direct Addressing

Time:
put: O(1)
get: O(1)
remove: O(1)

Space: O(m)

Where:
m = key range size, here 1,000,001

Idea:
Use a fixed-size array where each key maps directly to an index.
This avoids collisions because the array size covers the full allowed key range.
"""

class MyHashMap:
    def __init__(self):
        self.number_of_buckets = 1000001
        self.buckets = [[] for _ in range(self.number_of_buckets)]
    
    def put(self, key: int, value: int) -> None:
        self.buckets[self._hash(key)] = [key, value]
        
    def get(self, key: int) -> int:
        element = self.buckets[self._hash(key)]
        if element:
            return element[1]
        return -1
    
    def remove(self, key: int) -> None:
        hashed_key = self._hash(key)
        if self.buckets[hashed_key]:
            self.buckets[hashed_key] = []
    
    def _hash(self, key: int) -> int:
        return key % self.number_of_buckets