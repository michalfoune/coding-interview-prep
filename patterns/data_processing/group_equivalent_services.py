"""Group service names that have equivalent character frequencies.

Two service names are equivalent if, after normalization, they contain the
same alphanumeric characters with the same counts, regardless of order.
"""

import re
from collections import Counter, defaultdict


def group_equivalent_services(service_names: list[str]) -> list[list[str]]:
    """Return groups of equivalent original service names.

    Normalization rules:
    - lowercase service names
    - ignore non-alphanumeric characters
    - keep letters and digits
    - ignore character order
    - preserve character frequency

    Only groups with at least two service names are returned.
    Names inside each group are sorted alphabetically, and the final list of
    groups is also sorted.
    """
    equivalent_services = defaultdict(list)

    for service_name in service_names:
        normalized_service_name = _normalize(service_name)
        if not normalized_service_name:
            continue

        counter = Counter(normalized_service_name)
        key = tuple(sorted(counter.items()))
        equivalent_services[key].append(service_name)

    result = []

    for group in equivalent_services.values():
        if len(group) > 1:
            result.append(sorted(group))

    return sorted(result)


def _normalize(text: str) -> str:
    """Normalize text by lowercasing and keeping only letters and digits."""
    if not text:
        return ""

    parts = re.findall(r"[a-z0-9]+", text.lower())
    return "".join(parts)


def main() -> None:
    services = [
        "Auth-Service",
        "service-auth",
        "BillingAPI",
        "api-billing",
        "Cache",
        "cache-v2",
        "v2-cache",
        "Worker1",
        "worker-1",
        "worker-2",
        "!!!",
    ]

    assert group_equivalent_services(services) == [
        ["Auth-Service", "service-auth"],
        ["BillingAPI", "api-billing"],
        ["Worker1", "worker-1"],
        ["cache-v2", "v2-cache"],
    ]

    assert group_equivalent_services([]) == []
    assert group_equivalent_services(["!!!", "   ", "abc"]) == []
    assert group_equivalent_services(["aab", "aba", "baa", "ab"]) == [
        ["aab", "aba", "baa"]
    ]

    print("All tests passed.")


if __name__ == "__main__":
    main()
