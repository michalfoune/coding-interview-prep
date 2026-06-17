from collections import Counter, deque
from typing import Deque


def unique_users_last_window(
    events: list[tuple[int, str]],
    window_seconds: int,
) -> list[int]:
    """
    For each event, return the number of unique users seen in the trailing
    time window ending at that event's timestamp.

    Window is inclusive:
        keep events where event_time >= current_time - window_seconds

    Example:
        current_time = 8, window_seconds = 5
        keep timestamps >= 3
        evict timestamps < 3

    Time:
        O(n), because each event is added once and removed once.

    Space:
        O(w), where w is the max number of events inside the window.
    """
    if window_seconds < 0:
        raise ValueError("window_seconds must be non-negative")

    window: Deque[tuple[int, str]] = deque()
    user_counts: Counter[str] = Counter()
    result: list[int] = []

    previous_time: int | None = None

    for timestamp, user_id in events:
        if previous_time is not None and timestamp < previous_time:
            raise ValueError("timestamps must be increasing or non-decreasing")
        previous_time = timestamp

        # Add current event.
        window.append((timestamp, user_id))
        user_counts[user_id] += 1

        # Remove expired events.
        cutoff = timestamp - window_seconds

        while window and window[0][0] < cutoff:
            old_timestamp, old_user = window.popleft()
            user_counts[old_user] -= 1

            if user_counts[old_user] == 0:
                del user_counts[old_user]

        # Number of unique users currently in the window.
        result.append(len(user_counts))

    return result


def main() -> None:
    events = [
        (1, "u1"),
        (2, "u2"),
        (3, "u1"),
        (8, "u3"),
        (10, "u1"),
    ]

    expected = [
        1,  # t=1: keep >= -4 -> u1
        2,  # t=2: keep >= -3 -> u1, u2
        2,  # t=3: keep >= -2 -> u1, u2
        2,  # t=8: keep >= 3  -> u1 at t=3, u3 at t=8
        2,  # t=10: keep >= 5 -> u3 at t=8, u1 at t=10
    ]

    actual = unique_users_last_window(events, window_seconds=5)

    print("Actual:  ", actual)
    print("Expected:", expected)
    print("Correct: ", actual == expected)

    assert actual == expected, f"Expected {expected}, got {actual}"


if __name__ == "__main__":
    main()