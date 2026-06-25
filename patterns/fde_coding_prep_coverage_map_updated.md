# FDE Coding Prep Coverage Map

Updated based on the latest coding-round clarification: expect **general SWE / LeetCode-style Python**, with **strings as the common theme**, and possible **SRE or distributed-systems framing**. This means the original FDE-realistic coverage is still useful, but the remaining prep should shift toward **string-heavy DSA patterns hidden under realistic prompts**.

## Coverage table

| # | Status | Pattern / problem type | Example realistic prompt | Notes / priority |
|---:|:---:|---|---|---|
| 1 | ✅ | API pagination loop | Fetch all users/items by repeatedly calling `fetch_page(next_token)` | Covered. Lower priority now; useful FDE realism, but less central for LeetCode-style DSA. |
| 2 | ✅ | Latest status per entity | Given service health events, find services whose latest status is unhealthy | Covered. Still relevant: string/log parsing + hashmap state. |
| 3 | ✅ | Idempotent event processing | Deduplicate billing/payment events by `event_id` and compute totals | Covered. Still relevant: sets, dicts, aggregation. |
| 4 | ✅ | Error-rate threshold per service | Count total/failing requests per service and return unstable services | Covered. Still relevant: grouping, counting, ratios, thresholds. |
| 5 | ✅ | Sliding-window health monitor / OOP | `ServiceHealthMonitor.record()` + `get_unstable_services(...)` | Covered. Convert mentally to simple function-style version too; avoid overusing OOP in interview. |
| 6 | ✅ | Rate limiter / hit counter | Allow/deny requests per user within a time window | Covered earlier. Still relevant: sliding window, queues/lists, cleanup, boundary cases. |
| 7 | ✅ | Dependency graph / cycle detection | Detect whether service/package dependencies contain a cycle | Covered. High relevance for strings + graphs / distributed-systems framing. |
| 8 | ✅ | Topological ordering | Return safe deployment/build order from dependency graph | Covered. High relevance for task/service dependency prompts. |
| 9 | ✅ | Reverse dependency / impact analysis | Given dependency graph, find downstream services impacted by a change | Covered. High relevance; review clean full version. |
| 10 | ✅ | Feature flag evaluator / OOP rules engine | Add flags and evaluate user/group targeting rules | Covered. Useful but lower priority now unless the prompt becomes rules/state-machine style. |
| 11 | ✅ | Missing sequence / gap detection | Given IDs/timestamps, find missing ranges or gaps | Covered. High relevance for SRE/log/sequences. |
| 12 | ✅ | Trie / prefix index | Store/search strings, autocomplete, prefix lookup | Covered earlier. Worth light review; string-heavy but probably not the highest probability unless prefix/search appears. |
| 13 | ✅ | Messy CSV / JSON normalization | Parse records, clean malformed/missing fields, aggregate output | Covered. High relevance: string parsing, validation, normalization. |
| 14 | ✅ | Retry / exponential backoff wrapper | Retry failing operations, record exponential backoff delays, re-raise last exception | Covered. Lower priority now; useful FDE realism but less central if round is DSA. |
| 15 | ✅ | Top-K / ranking / heap | Return top services/users/items by score/count | Covered. High relevance: frequency maps, sorting, tie-breaks, heap if needed. |
| 16 | ✅ | Mini search / RAG-like retrieval index | Store docs/chunks and return best matches by keyword/vector-like score | Covered. High relevance: reverse index + scoring + ranking. |
| 17 | 🟠 | String frequency / character counting | Given log labels, event types, or tokens, count frequencies and compare/group strings | WIP. Covers anagrams, first non-repeating char, frequency comparison, token counts. Core structures: dict / Counter / sorted key. |
| 18 | ⬜ | Substring / sliding-window strings | Find longest valid substring, recent unique users/tokens, or events satisfying window constraints | Add. High-priority LeetCode pattern. Core structures: two pointers, set/dict counts, left/right window. |
| 19 | ⬜ | Two pointers on strings / arrays | Validate near-palindrome, merge sorted event streams, dedupe sorted records, compare compressed strings | Add. Medium priority. Often hidden in string/log/stream prompts. |
| 20 | ⬜ | Binary search / first anomaly | Find first failing version/timestamp, first unhealthy state, threshold crossing, rotated sorted array basics | Add lightly. Important weak flank; do not over-invest, but know the boundary-search skeleton. |
| 21 | ⬜ | Stack for strings | Validate nested syntax, simplify paths, remove adjacent duplicates, process undo-like event streams | Add. Medium priority. Common SWE pattern; possible string-heavy prompt. |
| 22 | ⬜ | String graph construction | Build graph from string pairs/relationships and run BFS/DFS/topo/cycle detection | Add. Very high relevance: bridge between LeetCode strings and SRE/distributed systems. |
| 23 | ⬜ | Sorting with custom tie-breaks | Rank services/documents/errors by count/score, then name/time/id deterministically | Add. High relevance. Practice `sorted(..., key=lambda item: (-score, name))` style. |

## Reframed summary

```text
Original FDE-realistic patterns: strong coverage.
New weak flank: string-heavy LeetCode / DSA patterns.
Most important shift: DSA pattern recognition first, FDE/SRE story second.
```

```text
Solidly covered: 15
Partly covered: 1
New / not yet covered: 7
```

## Current highest-value remaining topics

```text
1. Code mini search / reverse index yourself (#16)
2. String frequency / counting / grouping (#17)
3. Substring sliding window (#18)
4. String graph construction (#22)
5. Sorting with custom tie-breaks (#23)
6. Two pointers on strings / arrays (#19)
7. Stack for strings (#21)
8. Binary search / first anomaly (#20) — light but necessary
```

## Prep allocation for the extra week

```text
50%  New / weak DSA patterns around strings and graphs
30%  Timed implementation in Google Docs / notepad conditions
15%  Review known FDE / SRE realistic problems
5%   Syntax, red-zone mistakes, and interview control
```

## How to interpret the expected coding round

```text
Likely not: AI engineering implementation.
Likely not: deep GCP or FDE product design.
Likely not: pure practical mini-system only.

Likely: one general SWE / LeetCode-style coding question.
Common theme: strings.
Possible framing: SRE or distributed systems.
Assessed skills: understand prompt, discover requirements, choose data structures, code clean Python, handle edge cases, explain assumptions.
No dynamic programming.
```

## Pattern-recognition checklist

When the problem is unfamiliar, do not search for a memorized trick first. Search for the underlying relationship.

```text
Membership?              -> set
Counting/frequency?      -> dict / Counter
Grouping?                -> dict of lists/sets/counts
Order over time?         -> sort, two pointers, sliding window
Dependencies?            -> graph adjacency list
Reverse lookup?          -> reverse index / reverse adjacency
Top results?             -> frequency map + sorted / heap
Nested structure?        -> stack
First threshold/anomaly? -> binary search
Repeated status changes? -> tracker / state machine
```

## Per-problem pattern card

After each practice problem, capture only this:

```text
Problem:
Pattern bucket:
Core data structure:
Key invariant:
Trap / bug risk:
Edge tests:
```

## Interview operating rules

```text
1. Clarify inputs, outputs, ordering assumptions, duplicates, and edge cases.
2. State the simple approach before coding.
3. Prefer simple Python over clever Python.
4. Avoid excessive type hints before core logic is done.
5. Test normal case, empty/minimal case, duplicate/boundary case.
6. If stuck, write brute force first, then improve.
7. Explain trade-offs calmly; do not self-deprecate.
```
