"""
Problem: Encode and Decode Strings
Source: NeetCode 150 rapid review
Difficulty: Medium
Mode: Rapid-fire implementation
Authorship: Written by me after discussing the index-scanning approach
Date: 2026-06-27
Pattern: String serialization / parsing
Status: Correct 10/10 after minor syntax cleanup

Prompt:
    Design two functions:
        encode(strings: list[str]) -> str
        decode(encoded: str) -> list[str]

    The goal is to convert a list of strings into a single string and then
    recover the original list exactly.

Why delimiter-only encoding is unsafe:
    If we simply do "#".join(strings), decoding breaks when one of the input
    strings itself contains "#".

Safe encoding strategy:
    Store each string as:

        length#string

    Example:
        ["api", "db", "auth"]
        -> "3#api2#db4#auth"

    Example with special characters:
        ["api#1", "", "x"]
        -> "5#api#10#1#x"

    The decoder reads:
        1. digits until "#"
        2. convert digits to length
        3. read exactly length characters
        4. move index to the next encoded item

Key invariant:
    At the beginning of every decode loop, i points to the first digit of the
    next length prefix.

Time:
    O(n), where n is the total number of characters across all strings.

Space:
    O(n), for the encoded string or decoded list.
"""


def encode(strings: list[str]) -> str:
    """
    Encode a list of strings into one string using length-prefix encoding.

    Each string becomes:

        <length>#<string>

    This is safe even if the string itself contains "#", digits, spaces,
    punctuation, or is empty.
    """
    result = []

    for value in strings:
        result.append(str(len(value)))
        result.append("#")
        result.append(value)

    return "".join(result)


def decode(encoded: str) -> list[str]:
    """
    Decode a string produced by encode(...) back into the original list.

    Index choreography:

        i = start of the next length prefix
        j = scans forward until "#"

    Then:

        encoded[i:j] gives the length
        j + 1 is the start of the actual string
        start + length is the end of the actual string
        i moves to end for the next loop
    """
    i = 0
    result = []

    while i < len(encoded):
        j = i

        while encoded[j] != "#":
            j += 1

        length = int(encoded[i:j])
        start = j + 1
        end = start + length

        result.append(encoded[start:end])

        i = end

    return result


def main():
    test_cases = [
        [],
        [""],
        ["api"],
        ["api", "db", "auth"],
        ["api#1", "", "hello/world", "a:b:c"],
        ["#", "##", "###"],
        ["123", "45#67", ""],
        ["spaces are ok", " leading", "trailing "],
        ["unicode-český", "emoji-🙂", ""],
        ["0", "00", "000"],
    ]

    for original in test_cases:
        encoded = encode(original)
        decoded = decode(encoded)

        assert decoded == original, (
            f"Failed round trip:\n"
            f"original={original!r}\n"
            f"encoded={encoded!r}\n"
            f"decoded={decoded!r}"
        )

    # Explicit known encodings.
    assert encode(["api", "db", "auth"]) == "3#api2#db4#auth"
    assert decode("3#api2#db4#auth") == ["api", "db", "auth"]

    assert encode(["api#1", "", "x"]) == "5#api#10#1#x"
    assert decode("5#api#10#1#x") == ["api#1", "", "x"]

    print("All tests passed.")


if __name__ == "__main__":
    main()
