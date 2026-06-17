from collections import Counter, defaultdict, deque
from typing import Deque


class FailedUserMonitor:
    """
    Tracks the number of unique users with failed requests per endpoint
    within a fixed trailing time window.

    A failed request is status_code >= 400.

    Time:
        record: amortized O(1)
        unique_failed_users: amortized O(1)

    Space:
        O(W), where W is the number of failed events currently inside
        the active window across endpoints.
    """

    def __init__(self, window_seconds: int):
        if window_seconds < 0:
            raise ValueError("window_seconds must be non-negative")

        self.window_seconds = window_seconds
        self.current_time = 0

        # endpoint -> deque of (timestamp, user_id)
        self.events: dict[str, Deque[tuple[int, str]]] = defaultdict(deque)

        # endpoint -> Counter of user_id -> number of failed events in window
        self.user_counts: dict[str, Counter[str]] = defaultdict(Counter)

    def record(
        self,
        timestamp: int,
        user_id: str,
        endpoint: str,
        status_code: int,
    ) -> None:
        """
        Records one API request event.

        Assumption:
            Events arrive in non-decreasing timestamp order.
        """
        if timestamp < self.current_time:
            raise ValueError("timestamps must be non-decreasing")

        self.current_time = timestamp

        if status_code >= 400:
            self.events[endpoint].append((timestamp, user_id))
            self.user_counts[endpoint][user_id] += 1

        self._evict_expired(endpoint)

    def unique_failed_users(self, endpoint: str) -> int:
        """
        Returns the number of unique users with at least one failed request
        for this endpoint within the trailing window ending at current_time.
        """
        self._evict_expired(endpoint)
        return len(self.user_counts[endpoint])

    def _evict_expired(self, endpoint: str) -> None:
        """
        Keeps events where:

            timestamp >= current_time - window_seconds

        So expired events are:

            timestamp < current_time - window_seconds
        """
        cutoff = self.current_time - self.window_seconds
        queue = self.events[endpoint]
        counts = self.user_counts[endpoint]

        while queue and queue[0][0] < cutoff:
            old_timestamp, old_user = queue.popleft()

            counts[old_user] -= 1
            if counts[old_user] == 0:
                del counts[old_user]


def main():
    monitor = FailedUserMonitor(window_seconds=5)

    events = [
        # time, user, endpoint, status, expected_login_failed_users
        (1,  "u1", "/login",  200, 0),  # only success
        (2,  "u2", "/login",  401, 1),  # u2 failed
        (3,  "u1", "/login",  401, 2),  # u2 and u1 failed
        (7,  "u3", "/search", 200, 2),  # u2 at t=2 still included; cutoff is 2
        (8,  "u1", "/login",  401, 1),  # u2 expired; u1 remains
        (10, "u2", "/login",  401, 2),  # u1 and u2
    ]

    for timestamp, user_id, endpoint, status_code, expected in events:
        monitor.record(timestamp, user_id, endpoint, status_code)
        actual = monitor.unique_failed_users("/login")

        print(timestamp, actual, expected, actual == expected)

        assert actual == expected, f"Expected {expected}, got {actual}"


if __name__ == "__main__":
    main()