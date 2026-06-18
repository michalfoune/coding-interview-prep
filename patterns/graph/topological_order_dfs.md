# Topological Dependency Ordering — DFS Postorder

## Prompt

You are given services and dependencies.

```python
{
    "api": ["auth", "db"],
    "auth": ["db"],
    "worker": ["db"],
    "db": []
}
```

Return a valid startup/build order where dependencies come before dependents.

For example:

- `db` must appear before `auth`
- `db` must appear before `api`
- `db` must appear before `worker`
- `auth` must appear before `api`

## Recognition trigger

Prerequisites must come before dependents. Directed acyclic graph. Build/startup ordering.

## Edge meaning

In this input:

```text
service -> dependency
```

Example: `api -> auth` means `api` depends on `auth`, so `auth` must come before `api`.

## Data structure

- Directed adjacency list: `service -> dependencies`
- `visiting` set for cycle detection
- `visited` set for fully processed nodes
- `order` list for topological output

## Algorithm

DFS postorder. For each service, recursively process all dependencies first. Append the service after its dependencies have been appended.

## Pseudocode

```python
def dfs(service):
    if service in visiting: raise ValueError("cycle")
    if service in visited: return

    visiting.add(service)
    for dependency in graph.get(service, []):
        dfs(dependency)

    visiting.remove(service)
    visited.add(service)
    order.append(service)

for service in all_nodes:
    dfs(service)

return order
```

## Main trap

Appending before processing dependencies gives the wrong order.

Putting `visited.add(service)` only in the outer loop is wrong. `visited` belongs inside `dfs()` because recursive calls also enter nodes.

## Complexity

- Time: `O(V + E)`
- Space: `O(V)` for `visited`, `visiting`, recursion stack, and `order`
- Graph storage: `O(V + E)`

## Interview sentence

"Since the input maps service to dependencies, I can DFS each service, recursively process dependencies first, and append the service on the way back. I’ll use `visiting` for cycle detection and `visited` to avoid duplicate work."

## Misses to watch

- Define edge meaning before coding.
- Do not reverse the graph for this DFS version.
- Do not treat the graph as a tree with one root.
- `visited` must be checked and updated inside `dfs()`.
