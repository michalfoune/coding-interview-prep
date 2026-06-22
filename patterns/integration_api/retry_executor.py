# import time


class RetryExecutor:
    """
    Execute unreliable operations with retry and exponential backoff.

    For interview/testability purposes, this implementation records the delays
    that would have been used instead of actually sleeping.
    """

    def __init__(self):
        self.delays: list[int] = []

    def execute(self, operation, max_attempts: int, base_delay: int) -> object:
        """
        Execute operation() with retry.

        Args:
            operation: Callable with no arguments.
            max_attempts: Maximum number of attempts, including the first try.
            base_delay: Base delay in seconds.

        Returns:
            Whatever operation() returns if it succeeds.

        Raises:
            ValueError: If max_attempts is less than 1.
            Exception: Re-raises the last exception if all attempts fail.
        """
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")

        self.delays = []
        last_exception = None

        for attempt in range(max_attempts):
            try:
                return operation()
            except Exception as ex:
                last_exception = ex

                is_final_attempt = attempt == max_attempts - 1
                if not is_final_attempt:
                    delay = base_delay * (2 ** attempt)
                    # time.sleep(delay)
                    self.delays.append(delay)

        raise last_exception

    def get_delays(self) -> list[int]:
        """Return delays recorded during the most recent execute() call."""
        return self.delays


def main():
    # Case 1: succeeds immediately, no delays.
    executor = RetryExecutor()

    def succeeds_immediately():
        return "ok"

    result = executor.execute(succeeds_immediately, max_attempts=3, base_delay=2)
    assert result == "ok"
    assert executor.get_delays() == []

    # Case 2: fails twice, then succeeds.
    executor = RetryExecutor()
    counter = {"count": 0}

    def flaky_operation():
        counter["count"] += 1

        if counter["count"] < 3:
            raise ValueError("temporary failure")

        return "success"

    result = executor.execute(flaky_operation, max_attempts=4, base_delay=2)
    assert result == "success"
    assert executor.get_delays() == [2, 4]

    # Case 3: all attempts fail, re-raise last exception.
    executor = RetryExecutor()

    def always_fails():
        raise RuntimeError("service down")

    try:
        executor.execute(always_fails, max_attempts=3, base_delay=5)
        assert False, "Expected RuntimeError"
    except RuntimeError as ex:
        assert str(ex) == "service down"

    assert executor.get_delays() == [5, 10]

    # Case 4: valid falsy return value should still count as success.
    executor = RetryExecutor()

    def returns_zero():
        return 0

    result = executor.execute(returns_zero, max_attempts=3, base_delay=2)
    assert result == 0
    assert executor.get_delays() == []

    print("All tests passed.")


if __name__ == "__main__":
    main()
