import json
from typing import Any, Iterable, Iterator, TypedDict


class Incident(TypedDict):
    incident_id: str
    service: str
    severity: str
    status: str
    created_at: str
    owner: str | None
    tags: list[str]
    metadata: dict[str, Any]


def parse_incidents(rows: Iterable[dict[str, str]]) -> Iterator[Incident]:
    """
    Parse messy incident rows into normalized incident dictionaries.

    Each input row is expected to come from a CSV-like source, where values
    are raw strings and fields may contain extra whitespace, inconsistent
    casing, missing optional values, or invalid metadata.

    The input may be any iterable of rows, such as a list, CSV reader, or
    generator. Valid incidents are yielded one at a time, so callers can
    process large inputs without storing all valid incidents in memory.

    Required fields are normalized and validated:
        - incident_id: required, stripped
        - service: required, stripped and lowercased
        - severity: required, stripped and uppercased
        - status: required, stripped and lowercased
        - created_at: required, basic UTC timestamp validation

    Rows with invalid required fields are skipped.

    Optional fields are normalized safely:
        - owner: stripped, or None if empty
        - tags: comma-separated string converted to list[str]
        - metadata: JSON string parsed into a dict, or {} if missing/invalid

    Valid incidents are yielded in input order.

    Time: O(n * m)
    Space: O(m)

    n = number of input rows
    m = average amount of data per row
    """
    valid_severities = {"P0", "P1", "P2", "P3"}
    valid_statuses = {"open", "resolved", "mitigated"}

    for row in rows:
        incident_id = row.get("incident_id", "").strip()
        service = row.get("service", "").strip().lower()
        severity = row.get("severity", "").strip().upper()
        status = row.get("status", "").strip().lower()
        created_at = row.get("created_at", "").strip()

        if not incident_id:
            continue

        if not service:
            continue

        if severity not in valid_severities:
            continue

        if status not in valid_statuses:
            continue

        if "T" not in created_at or not created_at.endswith("Z"):
            continue

        owner = row.get("owner", "").strip()
        if not owner:
            owner = None

        raw_tags = row.get("tags", "")
        tags = []

        for tag in raw_tags.split(","):
            tag = tag.strip().lower()
            if tag:
                tags.append(tag)

        raw_metadata = row.get("metadata", "").strip()
        metadata: dict[str, Any] = {}

        if raw_metadata:
            try:
                parsed_metadata = json.loads(raw_metadata)
                if isinstance(parsed_metadata, dict):
                    metadata = parsed_metadata
            except json.JSONDecodeError:
                metadata = {}

        incident: Incident = {
            "incident_id": incident_id,
            "service": service,
            "severity": severity,
            "status": status,
            "created_at": created_at,
            "owner": owner,
            "tags": tags,
            "metadata": metadata,
        }

        yield incident


def main():
    rows = [
        {
            "incident_id": "INC-1001",
            "service": "payments ",
            "severity": " P1 ",
            "status": "open",
            "created_at": "2026-06-10T14:30:00Z",
            "owner": " alice@example.com ",
            "tags": "checkout, latency, customer-impacting",
            "metadata": '{"region": "us-central1", "retries": 3}',
        },
        {
            "incident_id": "INC-1002",
            "service": "Search",
            "severity": "p2",
            "status": "RESOLVED",
            "created_at": "2026-06-10T15:10:00Z",
            "owner": "",
            "tags": "ranking, relevance",
            "metadata": '{"region": "europe-west1"}',
        },
    ]

    incident_stream = parse_incidents(rows)

    for incident in incident_stream:
        print(incident)


if __name__ == "__main__":
    main()