# Lessons Learned: Palindrome With Up To M Deletions

## Suggested Repo Location

This twist belongs under dynamic programming:

```text
patterns/dynamic_programming/is_palindrome_with_deletions.py
patterns/dynamic_programming/lessons_palindrome_with_deletions.md
```

This is a twist on:

```text
patterns/strings/is_near_palindrome.py
```

The one-deletion version is a clean two-pointer problem.

The `m`-deletions version becomes a dynamic programming / memoized recursion problem.

---

## Quick Summary

- For one deletion, two pointers are enough.
- For up to `m` deletions, each mismatch creates repeated branching choices.
- The key subproblem is: minimum deletions needed to make `text[left:right]` a palindrome.
- If outer characters match, move inward with no deletion.
- If outer characters differ, delete left or delete right and take the cheaper option.
- Without cache, the recursion can become exponential.
- With `@lru_cache`, each `(left, right)` range is solved once.
- That changes the complexity from roughly `2 ** n` to `n ** 2`.

---

## Problem Shape

Implement:

```python
def is_palindrome_with_deletions(text: str, max_deletions: int) -> bool:
```

Return `True` if `text` can become a palindrome by deleting at most `max_deletions` characters.

Examples:

```python
is_palindrome_with_deletions("abca", 1) == True
is_palindrome_with_deletions("abc", 1) == False
is_palindrome_with_deletions("abc", 2) == True
is_palindrome_with_deletions("abxycdba", 2) == True
is_palindrome_with_deletions("abxycdba", 1) == False
```

---

## The Interview Explanation I Want To Remember

```text
I compute the minimum number of deletions needed to make text[left:right] a palindrome.

If the outer characters match, no deletion is needed there, so I move inward.

If they differ, I must delete either the left character or the right character, so I take 1 plus the cheaper of those two recursive options.

At the end, I compare the minimum deletions needed with max_deletions.
```

This is the whole problem in four lines.

---

## Clean Solution

```python
from functools import lru_cache


def is_palindrome_with_deletions(text: str, max_deletions: int) -> bool:
    if max_deletions < 0:
        return False

    @lru_cache(maxsize=None)
    def min_deletions_needed(left: int, right: int) -> int:
        if left >= right:
            return 0

        if text[left] == text[right]:
            return min_deletions_needed(left + 1, right - 1)

        delete_left = 1 + min_deletions_needed(left + 1, right)
        delete_right = 1 + min_deletions_needed(left, right - 1)

        return min(delete_left, delete_right)

    return min_deletions_needed(0, len(text) - 1) <= max_deletions
```

---

## How The Recursion Works

The helper means:

```python
min_deletions_needed(left, right)
```

Return the fewest deletions needed to make this substring range a palindrome:

```text
text[left : right + 1]
```

Base case:

```python
if left >= right:
    return 0
```

Why?

An empty string or one-character string is already a palindrome.

Matching outer characters:

```python
if text[left] == text[right]:
    return min_deletions_needed(left + 1, right - 1)
```

No deletion is needed for those two characters.

Mismatching outer characters:

```python
delete_left = 1 + min_deletions_needed(left + 1, right)
delete_right = 1 + min_deletions_needed(left, right - 1)
return min(delete_left, delete_right)
```

If the outer characters do not match, one of them must be deleted.

Take the cheaper option.

---

## Why The One-Deletion Version Was Simpler

For `max_deletions = 1`, at the first mismatch you only get one chance:

```text
skip left OR skip right
```

That can be solved with two pointers and a helper.

For `max_deletions > 1`, there can be many mismatches, and every mismatch creates branching choices.

That is why the problem shifts from:

```text
two pointers
```

to:

```text
dynamic programming / memoized recursion
```

---

## What `@lru_cache` Does

This decorator:

```python
@lru_cache(maxsize=None)
```

makes Python remember function results by arguments.

So if the code computes:

```python
min_deletions_needed(2, 7)
```

and gets result `3`, Python stores:

```text
(2, 7) -> 3
```

If recursion later asks again for:

```python
min_deletions_needed(2, 7)
```

Python returns the cached result immediately instead of recomputing the whole subtree.

The function body does not show explicit cache logic because the decorator wraps the function automatically.

Mentally, it behaves like:

```python
cache = {}

def wrapped(left, right):
    if (left, right) in cache:
        return cache[(left, right)]

    result = original_function(left, right)
    cache[(left, right)] = result
    return result
```

---

## Bigger Recursion Tree Without Cache

Each mismatch creates two branches:

```text
delete left
delete right
```

For a string like `"abcdef"`, many outer characters do not match.

The recursion starts like this:

```text
f(0,5)  # "abcdef"
├── delete left  -> f(1,5)  # "bcdef"
│   ├── delete left  -> f(2,5)  # "cdef"
│   │   ├── delete left  -> f(3,5)
│   │   └── delete right -> f(2,4)
│   │
│   └── delete right -> f(1,4)  # "bcde"
│       ├── delete left  -> f(2,4)
│       └── delete right -> f(1,3)
│
└── delete right -> f(0,4)  # "abcde"
    ├── delete left  -> f(1,4)  # "bcde"
    │   ├── delete left  -> f(2,4)
    │   └── delete right -> f(1,3)
    │
    └── delete right -> f(0,3)  # "abcd"
        ├── delete left  -> f(1,3)
        └── delete right -> f(0,2)
```

Repeated states:

```text
f(1,4) appears multiple times
f(2,4) appears multiple times
f(1,3) appears multiple times
```

Without cache, each repeated state recomputes its subtree again.

With cache, each repeated state is computed once.

---

## Short Explanation: Exponential To Quadratic

Without cache:

```text
Each mismatch branches into two recursive calls.
The tree can roughly double at each level.
That is exponential: about 2 ** n.
```

With cache:

```text
The state is only (left, right).
There are only about n * n possible ranges.
Each range is solved once.
That is quadratic: about n ** 2.
```

---

## Numeric Intuition

```text
n = 10
n ** 2 = 100
2 ** n = 1,024
```

```text
n = 20
n ** 2 = 400
2 ** n = 1,048,576
```

```text
n = 30
n ** 2 = 900
2 ** n = 1,073,741,824
```

So:

```text
n ** 2 = quadratic
2 ** n = exponential
```

The cache turns repeated branching work into a grid of substring ranges.

---

## Complexity

With `@lru_cache`:

```text
Time: O(n^2)
Space: O(n^2)
```

Why?

There are at most `n * n` possible `(left, right)` pairs.

Each pair is computed once.

Without cache, the same ranges are recomputed many times, producing exponential behavior.

---

## Red-Zone Summary

```text
Correct:
- Define subproblem as minimum deletions needed for text[left:right].
- If outer chars match, move inward.
- If they differ, delete left or delete right.
- Add 1 for the deletion.
- Take the minimum.
- Compare final minimum deletions to max_deletions.
- Use @lru_cache to avoid recomputing ranges.

Avoid:
- Trying to force this into the one-deletion two-pointer solution.
- Forgetting that multiple mismatches require multiple branching choices.
- Forgetting +1 when deleting left or right.
- Forgetting that cache is what changes the solution from exponential to quadratic.
- Confusing n ** 2 with 2 ** n.
```
