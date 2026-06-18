# Reverse Dependency Graph

## Prompt

You are given this dependency map:

```python
{
    "api": ["auth", "db"],
    "auth": ["db"],
    "worker": ["db"],
    "db": []
}
```

Build a structure that answers:

```text
If db changes, which services are directly affected?
```

## Recognition trigger

Impact analysis, blast radius, "what depends on X?", reverse lookup over dependencies.

## Data structure

Reverse adjacency list:

```text
dependency -> list of direct dependents
```

Example result:

```python
{
    "auth": ["api"],
    "db": ["api", "auth", "worker"]
}
```

## Algorithm

Iterate through the original dependency map. For each `service` and each `dependency`, add `service` to `reverse[dependency]`.

For direct impact, return `reverse[changed_service]`.

For transitive impact, run DFS/BFS from `changed_service` on the reverse graph.

## Pseudocode

```python
reverse = defaultdict(list)

for service, deps in graph.items():
    reverse[service]  # optional: include services with no dependents
    for dep in deps:
        reverse[dep].append(service)

return reverse[changed_service]
```

Python-like no-import version:

```python
reverse = {}

for service, deps in graph.items():
    reverse.setdefault(service, [])
    for dep in deps:
        reverse.setdefault(dep, [])
        reverse[dep].append(service)

return reverse.get(changed_service, [])
```

## Main trap

Confusing direct impact with transitive impact.

- Direct: return immediate dependents from the reverse graph.
- Transitive: traverse the reverse graph to get the full blast radius.

## Complexity

Build reverse graph:

- Time: `O(V + E)`
- Space: `O(V + E)`

Direct lookup:

- Time: `O(k)`, where `k` is the number of direct dependents returned
- Space: `O(k)` if returning a copy

Transitive DFS/BFS:

- Time: `O(V + E)` worst case
- Space: `O(V)`

## Interview sentence

"I’d clarify whether we want direct dependents or the full blast radius. If direct, I’ll build a reverse dependency map and do an `O(k)` lookup. If transitive, I’ll traverse the reverse graph from the changed service."

## Misses to watch

- Do not start DFS from all nodes when the question asks about one changed service.
- Do not forget to reverse `service -> dependency` into `dependency -> service`.
- Be explicit about direct vs transitive.
