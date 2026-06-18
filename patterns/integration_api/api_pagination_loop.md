# API Pagination Loop

## Prompt

You are building a small integration that fetches users from a paginated API.

The API function is already provided:

```python
fetch_page(page_token) -> dict
```

It returns a response like:

```python
{
    "users": ["u1", "u2"],
    "next_page_token": "abc",
}
```

If there are no more pages, `"next_page_token"` is missing or `None`.

Write a function:

```python
get_all_users(fetch_page) -> list[str]
```

that keeps calling `fetch_page` until all pages are fetched and returns all users.

## Example

```python
fetch_page(None)
# returns:
{
    "users": ["u1", "u2"],
    "next_page_token": "abc",
}

fetch_page("abc")
# returns:
{
    "users": ["u3"],
    "next_page_token": "def",
}

fetch_page("def")
# returns:
{
    "users": ["u4"],
}
```

Expected output:

```python
["u1", "u2", "u3", "u4"]
```

## Recognition Trigger

Paginated API. Repeatedly call a provided API/helper function until the response has no next-page token.

## Clarifying Questions

- Can I assume `fetch_page` always returns a dictionary?
- Should I preserve API order?
- Can an empty page have `"users": []` or missing `"users"`?
- Should I guard against repeated page tokens causing an infinite loop?

## Data Structure

- `result: list[str]` to accumulate all users
- `page_token` to track the next page to fetch
- Optional: `seen_tokens: set[str]` for production hardening against repeated tokens

## Algorithm

Use a Python `while True` loop to mimic a do-while loop:

1. Start with `page_token = None`.
2. Fetch the current page.
3. Extend `result` with users from that page.
4. Read the next page token.
5. Break when there is no next page token.

## Pseudocode

```python
def get_all_users(fetch_page) -> list[str]:
    result = []
    page_token = None

    while True:
        page = fetch_page(page_token)
        result.extend(page.get("users", []))

        page_token = page.get("next_page_token")
        if not page_token:
            break

    return result
```

## Main Traps

- Duplicating first-page logic outside the loop.
- Forgetting Python has no native `do while`; use `while True` + `break`.
- Using `page["next_page_token"]` when the final page may not have that key.
- Forgetting to update `page_token`, causing an infinite loop.
- Confusing the callable `fetch_page` with the result of calling `fetch_page(page_token)`.
- Optional production hardening: repeated page tokens can cause infinite pagination.

## Complexity

Let:

- `P` = number of pages
- `U` = total number of users returned across all pages

Time:

```text
O(P + U)
```

Space:

```text
O(U)
```

because the result list stores all users.

## Interview Sentence

“I’ll treat `fetch_page` as a provided callable dependency. I’ll start with `page_token = None`, fetch a page, append its users, update the token, and stop when the response has no next token. Python does not have `do while`, so I’ll use `while True` with a break condition after each fetch.”
