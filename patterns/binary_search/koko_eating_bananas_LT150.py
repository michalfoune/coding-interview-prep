"""
Problem: Koko Eating Bananas
Source: NeetCode 150 rapid review
Difficulty: Medium
Pattern: Binary search on the answer
Status: Correct final implementation

Prompt:
    Koko has several piles of bananas.

    Each hour, she chooses one pile and eats up to `speed` bananas from it.
    If the pile has fewer than `speed` bananas, she finishes that pile and
    the hour is still spent.

    Given:
        piles: list[int]
        h: int

    Return the minimum integer eating speed such that all piles can be eaten
    within h hours.

Example:
    piles = [3, 6, 7, 11]
    h = 8

    At speed 4:
        pile 3  -> 1 hour
        pile 6  -> 2 hours
        pile 7  -> 2 hours
        pile 11 -> 3 hours

        total = 8 hours

    So speed 4 works, and it is the minimum valid speed.

Core idea:
    This is binary search on the answer.

    We are not searching over array indexes.
    We are searching over possible eating speeds.

Search space:
    Minimum possible speed:
        1

    Maximum necessary speed:
        max(piles)

    Any speed above max(piles) is unnecessary, because Koko can already
    finish any pile in one hour at speed max(piles).

Feasibility check:
    For a candidate speed, compute how many total hours Koko needs.

    For one pile:
        hours = ceil(pile / speed)

    Without importing math.ceil, use integer ceiling division:

        hours = (pile + speed - 1) // speed

Binary search rule:
    If a speed works, try a smaller speed:

        right = mid

    Do not use right = mid - 1 here, because mid itself may be the minimum
    valid answer.

    If a speed is too slow, search higher:

        left = mid + 1

At the end:
    left == right

    That value is the minimum valid speed.

Time:
    O(n log m)

    n = number of piles
    m = max pile size

Space:
    O(1), ignoring input
"""


def min_eating_speed(piles: list[int], h: int) -> int:
    """
    Return the minimum integer speed needed to eat all piles within h hours.

    Uses binary search over possible speeds.

    For each candidate speed, `can_eat` checks whether that speed finishes
    all piles within the allowed number of hours.
    """
    left = 1
    right = max(piles)

    def can_eat(speed: int) -> bool:
        hours_total = 0

        for pile in piles:
            hours = (pile + speed - 1) // speed
            hours_total += hours

        return hours_total <= h

    while left < right:
        mid = (left + right) // 2

        if can_eat(mid):
            right = mid
        else:
            left = mid + 1

    return left


def main():
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23

    # One pile.
    assert min_eating_speed([10], 1) == 10
    assert min_eating_speed([10], 2) == 5
    assert min_eating_speed([10], 10) == 1

    # Already enough time to eat one banana per hour.
    assert min_eating_speed([1, 1, 1, 1], 4) == 1

    # Equal piles.
    assert min_eating_speed([5, 5, 5], 3) == 5
    assert min_eating_speed([5, 5, 5], 6) == 3

    print("All tests passed.")


if __name__ == "__main__":
    main()
