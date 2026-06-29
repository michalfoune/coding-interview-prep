"""
Problem: Server Missing Sequences
Rapid Pattern Drill Problem 4
Pattern: Event stream tracker / SRE sequence gap detection
Status: Green review item

Prompt:
    You receive log events from servers. Each event has:
        (server_id, sequence_number, status)

    For each server, detect missing sequence numbers.

Core idea:
    Group sequence numbers by server.
    Use a set per server to deduplicate.
    Sort each server's observed sequence numbers.
    Scan adjacent observed sequence numbers.
    If there is a gap, emit every missing number inside the gap.

Mental model:
    Outer loop walks known/observed things.
    Conditional inner loop fills or expands the implied missing things.
"""

from collections import defaultdict


def find_missing_sequences(
    events: list[tuple[str, int, str]]
) -> dict[str, list[int]]:
    sequences_by_server = defaultdict(set)

    for server_id, sequence_number, status in events:
        sequences_by_server[server_id].add(sequence_number)

    missing_by_server = {}

    for server_id, sequences in sequences_by_server.items():
        sorted_sequences = sorted(sequences)
        missing = []

        for i in range(len(sorted_sequences) - 1):
            current_seq = sorted_sequences[i]
            next_seq = sorted_sequences[i + 1]

            if next_seq > current_seq + 1:
                for missing_seq in range(current_seq + 1, next_seq):
                    missing.append(missing_seq)

        if missing:
            missing_by_server[server_id] = missing

    return missing_by_server


def main():
    events = [
        ("server-a", 1, "ok"),
        ("server-a", 2, "ok"),
        ("server-a", 4, "ok"),
        ("server-b", 1, "ok"),
        ("server-b", 3, "ok"),
        ("server-b", 4, "ok"),
    ]

    assert find_missing_sequences(events) == {
        "server-a": [3],
        "server-b": [2],
    }

    assert find_missing_sequences([
        ("a", 1, "ok"),
        ("a", 1, "ok"),
        ("a", 4, "ok"),
    ]) == {"a": [2, 3]}

    assert find_missing_sequences([
        ("a", 10, "ok"),
        ("a", 11, "ok"),
    ]) == {}

    print("All tests passed.")


if __name__ == "__main__":
    main()
