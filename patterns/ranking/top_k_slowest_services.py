from collections import defaultdict


def top_k_slowest_services(
    logs: list[tuple[int, str, int]],
    k: int,
    min_requests: int,
) -> list[tuple[str, float]]:
    """
    Return the top k services with the highest average latency.

    Assignment:
    You are given API request logs. Each log entry is a tuple:

        (timestamp, service_name, latency_ms)

    Rules:
    - Treat every log entry as one observed request.
    - Logs may be unsorted; order does not matter for this aggregation.
    - Do not deduplicate records.
    - Ignore services with fewer than min_requests requests.
    - Average latency = total latency / request count.
    - Sort by average latency descending.
    - If two services have the same average latency, sort alphabetically by service name.
    - Return a list of (service_name, average_latency) tuples.
    - If k is larger than the number of qualifying services, return all qualifying services.
    - If k <= 0, return [].

    Time:
        O(n + s log s), where n is number of logs and s is number of services.

    Space:
        O(s)
    """
    if k <= 0:
        return []

    counts = defaultdict(int)
    totals = defaultdict(int)

    for _, service_name, latency in logs:
        counts[service_name] += 1
        totals[service_name] += latency

    avg_latency = {}

    for service, total in totals.items():
        if counts[service] >= min_requests:
            avg_latency[service] = total / counts[service]

    sorted_latency = sorted(
        avg_latency.items(),
        key=lambda item: (-item[1], item[0]),
    )

    # If the prompt asked for service names only, use:
    # return [service for service, _ in sorted_latency[:k]]

    return sorted_latency[:k]


def main():
    logs = [
        (1, "api", 350),
        (2, "api", 421),
        (3, "db", 54),
        (4, "cache", 5),
        (5, "db", 98),
        (6, "api", 424),
    ]

    result = top_k_slowest_services(
        logs,
        k=3,
        min_requests=2,
    )

    expected = [
        ("api", 398.3333333333333),
        ("db", 76.0),
    ]

    assert result == expected
    print("All tests passed.")


if __name__ == "__main__":
    main()
