class HeartbeatTracker:
    """
    Track server liveness using heartbeat timestamps.

    Each server is mapped to its most recent heartbeat timestamp. A server is
    considered alive when its latest heartbeat is within the timeout window:
        0 <= current_time - last_seen <= timeout

    If a heartbeat arrives out of order, keep the newest timestamp only.
    A server with a heartbeat timestamp in the future relative to current_time
    is treated as not alive.

    record_heartbeat:
        Time: O(1)
        Space: O(1) additional space per call

    is_alive:
        Time: O(1)
        Space: O(1)

    get_dead_servers:
        Time: O(n)
        Space: O(d)

    n = number of tracked servers
    d = number of dead servers returned
    """
    def __init__(self, timeout: int):
        self.servers: dict[str, int] = {}
        self.timeout = timeout

    def record_heartbeat(self, server: str, timestamp: int) -> None:
        if server not in self.servers:
            self.servers[server] = timestamp
        else:
            self.servers[server] = max(self.servers[server], timestamp)

    def is_alive(self, server: str, current_time: int) -> bool:
        if server not in self.servers:
            return False

        age = current_time - self.servers[server]
        return 0 <= age <= self.timeout

    def get_dead_servers(self, current_time: int) -> list[str]:
        dead = []

        for server, last_seen in self.servers.items():
            age = current_time - last_seen

            if age < 0 or age > self.timeout:
                dead.append(server)

        return dead
    

def main():
    timeout = 60
    ht = HeartbeatTracker(timeout)

    ht.record_heartbeat("server_1", 89)
    ht.record_heartbeat("server_2", 22)
    ht.record_heartbeat("server_3", 150)

    alive_test_cases = [
        ("server_1", 102, True),
        ("server_2", 102, False),
        ("server_10", 89, False),
        ("server_1", 89, True),
        ("server_1", 150, False),
    ]

    print("is_alive test cases:")
    for server, current_time, expected in alive_test_cases:
        actual = ht.is_alive(server, current_time)
        print(
            f"{server} alive at {current_time}: "
            f"{actual} | expected: {expected}"
        )

    dead_test_cases = [
        (102, ["server_2", "server_3"]),  # server_3 is in the future
        (150, ["server_1", "server_2"]),  # server_3 is exactly current time, alive
    ]

    print("\nget_dead_servers test cases:")
    for current_time, expected in dead_test_cases:
        actual = ht.get_dead_servers(current_time)
        print(
            f"dead servers at {current_time}: "
            f"{actual} | expected: {expected}"
        )


if __name__ == "__main__":
    main()