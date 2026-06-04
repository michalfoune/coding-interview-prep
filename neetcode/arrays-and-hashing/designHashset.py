"""
Problem: Design HashSet
Difficulty: Easy
Pattern: Hash Table / Buckets

Time:
add: O(1) average, O(n) worst case
remove: O(1) average, O(n) worst case
contains: O(1) average, O(n) worst case

Space: O(n + b)

Where:
n = number of stored keys
b = number of buckets

Idea:
Use a fixed-size list of buckets. Hash each key to a bucket index using
key % num_buckets. Each bucket stores keys that collide at the same index.
For add, remove, and contains, only search within the relevant bucket.
"""

class MyHashSet:
    def __init__(self):
        self.num_buckets = 1000
        self.buckets = [[] for _ in range(self.num_buckets)]
        
    def add(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        if key not in bucket:
            bucket.append(key)

    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]
        if key in bucket:
            bucket.remove(key)

    def contains(self, key: int) -> bool:
        bucket = self.buckets[self._hash(key)]
        return key in bucket

    def _hash(self, key: int) -> int:
        return key % self.num_buckets