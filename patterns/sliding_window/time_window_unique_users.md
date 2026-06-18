# Time-Window Unique Users

## Prompt

You receive log events as tuples:

```python
(timestamp, user_id)
```

Timestamps are increasing.

For each event, return the number of unique users seen in the last 5 seconds, inclusive.

Example:

```python
[
    (1, "u1"),
    (2, "u2"),
    (3, "u1"),
    (8, "u3"),
    (10, "u1")
]
```

Correct output for `window_seconds = 5`:

```python
[1, 2, 2, 2, 2]
```

## Clarifying questions

Do you want the running count after every event, or only the final count after all events? In this case running count after every event is expected.

## Recognition trigger

"last N seconds", "trailing window", "timestamps increasing", "unique users", "distinct IDs".

## Data structure

- `deque` of `(timestamp, user_id)` for events currently in the window
- `Counter` / frequency map: `user_id -> count in current window`
- result list

## Algorithm

Process events in timestamp order. Add the new event. Evict expired events from the left. Maintain user counts. The number of unique users is `len(counts)`.

## Pseudocode

```python
window = deque()
counts = Counter()
result = []

for time, user in events:
    window.append((time, user))
    counts[user] += 1

    cutoff = time - window_seconds
    while window and window[0][0] < cutoff:
        old_time, old_user = window.popleft()
        counts[old_user] -= 1
        if counts[old_user] == 0: del counts[old_user]

    result.append(len(counts))

return result
```

## Main trap

Using a `set` instead of a `Counter`.

If `u1` appears twice in the window and the older `u1` expires, `u1` should still count because the newer event remains. A `set` cannot track that; a `Counter` can.

Boundary trap: because the window is inclusive, keep:

```text
event_time >= current_time - window_seconds
```

So evict:

```text
event_time < cutoff
```

not `event_time <= cutoff`.

## Complexity

- Time: `O(n)`, because each event is appended once and evicted once
- Space: `O(w + u)`, where `w` is max events in the window and `u` is unique users in the window
- Worst-case space: `O(n)`

## Interview sentence

"This is a streaming sliding-window problem. Since users can appear multiple times inside the window, I need a deque for eviction order and a frequency map to maintain the unique-user count correctly."

## Misses to watch

- Do not rescan the full list for every event; that becomes `O(n^2)`.
- Do not use only a `set` unless each user can appear at most once.
- Confirm inclusive vs exclusive window boundary.
