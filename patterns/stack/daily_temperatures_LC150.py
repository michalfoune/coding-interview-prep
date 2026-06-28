"""
Problem: Daily Temperatures
Source: NeetCode 150 rapid review
Difficulty: Medium
Mode: Rapid-fire implementation after seeing/discussing the monotonic stack shape
Authorship: Written by me in Google Docs after understanding the pattern
Date: 2026-06-27, Saturday 10:16pm
Pattern: Monotonic stack
Status: Correct 10/10

Cherry-pick note:
    This was not invented from pure nothing — I first saw/discussed the
    monotonic stack shape. But after that, the implementation was written
    cleanly and correctly from understanding.

    In a long prep marathon, this counts as a real win:
    the pattern was understood, translated into code, and written correctly.

Prompt:
    Given a list of daily temperatures, return a list where each position
    tells how many days you have to wait until a warmer temperature.

    If there is no future warmer day, return 0 for that position.

Example:
    temperatures = [73, 74, 75, 71, 69, 72, 76, 73]

    result = [1, 1, 4, 2, 1, 1, 0, 0]

Core idea:
    Use a stack of unresolved indexes.

    The stack stores indexes of days that have not yet found a warmer
    future day.

    When the current temperature is warmer than the temperature at the
    index on top of the stack, the current day resolves that previous day.

Why indexes, not temperatures?
    The answer needs a distance in days:

        current_index - previous_index

    So the stack must store indexes.

Why the nested while loop is still O(n):
    Each index is pushed once and popped at most once.

    Even though there is a while loop inside the for loop, the total number
    of pops across the whole algorithm is at most n.

Time:
    O(n)

Space:
    O(n)
"""


def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    Return the number of days until a warmer future temperature for each day.

    Monotonic stack invariant:
        The stack contains indexes of days whose warmer future day has not
        been found yet.

    For each current temperature:
        - while the current temperature is warmer than the unresolved day
          on top of the stack, pop that previous day and fill its answer
        - then push the current index, because it may need a warmer future day
    """
    result = [0] * len(temperatures)
    stack = []

    for i, temperature in enumerate(temperatures):
        while stack and temperature > temperatures[stack[-1]]:
            previous_index = stack.pop()
            result[previous_index] = i - previous_index

        stack.append(i)

    return result


def main():
    assert daily_temperatures([]) == []
    assert daily_temperatures([73]) == [0]

    assert daily_temperatures(
        [73, 74, 75, 71, 69, 72, 76, 73]
    ) == [1, 1, 4, 2, 1, 1, 0, 0]

    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    assert daily_temperatures([30, 60, 90]) == [1, 1, 0]
    assert daily_temperatures([90, 80, 70]) == [0, 0, 0]

    # Equal temperatures are not warmer.
    assert daily_temperatures([70, 70, 70]) == [0, 0, 0]

    # Current warmer day can resolve multiple previous unresolved days.
    assert daily_temperatures([70, 55, 56, 71]) == [3, 1, 1, 0]

    # Mixed ups and downs.
    assert daily_temperatures([60, 50, 55, 53, 70]) == [4, 1, 2, 1, 0]

    print("All tests passed.")


if __name__ == "__main__":
    main()
