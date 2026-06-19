from collections import defaultdict


class ServiceHealthMonitor:
    """
    In-memory service health monitor.

    The monitor stores API request logs recorded over time and can report
    services whose recent failure rate exceeds a threshold.

    Assumptions:
    - Timestamps passed to record() are non-decreasing.
    - The monitor's current time is the latest timestamp recorded.
    - A request is considered failed if status_code >= 500.
    - get_unstable_services() uses an inclusive time window:
      timestamp >= current_time - window_seconds.
    - Logs are retained because different queries may use different window sizes.
    """

    def __init__(self):
        """Initialize an empty monitor."""
        self.logs = []
        self.current_time = None

    def record(self, timestamp, service, status_code) -> None:
        """
        Record one API request.

        Args:
            timestamp: Integer timestamp in seconds.
            service: Service name.
            status_code: HTTP status code for the request.
        """
        self.logs.append((timestamp, service, status_code))
        self.current_time = timestamp

    def get_unstable_services(
        self,
        window_seconds,
        min_requests,
        failure_threshold,
    ) -> list[str]:
        """
        Return unstable services in the recent time window.

        A service is unstable if:
        - it has at least min_requests requests in the window
        - failed_requests / total_requests >= failure_threshold

        Results are sorted by:
        1. highest failure rate first
        2. service name alphabetically for ties

        Args:
            window_seconds: Size of the recent time window.
            min_requests: Minimum number of requests required for a service
                to be considered.
            failure_threshold: Inclusive failure-rate threshold.

        Returns:
            List of service names.
        """
        if self.current_time is None:
            return []

        totals = defaultdict(int)
        failures = defaultdict(int)
        failure_rates = {}

        cutoff = self.current_time - window_seconds

        for timestamp, service, status in self.logs:
            if timestamp >= cutoff:
                totals[service] += 1

                if status >= 500:
                    failures[service] += 1

        for service, total_count in totals.items():
            failure_count = failures.get(service, 0)
            failure_rate = failure_count / total_count

            if total_count >= min_requests and failure_rate >= failure_threshold:
                failure_rates[service] = failure_rate

        sorted_failure_rates = sorted(
            failure_rates.items(),
            key=lambda item: (-item[1], item[0]),
        )

        return [service for service, _ in sorted_failure_rates]


def main():
    monitor = ServiceHealthMonitor()

    monitor.record(1, "api", 200)
    monitor.record(2, "api", 500)
    monitor.record(3, "api", 503)

    monitor.record(4, "db", 500)
    monitor.record(5, "db", 200)

    monitor.record(10, "worker", 500)
    monitor.record(11, "worker", 500)
    monitor.record(12, "worker", 200)

    print(monitor.get_unstable_services(
        window_seconds=10,
        min_requests=2,
        failure_threshold=0.5,
    ))


if __name__ == "__main__":
    main()