from functools import lru_cache


def is_palindrome_with_deletions(text: str, max_deletions: int) -> bool:
    """
    Return True if text can become a palindrome by deleting at most
    max_deletions characters.

    This is a dynamic programming / memoized recursion twist on the
    near-palindrome problem.

    Interview explanation:
        I compute the minimum number of deletions needed to make
        text[left:right] a palindrome.

        If the outer characters match, no deletion is needed there,
        so I move inward.

        If they differ, I must delete either the left character or the right
        character, so I take 1 plus the cheaper of those two recursive options.

        At the end, I compare the minimum deletions needed with max_deletions.

    Time: O(n^2)
    Space: O(n^2)
    """
    if max_deletions < 0:
        return False

    @lru_cache(maxsize=None)
    def min_deletions_needed(left: int, right: int) -> int:
        if left >= right:
            return 0

        if text[left] == text[right]:
            return min_deletions_needed(left + 1, right - 1)

        delete_left = 1 + min_deletions_needed(left + 1, right)
        delete_right = 1 + min_deletions_needed(left, right - 1)

        return min(delete_left, delete_right)

    return min_deletions_needed(0, len(text) - 1) <= max_deletions


def main():
    assert is_palindrome_with_deletions("", 0) is True
    assert is_palindrome_with_deletions("a", 0) is True
    assert is_palindrome_with_deletions("aba", 0) is True
    assert is_palindrome_with_deletions("abca", 1) is True
    assert is_palindrome_with_deletions("abc", 1) is False
    assert is_palindrome_with_deletions("abc", 2) is True
    assert is_palindrome_with_deletions("abcdef", 5) is True
    assert is_palindrome_with_deletions("abcdef", 4) is False
    assert is_palindrome_with_deletions("raceacar", 1) is True
    assert is_palindrome_with_deletions("abccdba", 1) is True
    assert is_palindrome_with_deletions("abxcdba", 1) is True
    assert is_palindrome_with_deletions("abxycdba", 2) is True
    assert is_palindrome_with_deletions("abxycdba", 1) is False
    assert is_palindrome_with_deletions("abcda", 2) is True
    assert is_palindrome_with_deletions("abcda", 1) is False
    assert is_palindrome_with_deletions("abc", -1) is False

    print("All tests passed.")


if __name__ == "__main__":
    main()
