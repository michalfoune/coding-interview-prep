from functools import lru_cache

WHITE = "w"
BLACK = "b"

EMPTY = "."

BOARD_SIZE = 8

# Uppercase = white, lowercase = black
# K/k = king
# Q/q = queen
# R/r = rook
# B/b = bishop


def opposite(side: str) -> str:
    return BLACK if side == WHITE else WHITE


def piece_side(piece: str) -> str | None:
    if piece == EMPTY:
        return None
    return WHITE if piece.isupper() else BLACK


def in_bounds(row: int, col: int) -> bool:
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def get_piece(board: tuple[str, ...], row: int, col: int) -> str:
    return board[row][col]


def set_piece(board: tuple[str, ...], row: int, col: int, piece: str) -> tuple[str, ...]:
    board_as_lists = [list(line) for line in board]
    board_as_lists[row][col] = piece
    return tuple("".join(line) for line in board_as_lists)


def make_move(
    board: tuple[str, ...],
    from_row: int,
    from_col: int,
    to_row: int,
    to_col: int,
) -> tuple[str, ...]:
    piece = get_piece(board, from_row, from_col)
    board = set_piece(board, from_row, from_col, EMPTY)
    board = set_piece(board, to_row, to_col, piece)
    return board


def find_king(board: tuple[str, ...], side: str) -> tuple[int, int]:
    target = "K" if side == WHITE else "k"

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == target:
                return row, col

    raise ValueError(f"No king found for side {side}")


def sliding_moves(
    board: tuple[str, ...],
    row: int,
    col: int,
    directions: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    result = []
    moving_piece = get_piece(board, row, col)
    moving_side = piece_side(moving_piece)

    for row_delta, col_delta in directions:
        current_row = row + row_delta
        current_col = col + col_delta

        while in_bounds(current_row, current_col):
            target_piece = get_piece(board, current_row, current_col)
            target_side = piece_side(target_piece)

            if target_piece == EMPTY:
                result.append((current_row, current_col))
            else:
                if target_side != moving_side:
                    result.append((current_row, current_col))
                break

            current_row += row_delta
            current_col += col_delta

    return result


def pseudo_moves_for_piece(
    board: tuple[str, ...],
    row: int,
    col: int,
) -> list[tuple[int, int]]:
    piece = get_piece(board, row, col)

    if piece == EMPTY:
        return []

    side = piece_side(piece)
    piece_type = piece.upper()

    if piece_type == "K":
        result = []

        for row_delta in [-1, 0, 1]:
            for col_delta in [-1, 0, 1]:
                if row_delta == 0 and col_delta == 0:
                    continue

                next_row = row + row_delta
                next_col = col + col_delta

                if not in_bounds(next_row, next_col):
                    continue

                target_piece = get_piece(board, next_row, next_col)
                target_side = piece_side(target_piece)

                if target_piece == EMPTY or target_side != side:
                    result.append((next_row, next_col))

        return result

    if piece_type == "R":
        return sliding_moves(
            board,
            row,
            col,
            directions=[
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
            ],
        )

    if piece_type == "B":
        return sliding_moves(
            board,
            row,
            col,
            directions=[
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ],
        )

    if piece_type == "Q":
        return sliding_moves(
            board,
            row,
            col,
            directions=[
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1),
            ],
        )

    return []


def is_square_attacked(
    board: tuple[str, ...],
    row: int,
    col: int,
    by_side: str,
) -> bool:
    for from_row in range(BOARD_SIZE):
        for from_col in range(BOARD_SIZE):
            piece = get_piece(board, from_row, from_col)

            if piece == EMPTY:
                continue

            if piece_side(piece) != by_side:
                continue

            attacked_squares = pseudo_moves_for_piece(board, from_row, from_col)

            if (row, col) in attacked_squares:
                return True

    return False


def is_in_check(board: tuple[str, ...], side: str) -> bool:
    king_row, king_col = find_king(board, side)
    return is_square_attacked(board, king_row, king_col, opposite(side))


def generate_legal_moves(
    board: tuple[str, ...],
    side: str,
) -> list[tuple[tuple[int, int], tuple[int, int], tuple[str, ...]]]:
    result = []

    for from_row in range(BOARD_SIZE):
        for from_col in range(BOARD_SIZE):
            piece = get_piece(board, from_row, from_col)

            if piece == EMPTY:
                continue

            if piece_side(piece) != side:
                continue

            for to_row, to_col in pseudo_moves_for_piece(board, from_row, from_col):
                target_piece = get_piece(board, to_row, to_col)

                # Important simplification fix:
                # A legal chess move never captures the king.
                if target_piece in ("K", "k"):
                    continue

                next_board = make_move(board, from_row, from_col, to_row, to_col)

                # A legal move cannot leave your own king in check.
                if not is_in_check(next_board, side):
                    result.append(
                        (
                            (from_row, from_col),
                            (to_row, to_col),
                            next_board,
                        )
                    )

    return result


def is_checkmate(board: tuple[str, ...], side: str) -> bool:
    if not is_in_check(board, side):
        return False

    return len(generate_legal_moves(board, side)) == 0


