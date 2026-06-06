"""
Problem: Design HashMap
Difficulty: Easy
Pattern: Array / List of Pairs

Time:
put: O(n)
get: O(n)
remove: O(n)

Space: O(n)

Where:
n = number of stored key-value pairs

Idea:
Store key-value pairs in a list as 2-element lists: [key, value].
For put, scan the list. If the key already exists, update its value.
Otherwise, append a new [key, value] pair.
For get, scan the list and return the value for the matching key.
For remove, scan the list and remove the matching pair.
"""

class MyHashMap:
    def __init__(self):
        self.items = []

    def put(self, key: int, value: int) -> None:
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items[i] = [key, value]
                return
        self.items.append([key, value])
        
    def get(self, key: int) -> int:
        for k, v in self.items:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                return