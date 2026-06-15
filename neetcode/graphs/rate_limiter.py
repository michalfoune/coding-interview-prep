from collections import defaultdict


class RateLimiter:
    def __init__(self, user_limit: int, global_limit: int, window_size: int):
        self.user_limit = user_limit
        self.global_limit = global_limit
        self.window_size = window_size
        self.requests: defaultdict[str, list[int]] = defaultdict(list)

    def allow_request(self, user: str, timestamp: int) -> bool:
        """
        Allow or reject requests using per-user and global sliding-window limits.

        Each accepted request is stored by user ID as a timestamp. Before checking
        a new request, expired timestamps are removed from the in-memory request
        history. A request is allowed only if both the user's active request count
        and the global active request count are still below their limits.

        The sliding window keeps requests where:
            timestamp - window_size < request_time <= timestamp

        Rejected requests are not recorded.

        Time: O(n)
        Space: O(n)

        n = number of accepted requests currently tracked.
        """
        global_request_count = 0

        for user_id, request_times in self.requests.items():
            self.requests[user_id] = [
                request_time
                for request_time in request_times
                if request_time > timestamp - self.window_size
            ]

            global_request_count += len(self.requests[user_id])

        user_request_count = len(self.requests[user])

        if user_request_count < self.user_limit and global_request_count < self.global_limit:
            self.requests[user].append(timestamp)
            return True

        return False


def main():
    rl = RateLimiter(2, 5, 10)

    print(rl.allow_request("M", 100))
    print(rl.allow_request("M", 101))
    print(rl.allow_request("M", 102))
    print(rl.allow_request("B", 102))
    print(rl.allow_request("B", 102))
    print(rl.allow_request("B", 102))
    print(rl.allow_request("C", 103))
    print(rl.allow_request("C", 104))


if __name__ == "__main__":
    main()

