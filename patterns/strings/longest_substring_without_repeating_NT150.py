"""
Problem: Longest Substring Without Repeating Characters
Rapid Pattern Drill Problem 1
Pattern: Sliding window, variable size
Status: Yellow-green review item

Prompt:
    Given a string, return the length of the longest substring without
    repeating characters.

Core idea:
    Maintain a window [left, right] with no duplicate characters.
    Move right forward one character at a time.
    If the new character is already in the window, shrink from the left
    until the duplicate is removed.

Trigger phrase:
    Longest substring/subarray satisfying a condition.

Main trap:
    When a duplicate appears, do not just move left by one blindly.
    Shrink until the duplicate is gone.
"""


def length_of_longest_substring(text: str) -> int:
    seen = set()
    left = 0
    best = 0

    for right, char in enumerate(text):
        while char in seen:
            seen.remove(text[left])
            left += 1

        seen.add(char)
        best = max(best, right - left + 1)

    return best


def main():
    assert length_of_longest_substring("") == 0
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
    assert length_of_longest_substring("abcdef") == 6
    print("All tests passed.")


if __name__ == "__main__":
    main()
