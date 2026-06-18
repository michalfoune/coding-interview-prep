# Directed Cycle Detection

## Prompt

You are given a dictionary where each key is a service and each value is a list of services it depends on.

```python
{
    "api": ["auth", "db"],
    "auth": ["db"],
    "db": ["api"]
}
```

Return whether there is a dependency cycle.

## Recognition trigger

Directed dependencies. Need to know if something indirectly depends on itself.

## Data structure

- Directed adjacency list: `service -> dependencies`
- `visiting` set: nodes currently on recursion path
- `visited` set: nodes fully processed and safe

## Algorithm

DFS each node. If DFS reaches a node already in `visiting`, there is a cycle. If it reaches a node already in `visited`, that path is already known safe.

## Pseudocode

```python
def dfs(node):
    if node in visiting: return True
    if node in visited: return False

    visiting.add(node)
    for dependency in graph.get(node, []):
        if dfs(dependency): return True

    visiting.remove(node)
    visited.add(node)
    return False

for node in all_nodes:
    if dfs(node): return True
return False
```

## Main trap

Using only one global `visited` set loses the recursion-stack information. A previously seen node is not automatically a cycle; a node currently on the recursion path is a cycle.

Also include dependency-only nodes or use `graph.get(node, [])`.

## Complexity

- Time: `O(V + E)`
- Space: `O(V)` for `visited`, `visiting`, and recursion stack
- Graph storage: `O(V + E)`

## Interview sentence

"This is directed cycle detection. I’ll use DFS with two states: `visiting` for the current recursion path and `visited` for fully processed nodes. A cycle exists if I hit a node already in `visiting`."

## Misses to watch

- Do not return after checking only the first neighbor.
- Do not use only `visited`.
- Do not start from just one assumed root; graphs may be disconnected.
