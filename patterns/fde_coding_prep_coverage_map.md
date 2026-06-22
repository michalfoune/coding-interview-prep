# FDE Coding Prep Coverage Map

| # | Status | Pattern / problem type | Example realistic prompt | Notes |
|---:|:---:|---|---|---|
| 1 | ✅ | API pagination loop | Fetch all users/items by repeatedly calling `fetch_page(next_token)` | Covered |
| 2 | ✅ | Latest status per entity | Given service health events, find services whose latest status is unhealthy | Covered |
| 3 | ✅ | Idempotent event processing | Deduplicate billing/payment events by `event_id` and compute totals | Covered |
| 4 | ✅ | Error-rate threshold per service | Count total/failing requests per service and return unstable services | Covered |
| 5 | ✅ | Sliding-window health monitor / OOP | `ServiceHealthMonitor.record()` + `get_unstable_services(...)` | Covered |
| 6 | ✅ | Rate limiter / hit counter | Allow/deny requests per user within a time window | Covered earlier |
| 7 | ✅ | Dependency graph / cycle detection | Detect whether service/package dependencies contain a cycle | Covered |
| 8 | ✅ | Topological ordering | Return safe deployment/build order from dependency graph | Covered |
| 9 | ✅ | Reverse dependency / impact analysis | Given dependency graph, find downstream services impacted by a change | Covered |
| 10 | ✅ | Feature flag evaluator / OOP rules engine | Add flags and evaluate user/group targeting rules | Covered |
| 11 | ✅ | Missing sequence / gap detection | Given IDs/timestamps, find missing ranges or gaps | Covered |
| 12 | ✅ | Trie / prefix index | Store/search strings, autocomplete, prefix lookup | Covered earlier, worth review |
| 13 | ✅ | Messy CSV / JSON normalization | Parse records, clean malformed/missing fields, aggregate output | Covered |
| 14 | ✅ | Retry / exponential backoff wrapper | Retry failing operations, record exponential backoff delays, re-raise last exception | Covered |
| 15 | 🟡 | Top-K / ranking / heap | Return top services/users/items by score/count | Light only |
| 16 | ⬜ | Mini search / RAG-like retrieval index | Store docs/chunks and return best matches by keyword/vector-like score | Not yet |

## Summary

```text
Solidly covered: 14
Partly covered: 1
Not yet / light only: 1
```

## Highest-value remaining topics

```text
1. Missing ranges / gap detection
2. Messy CSV / JSON normalization
3. Top-K ranking
4. Mini in-memory search / retrieval index
5. Reverse dependency impact analysis clean full version
```