@lru_cache(maxsize=None)
def can_force_checkmate(
    board: tuple[str, ...],
    side_to_move: str,
    attacker: str,
    plies_remaining: int,
) -> bool:
    """
    Return True if attacker can force checkmate within plies_remaining.

    A ply is a half-move:
    - White move = 1 ply
    - Black reply = 1 ply

    This is minimax:

    If attacker moves:
        attacker needs at least one move that guarantees mate.

    If defender moves:
        every legal defender response must still allow forced mate.
    """
    defender = opposite(attacker)

    if is_checkmate(board, defender):
        return True

    if plies_remaining == 0:
        return False

    legal_moves = generate_legal_moves(board, side_to_move)

    # Stalemate or no legal move without check is not checkmate.
    if not legal_moves:
        return False

    next_side = opposite(side_to_move)

    if side_to_move == attacker:
        # Attacker chooses the best move.
        return any(
            can_force_checkmate(next_board, next_side, attacker, plies_remaining - 1)
            for _, _, next_board in legal_moves
        )

    # Defender chooses the move that avoids mate if possible.
    return all(
        can_force_checkmate(next_board, next_side, attacker, plies_remaining - 1)
        for _, _, next_board in legal_moves
    )


def print_board(board: tuple[str, ...]) -> None:
    for row in board:
        print(row)
    print()


def main():
    # Test Case 1
    # Coordinates:
    # row 0 = rank 8
    # row 7 = rank 1
    #
    # This position:
    # black king on a8
    # white queen on b6
    # white king on c6
    #
    # White can play Qb7#.
    board = (
        "k.......",
        "........",
        ".QK.....",
        "........",
        "........",
        "........",
        "........",
        "........",
    )

    print("Initial board:")
    print_board(board)

    assert can_force_checkmate(
        board=board,
        side_to_move=WHITE,
        attacker=WHITE,
        plies_remaining=1,
    ) is True

    print("White can force checkmate in 1 ply.")

    # Already checkmated position:
    # black king on a8
    # white queen on b7
    # white king on c6
    checkmate_board = (
        "k.......",
        ".Q......",
        "..K.....",
        "........",
        "........",
        "........",
        "........",
        "........",
    )

    assert is_checkmate(checkmate_board, BLACK) is True

    print("Checkmate board detected correctly.")

    # Test Case 2
    # Coordinates:
    # row 0 = rank 8
    # row 7 = rank 1
    #
    # This position:
    # black king on h8
    # white queen on h1
    # white king on a1
    #
    # This is not intended as a mate-in-1 puzzle.
    # It is a deeper king-and-queen-vs-king endgame search position.
    # White should be able to force checkmate with enough search depth.
    board_2 = (
        ".......k",
        "........",
        "........",
        "........",
        "........",
        "........",
        "........",
        "K......Q",
    )

    print("Initial board #2:")
    print_board(board_2)

    # Shallow depth should not be enough.
    can_force_checkmate.cache_clear()

    assert can_force_checkmate(
        board=board_2,
        side_to_move=WHITE,
        attacker=WHITE,
        plies_remaining=3,
    ) is False

    print("White cannot force checkmate in only 3 plies.")

    # Deeper depth should be enough.
    # 14 plies = approximately 7 full chess moves.
    can_force_checkmate.cache_clear()

    assert can_force_checkmate(
        board=board_2,
        side_to_move=WHITE,
        attacker=WHITE,
        plies_remaining=14,
    ) is True

    print("White can force checkmate within 14 plies.")


    # Optional calibration:
    # Find the smallest ply depth where the simplified engine sees forced mate.
    for depth in range(1, 21):
        can_force_checkmate.cache_clear()

        if can_force_checkmate(
            board=board_2,
            side_to_move=WHITE,
            attacker=WHITE,
            plies_remaining=depth,
        ):
            print("First forced checkmate depth for board #2:", depth, "plies")
            break
    
    # Test Case 3
    # Coordinates:
    # row 0 = rank 8
    # row 7 = rank 1
    #
    # This position:
    # black king on d4
    # white king on a1
    # white queen on h1
    #
    # This is a deeper king-and-queen-vs-king search position.
    # The black king starts near the center, so White should need more depth
    # to force checkmate than in the corner/endgame examples.
    board_3 = (
        "........",
        "........",
        "........",
        "........",
        "...k....",
        "........",
        "........",
        "K......Q",
    )

    print("Initial board #3:")
    print_board(board_3)

    # Shallow depth should not be enough.
    can_force_checkmate.cache_clear()

    assert can_force_checkmate(
        board=board_3,
        side_to_move=WHITE,
        attacker=WHITE,
        plies_remaining=6,
    ) is False

    print("White cannot force checkmate in only 6 plies.")

    # Calibration:
    # Find the smallest ply depth where this simplified engine sees forced mate.
    first_forced_depth = None

    for depth in range(1, 31):
        can_force_checkmate.cache_clear()

        if can_force_checkmate(
            board=board_3,
            side_to_move=WHITE,
            attacker=WHITE,
            plies_remaining=depth,
        ):
            first_forced_depth = depth
            print("First forced checkmate depth for board #3:", depth, "plies")
            break

    assert first_forced_depth is not None

    # Optional deeper assertion.
    # This is the real "20-ish ply" test.
    can_force_checkmate.cache_clear()

    assert can_force_checkmate(
        board=board_3,
        side_to_move=WHITE,
        attacker=WHITE,
        plies_remaining=20,
    ) is True

    print("White can force checkmate within 20 plies.")

    print("All test cases passed.")

if __name__ == "__main__":
    main()