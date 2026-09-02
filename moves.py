def is_valid_move(col, row):
    return 0 <= col < 8 and 0 <= row < 8

def get_pawn_moves(col, row, color, board):
    moves = []

    move_side = 1 if color == "black" else -1

    if is_valid_move(col + move_side, row) and not board[col + move_side][row]:
        moves.append((col + move_side, row))

    if moves:
        if color == "black" and col == 1:
            if not board[col + 2 * move_side][row]:
                moves.append((col + 2 * move_side, row))
        elif color == "white" and col == 6:
            if not board[col + 2 * move_side][row]:
                moves.append((col + 2 * move_side, row))

    if is_valid_move(col + move_side, row + 1):
        take_move_piece = board[col + move_side][row + 1]

        if take_move_piece and take_move_piece.split("_")[0] != color:
            moves.append((col + move_side, row + 1))

    if is_valid_move(col + move_side, row - 1):
        take_move_piece = board[col + move_side][row - 1]

        if take_move_piece and take_move_piece.split("_")[0] != color:
            moves.append((col + move_side, row - 1))

    return moves


def get_bishop_moves(col, row, color, board):
    moves = []

    

    return []


def get_knight_moves(col, row, color, board):
    return []


def get_rook_moves(col, row, color, board):
    return []


def get_queen_moves(col, row, color, board):
    return []


def get_king_moves(col, row, color, board):
    return []