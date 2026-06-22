def missing_ranges(
    received_ids: list[int],
    start: int,
    end: int,
) -> list[tuple[int, int]]:
    """
    Return missing inclusive sequence ID ranges.

    received_ids may be unsorted, contain duplicates, and include IDs
    outside the expected [start, end] range.

    Approach:
    Deduplicate, filter to the expected range, and sort the received IDs.
    Track the next expected ID. For each valid received ID, if it is greater
    than the next expected ID, then the IDs from expected to valid_id - 1 are
    missing. After processing all valid IDs, append one final missing range
    if the expected ID has not reached the end of the range.

    Time: O(n log n)
    Space: O(n)

    n = number of received IDs
    """
    if start > end:
        return []

    valid_ids = sorted(
        {valid_id for valid_id in received_ids if start <= valid_id <= end}
    )

    result = []
    expected = start

    for valid_id in valid_ids:
        if valid_id > expected:
            result.append((expected, valid_id - 1))

        expected = valid_id + 1

    if expected <= end:
        result.append((expected, end))

    return result


def main():
    test_cases = [
        ([1, 3], 1, 3, [(2, 2)]),
        ([89, 90, 93, 94], 80, 100, [(80, 88), (91, 92), (95, 100)]),
        (
            [0, 10, 1000, 89, 90, 93, 94, 98, 99],
            80,
            100,
            [(80, 88), (91, 92), (95, 97), (100, 100)],
        ),
        (
            [-10, -100, 0, 878, 45, -66, 57, 5, 87, 54, 656, 44, 0],
            -1,
            600,
            [(-1, -1), (1, 4), (6, 43), (46, 53), (55, 56), (58, 86), (88, 600)],
        ),
        ([], 10, 5, []),
        ([], 10, 13, [(10, 13)]),
        ([10, 11, 12, 13], 10, 13, []),
    ]

    for received_ids, start, end, expected in test_cases:
        result = missing_ranges(received_ids, start, end)
        print(
            f"Missing ranges: {result} | "
            f"Expected: {expected} | "
            f"Correct: {result == expected}"
        )


if __name__ == "__main__":
    main()