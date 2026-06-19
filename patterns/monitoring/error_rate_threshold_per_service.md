# Error-Rate Threshold per Service

## Prompt

You are given a list of API request logs.

Each log is a tuple:

```python
(timestamp, service_name, status_code)
```

where:

- `timestamp` is an integer
- `service_name` is a string
- `status_code` is an integer HTTP status code
- logs may not be sorted

A request is considered failed if:

```python
status_code >= 500
```

Write a function:

```python
find_unstable_services(logs, min_requests, failure_threshold) -> list[str]
```

Return the names of services whose failure rate is greater than or equal to `failure_threshold`, but only for services with at least `min_requests` total requests.

Failure rate is:

```text
failed_requests / total_requests
```

Return the result sorted alphabetically.

## Example

```python
logs = [
    (1, "api", 200),
    (2, "api", 500),
    (3, "api", 503),
    (4, "db", 200),
    (5, "db", 500),
    (6, "worker", 500),
    (7, "worker", 200),
    (8, "worker", 200),
]

min_requests = 3
failure_threshold = 0.5
```

Service counts:

```text
api:    3 total, 2 failed -> 2/3 = 0.67
db:     2 total, 1 failed -> ignored because total < min_requests
worker: 3 total, 1 failed -> 1/3 = 0.33
```

Expected output:

```python
["api"]
```

## Recognition Trigger

Per-entity aggregation with two counters:

```text
service -> total request count
service -> failed request count
```

This is a classic monitoring/SRE pattern: scan logs, group by service, compute a metric, filter by threshold, return sorted offenders.

## Clarifying Questions

- Should failures include only `5xx` responses, or also `4xx` responses?
- Is `failure_threshold` inclusive, meaning `failure_rate >= failure_threshold`?
- Should services with fewer than `min_requests` be ignored even if their failure rate is high?
- Can `failure_threshold` be `0.0`?

## Data Structures

Common options:

```python
# Standard dict version
counts: dict[str, list[int]]

# Two-defaultdict version
totals: defaultdict[str, int]
failures: defaultdict[str, int]

# One-defaultdict version
counts: defaultdict[str, list[int]]
```

For interview safety, the two-`defaultdict(int)` version is often the clearest.

---

# Solution 1: Standard Dict

This version avoids `defaultdict` and initializes each service explicitly.

```python
def find_unstable_services(
    logs,
    min_requests,
    failure_threshold,
) -> list[str]:
    counts = {}  # service -> [failures, total]

    for timestamp, service, status in logs:
        if service not in counts:
            counts[service] = [0, 0]

        counts[service][1] += 1

        if status >= 500:
            counts[service][0] += 1

    result = []

    for service, (failure_count, total_count) in counts.items():
        if total_count >= min_requests and failure_count / total_count >= failure_threshold:
            result.append(service)

    return sorted(result)
```

## Why this works

- `counts[service][0]` stores failed requests
- `counts[service][1]` stores total requests
- each log updates the total count
- only `status >= 500` updates the failure count
- the second loop computes the failure rate and filters

---

# Solution 2: Two `defaultdict(int)` Counters

This is the preferred interview version.

```python
from collections import defaultdict


def find_unstable_services(
    logs,
    min_requests,
    failure_threshold,
) -> list[str]:
    totals = defaultdict(int)
    failures = defaultdict(int)

    for timestamp, service, status in logs:
        totals[service] += 1

        if status >= 500:
            failures[service] += 1

    result = []

    for service, total in totals.items():
        failure_count = failures.get(service, 0)

        if total >= min_requests and failure_count / total >= failure_threshold:
            result.append(service)

    return sorted(result)
```

## Why this version is strong

It maps directly to the problem statement:

```text
totals[service]   = total requests for this service
failures[service] = failed requests for this service
```

It avoids positional confusion like:

```python
counts[service][0]
counts[service][1]
```

It also avoids manual initialization.

## Note on `failures.get(service, 0)`

With `defaultdict(int)`, this would also work:

```python
failure_count = failures[service]
```

If the service has no failures, that creates a missing entry with value `0`.

Using `.get(service, 0)` avoids mutating `failures` during the read.

---

# Solution 3: One `defaultdict(lambda: [0, 0])`

This version stores both counters in one dictionary.

```python
from collections import defaultdict


def find_unstable_services(
    logs,
    min_requests,
    failure_threshold,
) -> list[str]:
    counts = defaultdict(lambda: [0, 0])  # service -> [failures, total]

    for timestamp, service, status in logs:
        counts[service][1] += 1

        if status >= 500:
            counts[service][0] += 1

    result = []

    for service, (failure_count, total_count) in counts.items():
        if total_count >= min_requests and failure_count / total_count >= failure_threshold:
            result.append(service)

    return sorted(result)
```

## Why this works

`defaultdict(lambda: [0, 0])` means:

```text
When a missing service is accessed, create a fresh [0, 0].
```

Then:

```python
counts[service][0]  # failure count
counts[service][1]  # total count
```

This is compact, but it is easier to reverse `[0]` and `[1]` under pressure.

---

# Main Traps

## Trap 1: `logs` is a list, not a dict

Wrong:

```python
for timestamp, service, status in logs.items():
    ...
```

Correct:

```python
for timestamp, service, status in logs:
    ...
```

Use `.items()` only when iterating over a dictionary’s key-value pairs.

## Trap 2: Counting loop and filtering loop must be separate

Wrong shape:

```python
for timestamp, service, status in logs:
    totals[service] += 1

    for service, total in totals.items():
        ...
```

Correct shape:

```python
for timestamp, service, status in logs:
    totals[service] += 1

for service, total in totals.items():
    ...
```

First finish building the counts, then compute rates.

## Trap 3: `defaultdict()` is not `defaultdict(int)`

Wrong:

```python
d = defaultdict()
d["api"]      # KeyError
```

Correct for counters:

```python
d = defaultdict(int)
d["api"] += 1
```

`defaultdict(int)` calls `int()` to create default value `0`.

## Trap 4: Factory must be callable

Wrong:

```python
counts = defaultdict([0, 0])
```

Correct:

```python
counts = defaultdict(lambda: [0, 0])
```

The factory creates the default value for a missing key.

## Trap 5: Typo in threshold variable

Wrong:

```python
failure_treshold
```

Correct:

```python
failure_threshold
```

## Trap 6: Returning the wrong variable

Wrong:

```python
return sorted(service)
```

Correct:

```python
return sorted(result)
```

## Trap 7: Threshold must be inclusive

The prompt says:

```text
greater than or equal to failure_threshold
```

So use:

```python
failure_count / total >= failure_threshold
```

not:

```python
failure_count / total > failure_threshold
```

---

# Complexity

Let:

- `N` = number of logs
- `S` = number of unique services
- `R` = number of returned unstable services

Counting logs:

```text
O(N)
```

Filtering services:

```text
O(S)
```

Sorting result:

```text
O(R log R)
```

Since `R <= S`, worst-case time is:

```text
O(N + S log S)
```

Space:

```text
O(S)
```

because the dictionaries store counters per unique service.

---

# Interview Sentence

“I’ll use per-service aggregation. I’ll keep one counter for total requests and one counter for failed requests, where failed means status code >= 500. After scanning the logs once, I’ll iterate through services with enough total traffic, compute failure_count / total_count, filter by the inclusive threshold, and return the matching services sorted alphabetically.”