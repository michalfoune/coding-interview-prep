"""
Problem: Circuit Breaker
Pattern: Python OOP + distributed-systems resilience pattern

Prompt:
    Implement a CircuitBreaker that protects a downstream service.

    States:
        CLOSED: requests are allowed
        OPEN: requests are blocked
        HALF_OPEN: after cooldown, allow a test request

Rules:
    - Start in CLOSED.
    - Each failure increments failure_count.
    - If failure_count reaches failure_threshold, move to OPEN.
    - While OPEN, block requests.
    - After cooldown time passes, move to HALF_OPEN and allow one test request.
    - If the test request succeeds, move to CLOSED and reset failures.
    - If the test request fails, move back to OPEN.

Distributed-systems idea:
    Protect a failing downstream dependency by failing fast instead of
    repeatedly calling it.

OOP idea:
    Store state on the object:
        self.state
        self.failure_count
        self.opened_at
"""


class CircuitBreaker:
    def __init__(self, failure_threshold: int, cooldown: int):
        self.failure_threshold = failure_threshold
        self.cooldown = cooldown

        self.state = "CLOSED"
        self.failure_count = 0
        self.opened_at = None

    def allow_request(self, current_time: int) -> bool:
        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":
            if current_time - self.opened_at >= self.cooldown:
                self.state = "HALF_OPEN"
                return True
            return False

        if self.state == "HALF_OPEN":
            return True

        return False

    def record_success(self) -> None:
        self.state = "CLOSED"
        self.failure_count = 0
        self.opened_at = None

    def record_failure(self, current_time: int) -> None:
        if self.state == "HALF_OPEN":
            self.state = "OPEN"
            self.opened_at = current_time
            return

        self.failure_count += 1

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            self.opened_at = current_time


def main():
    cb = CircuitBreaker(failure_threshold=2, cooldown=10)

    assert cb.state == "CLOSED"
    assert cb.allow_request(100) is True

    cb.record_failure(100)
    assert cb.state == "CLOSED"
    assert cb.failure_count == 1

    cb.record_failure(101)
    assert cb.state == "OPEN"
    assert cb.allow_request(105) is False

    assert cb.allow_request(111) is True
    assert cb.state == "HALF_OPEN"

    cb.record_success()
    assert cb.state == "CLOSED"
    assert cb.failure_count == 0
    assert cb.opened_at is None

    cb.record_failure(120)
    cb.record_failure(121)
    assert cb.state == "OPEN"
    assert cb.allow_request(131) is True
    assert cb.state == "HALF_OPEN"

    cb.record_failure(132)
    assert cb.state == "OPEN"

    print("All tests passed.")


if __name__ == "__main__":
    main()
