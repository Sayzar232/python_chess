def get_pawn_moves(col, row, color, board):
    moves = []

    move_side = 1 if color == "black" else -1

    if not board[col + move_side][row]:
        moves.append((col + move_side, row))
    else:
        return moves

    if color == "black" and col == 1:
        if not board[col + 2 * move_side][row]:
            moves.append((col + 2 * move_side, row))
    elif color == "white" and col == 6:
        if not board[col + 2 * move_side][row]:
            moves.append((col + 2 * move_side, row))

    return moves


def get_bishop_moves(col, row, color, board):
    return []


def get_knight_moves(col, row, color, board):
    return []


def get_rook_moves(col, row, color, board):
    return []


def get_queen_moves(col, row, color, board):
    return []


def get_king_moves(col, row, color, board):
    return []