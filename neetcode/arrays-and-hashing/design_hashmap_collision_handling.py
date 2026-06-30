"""
Problem: Design HashMap
Difficulty: Easy
Pattern: Hash Table / Separate Chaining

Time:
put: O(1) average, O(n) worst case
get: O(1) average, O(n) worst case
remove: O(1) average, O(n) worst case

Space: O(n + b)

Where:
n = number of stored key-value pairs
b = number of buckets

Idea:
Use a fixed-size array of buckets.
Each bucket stores key-value pairs that hash to the same index.
On put/get/remove, hash the key to find the bucket, then scan that bucket.

Buckets
Shape:
self.buckets = [
    [[key, value], [key, value]],   # bucket 0
    [],                            # bucket 1
    [[key, value]],                # bucket 2
    ...
]

Example:
self.buckets = [
    [[1000, 7], [2000, 9]],  # both hash to bucket 0 if num_buckets = 1000
    [[1, 42]],               # bucket 1
    [],                      # bucket 2
    [[3, 99]],               # bucket 3
]
"""

class MyHashMap:
    def __init__(self):
        self.num_buckets = 1000
        self.buckets = [[] for _ in range(self.num_buckets)]
    
    def put(self, key: int, value: int) -> None:
        bucket = self.buckets[self._hash(key)]

        for pair in bucket:
            stored_key = pair[0]

            if stored_key == key:
                pair[1] = value
                return

        bucket.append([key, value])
        
    def get(self, key: int) -> int:
        bucket = self.buckets[self._hash(key)]

        for stored_key, stored_value in bucket:
            if stored_key == key:
                return stored_value

        return -1
    
    def remove(self, key: int) -> None:
        bucket = self.buckets[self._hash(key)]

        for i, pair in enumerate(bucket):
            stored_key = pair[0]

            if stored_key == key:
                bucket.pop(i)
                return
    
    def _hash(self, key: int) -> int:
        return key % self.num_buckets