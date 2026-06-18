# Idempotent Event Processing / Customer Totals

## Prompt

You are processing billing events from an external system.

Each event is a tuple:

```python
(event_id, customer_id, amount)
```

where:

- `event_id` is a string
- `customer_id` is a string
- `amount` is an integer
- the same `event_id` may appear more than once because the external system retries delivery
- duplicate `event_id`s should only be counted once

Write a function:

```python
calculate_customer_totals(events) -> dict[str, int]
```

Return a dictionary mapping each `customer_id` to the total billed amount, counting each unique `event_id` only once.

If the same `event_id` appears multiple times, use only the first occurrence and ignore later duplicates.

For this version, assume:

- the same `event_id` always refers to the same logical event
- negative amounts are allowed and should be included in the total

## Example

```python
events = [
    ("e1", "custA", 100),
    ("e2", "custA", 50),
    ("e1", "custA", 100),
    ("e3", "custB", 200),
    ("e4", "custA", -20),
    ("e3", "custB", 200),
]
```

Expected output:

```python
{
    "custA": 130,
    "custB": 200,
}
```

Explanation:

- `e1` counted once: `custA +100`
- `e2` counted once: `custA +50`
- duplicate `e1` ignored
- `e3` counted once: `custB +200`
- `e4` counted once: `custA -20`
- duplicate `e3` ignored

## Recognition Trigger

External system retries, at-least-once delivery, duplicate event IDs, idempotent processing.

Use:

- a `set` to track processed event IDs
- a `dict` or `defaultdict(int)` to accumulate totals per customer

## Clarifying Questions

- If the same `event_id` appears again with a different `customer_id` or `amount`, should I ignore it as a duplicate or treat it as data corruption?
- Can amounts be negative, for refunds or corrections?
- Should the output include customers whose total is zero?

## Data Structures

```python
seen_ids: set[str]
totals: dict[str, int]
```

`seen_ids` prevents duplicate processing.

`totals` stores the running billed amount per customer.

## Algorithm

1. Initialize an empty set of seen event IDs.
2. Initialize a customer-to-total map.
3. Iterate through all events.
4. If the event ID has already been seen, skip it.
5. Otherwise, add the amount to that customer's total and mark the event ID as seen.

## Pseudocode

```python
from collections import defaultdict


def calculate_customer_totals(events) -> dict[str, int]:
    totals = defaultdict(int)
    seen_ids = set()

    for event_id, customer_id, amount in events:
        if event_id not in seen_ids:
            totals[customer_id] += amount
            seen_ids.add(event_id)

    return dict(totals)
```

## Main Traps

- Forgetting idempotency and counting duplicate event IDs more than once.
- Using a list instead of a set for seen IDs, making duplicate checks slower.
- Accidentally creating a dict instead of a set with `{}`.
- Using `defaultdict()` instead of `defaultdict(int)`.
- Updating totals before checking whether the event ID was already processed.
- Ignoring the possibility of negative amounts if refunds/corrections are allowed.

## Complexity

Let:

- `N` = number of events
- `E` = number of unique event IDs
- `C` = number of unique customers

Time:

```text
O(N)
```

Each event is processed once, and set/dict operations are average `O(1)`.

Space:

```text
O(E + C)
```

The `seen_ids` set stores unique event IDs, and the totals dictionary stores one entry per customer.

Since `E` and `C` are both at most `N`, this is often simplified to:

```text
O(N)
```

## Interview Sentence

“I’ll make the event processing idempotent by keeping a set of processed event IDs. For each event, if I have already seen the ID, I skip it. Otherwise, I add the amount to that customer’s running total and mark the event ID as seen. This gives linear time with average constant-time set and dict operations.”
