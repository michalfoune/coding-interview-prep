"""
Problem: Server Health Tracker
Pattern: Python OOP + SRE/distributed-systems-style state tracking

Prompt:
    Implement a small server health tracker.

    The tracker receives heartbeats and error events from servers.

    A server is healthy if:
        1. It has sent at least one heartbeat.
        2. Its latest heartbeat is within the configured timeout.
        3. Its latest error is not newer than its latest heartbeat.

Design choices:
    - Keep two dictionaries:
        self.last_heartbeat: server_id -> latest heartbeat timestamp
        self.last_error: server_id -> latest error timestamp

    - Use max(...) when recording events so older out-of-order events do not
      overwrite newer information.

    - For unhealthy_servers(...), define the universe of known servers as:
        servers that have either sent a heartbeat or reported an error.
"""


class ServerHealthTracker:
    def __init__(self, timeout: int):
        self.timeout = timeout
        self.last_heartbeat = {}
        self.last_error = {}

    def record_heartbeat(self, server_id: str, timestamp: int) -> None:
        """Record the latest heartbeat timestamp for a server."""
        self.last_heartbeat[server_id] = max(
            self.last_heartbeat.get(server_id, timestamp),
            timestamp
        )

    def record_error(self, server_id: str, timestamp: int) -> None:
        """Record the latest error timestamp for a server."""
        self.last_error[server_id] = max(
            self.last_error.get(server_id, timestamp),
            timestamp
        )

    def is_healthy(self, server_id: str, current_time: int) -> bool:
        """
        Return True if the server is currently healthy.

        A server is unhealthy if:
            - it has never sent a heartbeat
            - its latest heartbeat is too old
            - it has a newer error than its latest heartbeat
        """
        if server_id not in self.last_heartbeat:
            return False

        heartbeat_time = self.last_heartbeat[server_id]

        if current_time - heartbeat_time > self.timeout:
            return False

        error_time = self.last_error.get(server_id)

        if error_time is not None and error_time > heartbeat_time:
            return False

        return True

    def unhealthy_servers(self, current_time: int) -> list[str]:
        """
        Return all known servers that are unhealthy.

        Known servers are those that appear in either:
            - last_heartbeat
            - last_error
        """
        all_servers = set(self.last_heartbeat) | set(self.last_error)
        unhealthy = []

        for server_id in all_servers:
            if not self.is_healthy(server_id, current_time):
                unhealthy.append(server_id)

        return sorted(unhealthy)


def main():
    tracker = ServerHealthTracker(timeout=10)

    # Unknown server has no heartbeat, so it is unhealthy.
    assert tracker.is_healthy("missing-server", current_time=100) is False

    # Basic heartbeat freshness.
    tracker.record_heartbeat("a", 100)
    assert tracker.is_healthy("a", current_time=105) is True
    assert tracker.is_healthy("a", current_time=110) is True

    # Stale only when age is greater than timeout.
    assert tracker.is_healthy("a", current_time=111) is False

    # Error after heartbeat makes server unhealthy.
    tracker.record_heartbeat("b", 100)
    assert tracker.is_healthy("b", current_time=105) is True

    tracker.record_error("b", 105)
    assert tracker.is_healthy("b", current_time=106) is False

    # Newer heartbeat after error recovers server.
    tracker.record_heartbeat("b", 108)
    assert tracker.is_healthy("b", current_time=109) is True

    # Server with only an error is known, but unhealthy because no heartbeat.
    tracker.record_error("c", 120)
    assert tracker.is_healthy("c", current_time=121) is False

    # Out-of-order old heartbeat should not overwrite newer heartbeat.
    tracker.record_heartbeat("d", 200)
    tracker.record_heartbeat("d", 190)
    assert tracker.last_heartbeat["d"] == 200
    assert tracker.is_healthy("d", current_time=205) is True

    # Out-of-order old error should not overwrite newer error.
    tracker.record_error("e", 300)
    tracker.record_error("e", 250)
    assert tracker.last_error["e"] == 300

    # Unhealthy server listing.
    tracker2 = ServerHealthTracker(timeout=10)
    tracker2.record_heartbeat("healthy", 100)
    tracker2.record_heartbeat("stale", 80)
    tracker2.record_heartbeat("errored", 100)
    tracker2.record_error("errored", 105)
    tracker2.record_error("only-error", 100)

    assert tracker2.unhealthy_servers(current_time=106) == [
        "errored",
        "only-error",
        "stale",
    ]

    print("All tests passed.")


if __name__ == "__main__":
    main()
