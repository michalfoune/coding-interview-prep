# Latest Status Per Entity / Stale Unhealthy Services

## Prompt

You are given a list of health-check events from services in a distributed system.

Each event is a tuple:

```python
(timestamp, service_name, status)
```

where:

- `timestamp` is an integer
- `service_name` is a string
- `status` is either `"healthy"` or `"unhealthy"`
- events may not be sorted

Write a function:

```python
find_unhealthy_services(events, current_time, stale_after) -> list[str]
```

Return the service names whose latest known status is `"unhealthy"` and whose latest event is not stale.

A service's latest event is stale if:

```python
current_time - latest_timestamp > stale_after
```

Return the result sorted alphabetically.

## Example

```python
events = [
    (10, "api", "healthy"),
    (15, "db", "unhealthy"),
    (20, "api", "unhealthy"),
    (25, "worker", "healthy"),
    (30, "db", "healthy"),
    (40, "cache", "unhealthy"),
]

current_time = 45
stale_after = 20
```

Latest status per service:

```text
api    -> timestamp 20, unhealthy
db     -> timestamp 30, healthy
worker -> timestamp 25, healthy
cache  -> timestamp 40, unhealthy
```

Staleness:

```text
api:   45 - 20 = 25, stale
cache: 45 - 40 = 5, not stale
```

Expected output:

```python
["cache"]
```

## Recognition Trigger

For each entity, keep only the latest event, then filter by business rules.

This often appears as:

- latest status per service
- latest record per customer
- latest event per device
- latest failure per job
- stale resources / stale health checks

## Clarifying Questions

- Can I assume timestamps are unique per service?
- If two events for the same service have the same timestamp, should the later event in the input win?
- Should stale unhealthy services be excluded entirely, or returned separately as `unknown` / `stale`?
- Should the output be sorted alphabetically?

## Data Structure

Use a dictionary / hash map:

```python
latest: dict[str, tuple[int, str]]
```

Mapping:

```text
service_name -> (latest_timestamp, latest_status)
```

Example:

```python
latest = {
    "api": (20, "unhealthy"),
    "db": (30, "healthy"),
    "cache": (40, "unhealthy"),
}
```

## Algorithm

1. Create an empty dict `latest`.
2. Scan all events.
3. For each service, keep only the event with the newest timestamp.
4. Scan the latest states.
5. Return services whose latest status is `"unhealthy"` and whose latest timestamp is not stale.
6. Sort the result alphabetically.

## Pseudocode

```python
def find_unhealthy_services(
    events: list[tuple[int, str, str]],
    current_time: int,
    stale_after: int,
) -> list[str]:
    latest: dict[str, tuple[int, str]] = {}

    for ts, service, health in events:
        if service not in latest or ts >= latest[service][0]:
            latest[service] = (ts, health)

    result = []

    for service, (ts, health) in latest.items():
        is_not_stale = current_time - ts <= stale_after
        if health == "unhealthy" and is_not_stale:
            result.append(service)

    return sorted(result)
```

## Main Traps

- Forgetting that events may be unsorted.
- Appending every unhealthy event instead of keeping only the latest event per service.
- Treating an old unhealthy event as relevant even though a newer healthy event exists.
- Forgetting the stale check.
- Getting the staleness boundary wrong:
  - stale if `current_time - latest_timestamp > stale_after`
  - not stale if `current_time - latest_timestamp <= stale_after`
- Forgetting to sort the result.
- Using `defaultdict()` incorrectly when a normal dict is enough.

## Tie Behavior

This condition:

```python
ts >= latest[service][0]
```

means that if two events for the same service have the same timestamp, the later event in the input wins.

State this assumption if asked.

## Complexity

Let:

- `N` = number of events
- `S` = number of unique services

Building the dict:

```text
O(N)
```

Filtering latest services:

```text
O(S)
```

Sorting the returned services:

```text
O(S log S)
```

Total time:

```text
O(N + S log S)
```

Space:

```text
O(S)
```

because the dict stores one latest event per service.

## Interview Sentence

I’ll use a dict mapping service name to its latest event. Since events may be unsorted, I’ll scan all events and update the dict only when I see a newer timestamp. Then I’ll filter the latest states for services whose latest status is unhealthy and not stale, and finally return the result sorted alphabetically.
