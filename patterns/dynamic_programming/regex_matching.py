from functools import lru_cache


def is_match(s: str, p: str) -> bool:
    """
    Return True if pattern p matches the entire string s. (~LeetCode HARD)

    Supported pattern syntax:
    - "." matches any single character
    - "*" means zero or more of the previous pattern character

    Important:
    "*" does not mean "anything" by itself.
    It modifies the previous character.

    Examples:
    - "a*" means "", "a", "aa", "aaa", ...
    - ".*" means any sequence of characters

    Dynamic programming idea:
    match(i, j) means:
        Does s[i:] match p[j:]?

    Time: O(len(s) * len(p))
    Space: O(len(s) * len(p))
    """

    @lru_cache(maxsize=None)
    def match(i: int, j: int) -> bool:
        # If the pattern is exhausted, the string must also be exhausted.
        if j == len(p):
            return i == len(s)

        first_match = (
            i < len(s)
            and (p[j] == s[i] or p[j] == ".")
        )

        next_is_star = (
            j + 1 < len(p)
            and p[j + 1] == "*"
        )

        if next_is_star:
            # Option 1: use zero copies of p[j], so skip "x*".
            use_zero = match(i, j + 2)

            # Option 2: if current char matches, consume one char from s,
            # but stay at same pattern j because "*" may consume more.
            use_one_or_more = first_match and match(i + 1, j)

            return use_zero or use_one_or_more

        # Normal case: current chars must match, then both move forward.
        return first_match and match(i + 1, j + 1)

    return match(0, 0)


def main():
    assert is_match("aa", "a") is False
    assert is_match("aa", "a*") is True
    assert is_match("ab", ".*") is True
    assert is_match("aab", "c*a*b") is True
    assert is_match("mississippi", "mis*is*p*.") is False

    assert is_match("", "") is True
    assert is_match("", "c*") is True
    assert is_match("", ".*") is True
    assert is_match("abc", "abc") is True
    assert is_match("abc", "a.c") is True
    assert is_match("abc", "ab*bc") is True
    assert is_match("aaa", "a*a") is True
    assert is_match("aaa", "ab*a*c*a") is True
    assert is_match("abcd", "d*") is False
    assert is_match("ab", ".*c") is False

    print("All tests passed.")


if __name__ == "__main__":
    main()
