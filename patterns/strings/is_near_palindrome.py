def is_near_palindrome(text: str) -> bool:
    """
    Return True if text is already a palindrome or can become one by removing
    at most one character.

    This compares characters exactly:
    - case-sensitive
    - spaces and punctuation are treated as normal characters
    - no normalization is applied

    Approach:
    Use two pointers from both ends.
    If characters match, move inward.
    On the first mismatch, try skipping either the left character or the right
    character. If either remaining range is a palindrome, the whole string is
    a near-palindrome.

    Time: O(n)
    Space: O(1)
    """
    left = 0
    right = len(text) - 1

    def is_palindrome_part(left: int, right: int) -> bool:
        while left < right:
            if text[left] != text[right]:
                return False

            left += 1
            right -= 1

        return True

    while left < right:
        if text[left] != text[right]:
            return (
                is_palindrome_part(left + 1, right)
                or is_palindrome_part(left, right - 1)
            )

        left += 1
        right -= 1

    return True


def main():
    assert is_near_palindrome("") is True
    assert is_near_palindrome("a") is True
    assert is_near_palindrome("aa") is True
    assert is_near_palindrome("ab") is True
    assert is_near_palindrome("aba") is True
    assert is_near_palindrome("abca") is True
    assert is_near_palindrome("abc") is False
    assert is_near_palindrome("deeee") is True
    assert is_near_palindrome("racecar") is True
    assert is_near_palindrome("raceacar") is True
    assert is_near_palindrome("abcdef") is False
    assert is_near_palindrome("cbbcc") is True
    assert is_near_palindrome("abbab") is True
    assert is_near_palindrome("abccdba") is True

    print("All tests passed.")


if __name__ == "__main__":
    main()
