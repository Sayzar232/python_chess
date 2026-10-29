class Piece:
    def __init__(self, col: int, row: int, color: str):
        self.col = col
        self.row = row
        self.color = color

    def move(self, move_coord, board):
        board[self.col][self.row] = board[move_coord[0]][move_coord[1]]
        board[move_coord[0]][move_coord[1]] = 0


class Pawn(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.name = "пешка"

    def get_moves(self, board):
        moves = []

        move_side = 1 if self.color == "black" else -1

        if is_valid_move(self.col + move_side, self.row) and not board[self.col + move_side][self.row]:
            moves.append((self.col + move_side, self.row))

        if moves:
            if self.color == "black" and self.col == 1:
                if not board[self.col + 2 * move_side][self.row]:
                    moves.append((self.col + 2 * move_side, self.row))
            elif self.color == "white" and self.col == 6:
                if not board[self.col + 2 * move_side][self.row]:
                    moves.append((self.col + 2 * move_side, self.row))

        if is_valid_move(self.col + move_side, self.row + 1):
            take_move_piece = board[self.col + move_side][self.row + 1]

            if take_move_piece and take_move_piece.color != self.color:
                moves.append((self.col + move_side, self.row + 1))

        if is_valid_move(self.col + move_side, self.row - 1):
            take_move_piece = board[self.col + move_side][self.row - 1]

            if take_move_piece and take_move_piece.color != self.color:
                moves.append((self.col + move_side, self.row - 1))

        return moves


class Bishop(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.name = "слон"

    def get_moves(self, board):
        moves = []
        
        piece_directions = [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1)
        ]
        
        for move in piece_directions:
            for i in range(1, 8):
                coord = (move[0] * i + self.col, move[1] * i + self.row)
        
                if not is_valid_move(*coord):
                    break
        
                take_piece = get_take_piece_color(board, coord)
        
                # If cell is empty
                if not take_piece:
                    moves.append(coord)
                # If cell is teammate
                elif take_piece == self.color:
                    break
                # If cell is opponent
                else:
                    moves.append(coord)
                    break
        
        return moves


class Rook(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.name = "ладья"

    def get_moves(self, board):
        moves = []
        
        piece_directions = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1)
        ]

        for move in piece_directions:
            for i in range(1, 8):
                coord = (move[0] * i + self.col, move[1] * i + self.row)
        
                if not is_valid_move(*coord):
                    break
        
                take_piece = get_take_piece_color(board, coord)
        
                # If cell is empty
                if not take_piece:
                    moves.append(coord)
                # If cell is teammate
                elif take_piece == self.color:
                    break
                    # If cell is opponent
                else:
                    moves.append(coord)
                    break
        
        return moves


class Knight(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.name = "конь"

    def get_moves(self, board):
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
            coord = (move[0] + self.col, move[1] + self.row)
        
            if not is_valid_move(*coord):
                continue
        
            take_piece = get_take_piece_color(board, coord)
        
            if take_piece != self.color:
                moves.append(coord)
        
        return moves
        


class Queen(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.name = "ферзь"

    def get_moves(self, board):
        horizontal_moves = Rook(self.col, self.row, self.color).get_moves(board)
        diagonal_moves = Bishop(self.col, self.row, self.color).get_moves(board)

        return horizontal_moves + diagonal_moves


class King(Piece):
    def __init__(self, col, row, color):
        super().__init__(col, row, color)
        self.name = "король"

    def get_king_directions(self):
        piece_directions = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
            
                piece_directions.append((i, j))
    
        return piece_directions

    def get_moves(self, board):
        moves = []
    
        piece_directions = self.get_king_directions()
    
        for move in piece_directions:
            coord = (move[0] + self.col, move[1] + self.row)
    
            if not is_valid_move(*coord):
                continue
    
            take_piece = get_take_piece_color(board, coord)
    
            if take_piece != self.color:
                moves.append(coord)
    
        return moves

    def get_safe_moves(self, board):
        moves = []
        
        piece_directions = self.get_king_directions()
    
        for move in piece_directions:
            coord = (move[0] + self.col, move[1] + self.row)
    
            if not is_valid_move(*coord):
                continue
    
            take_piece = get_take_piece_color(board, coord)
    
            if take_piece != self.color:
                if self.check_king_moves(coord, board):
                    moves.append(coord)
    
        return moves

    def check_king_moves(self, coord, board):
        board_ = self.change_king_coord(coord, get_copy_board(board))
        if not self.is_king_in_check(board_):
            return True
        return False

    def is_king_in_check(self, board):
        opponent_color = "black" if self.color == "white" else "white"
        opponent_moves = get_all_moves(opponent_color, board)

        return (self.col, self.row) in opponent_moves

    def change_king_coord(self, coord, board):
        if not is_valid_move(self.col, self.row):
            return

        board[coord[0]][coord[1]] = board[self.col][self.row]
        board[self.col][self.row] = 0

        return board


def is_valid_move(col, row):
    """Check is move is valid"""
    return 0 <= col < 8 and 0 <= row < 8


def get_take_piece_color(board, coord):
    """Check if cell is empty or has a piece"""
    take_piece = 0
    if board[coord[0]][coord[1]]:
        take_piece = board[coord[0]][coord[1]].color

    return take_piece


def get_all_moves(color, board):
    moves = []

    for col in range(len(board)):
        for row, piece in enumerate(board[col]):
            if not piece:
                continue

            piece = piece.name

            coord = (col, row)

            piece_color = get_take_piece_color(board, coord)

            if color == piece_color:
                piece_data = (col, row, color)
                match piece:
                    case "пешка":
                        piece_moves = Pawn(*piece_data).get_moves(board)
                        moves.extend(piece_moves)
                    case "слон":
                        piece_moves = Bishop(*piece_data).get_moves(board)
                        moves.extend(piece_moves)
                    case "конь":
                        piece_moves = Knight(*piece_data).get_moves(board)
                        moves.extend(piece_moves)
                    case "ладья":
                        piece_moves = Rook(*piece_data).get_moves(board)
                        moves.extend(piece_moves)
                    case "ферзь":
                        piece_move = Queen(*piece_data).get_moves(board)
                        moves.extend(piece_moves)
                    case "король":
                        piece_moves = King(*piece_data).get_moves(board)
                        moves.extend(piece_moves)

    return moves


def get_copy_board(board):
    return [row.copy() for row in board]