def is_valid_move(col, row):
    """Check is move is valid"""
    return 0 <= col < 8 and 0 <= row < 8


def get_take_piece_color(board, coord):
    """Check if cell is empty or has a piece"""
    take_piece = 0
    if board[coord[0]][coord[1]]:
        take_piece = board[coord[0]][coord[1]].split("_")[0]

    return take_piece


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

    piece_directions = [
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]

    for move in piece_directions:
        for i in range(1, 8):
            coord = (move[0] * i + col, move[1] * i + row)

            if not is_valid_move(*coord):
                break

            take_piece = get_take_piece_color(board, coord)

            # If cell is empty
            if not take_piece:
                moves.append(coord)
            # If cell is teammate
            elif take_piece == color:
                break
            # If cell is opponent
            else:
                moves.append(coord)
                break

    return moves


def get_rook_moves(col, row, color, board):
    moves = []

    piece_directions = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1)
    ]

    for move in piece_directions:
        for i in range(1, 8):
            coord = (move[0] * i + col, move[1] * i + row)

            if not is_valid_move(*coord):
                break

            take_piece = get_take_piece_color(board, coord)

            # If cell is empty
            if not take_piece:
                moves.append(coord)
            # If cell is teammate
            elif take_piece == color:
                break
                # If cell is opponent
            else:
                moves.append(coord)
                break

    return moves


def get_knight_moves(col, row, color, board):
    moves = []

    piece_directions = [
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
        (2, 1),
        (2, -1),
        (-2, 1),
        (-2, -1)
    ]

    for move in piece_directions:
        coord = (move[0] + col, move[1] + row)

        if not is_valid_move(*coord):
            continue

        take_piece = get_take_piece_color(board, coord)

        if take_piece != color:
            moves.append(coord)

    return moves


def get_queen_moves(col, row, color, board):
    horizontal_moves = get_rook_moves(col, row, color, board)
    diagonal_moves = get_bishop_moves(col, row, color, board)

    return horizontal_moves + diagonal_moves


def get_king_moves(col, row, color, board):
    moves = []

    piece_directions = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue

            piece_directions.append((i, j))

    for move in piece_directions:
        coord = (move[0] + col, move[1] + row)

        if not is_valid_move(*coord):
            continue

        take_piece = get_take_piece_color(board, coord)

        if take_piece != color:
            moves.append(coord)

    return moves


def get_all_moves(color, board):
    moves = []

    for col in range(len(board)):
        for row, piece in enumerate(board[col]):
            if not piece:
                continue

            piece = piece.split("_")[1]

            coord = (col, row)

            piece_color = get_take_piece_color(board, coord)

            if color == piece_color:
                piece_data = (col, row, color, board)
                match piece:
                    case "пешка":
                        piece_moves = get_pawn_moves(*piece_data)
                        moves.extend(piece_moves)
                    case "слон":
                        piece_moves = get_bishop_moves(*piece_data)
                        moves.extend(piece_moves)
                    case "конь":
                        piece_moves = get_knight_moves(*piece_data)
                        moves.extend(piece_moves)
                    case "ладья":
                        piece_moves = get_rook_moves(*piece_data)
                        moves.extend(piece_moves)
                    case "ферзь":
                        piece_moves = get_queen_moves(*piece_data)
                        moves.extend(piece_moves)
                    case "король":
                        piece_moves = get_king_moves(*piece_data)
                        moves.extend(piece_moves)

    return moves