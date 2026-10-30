import pygame
from moves import *

pygame.init()

WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
CELLSIZE = WIDTH // BOARD_SIZE
BOARD_WHITE_COLOR = (240, 236, 183)
BOARD_BLACK_COLOR = (80, 40, 0)


class Board:
    def __init__(self):
        self.board = self._create_start_board()
        self.row = -1

    def _create_start_board(self):
        board = [[None for i in range(8)] for i in range(8)]

        for i in range(8):
            board[1][i] = Pawn(1, i, "black")

        for i in range(8):
            board[6][i] = Pawn(6, i, "white") 

        # Rooks
        board[0][0], board[0][7] = Rook(0, 0, "black"), Rook(0, 7, "black")
        board[7][0], board[7][7] = Rook(7, 0, "white"), Rook(7, 7, "white")

        # Knights
        board[0][1], board[0][6] = Knight(0, 1, "black"), Knight(0, 6, "black")
        board[7][1], board[7][6] = Knight(7, 1, "white"), Knight(7, 6, "white")

        # Bishops
        board[0][2], board[0][5] = Bishop(0, 2, "black"), Bishop(0, 5, "black")
        board[7][2], board[7][5] = Bishop(7, 2, "white"), Bishop(7, 5, "white")

        # Queens and Kings
        board[0][4], board[7][4] = Queen(0, 4, "black"), Queen(7, 4, "white")
        board[0][3], board[7][3] = King(0, 3, "black"), King(7, 3, "white")

        return board

    def __getitem__(self, index) -> list[Piece]:
        return self.board[index]

    def __len__(self):
        return len(self.board)


class Game:
    def __init__(self):
        "Инициализация объекта класса"
        self.pos_x = None
        self.pos_y = None
        self.move_color = "white"
        self.selected_piece = None

        self.board = Board()

        self.pieces_assets = self.download_assets()

        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Название")

    def __end__(self):
        "При выходе из игры"
        pygame.quit()

    @classmethod
    def pos_to_index(cls, pos_x, pos_y):
        row = pos_x // CELLSIZE
        col = pos_y // CELLSIZE
        return col, row

    @classmethod
    def pos_to_cell(cls, pos_x, pos_y):
        pos_x = pos_x // CELLSIZE
        pos_y = pos_y // CELLSIZE
        return pos_x, pos_y

    def draw_board(self):
        for x in range(CELLSIZE):
            color_num = x
            for y in range(CELLSIZE):
                color_num += 1
                color = BOARD_WHITE_COLOR if color_num % 2 == 0 else BOARD_BLACK_COLOR
                pygame.draw.rect(self.screen, color, (x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE))

    def draw_pieces(self, board, pieces_assets):
        for col in range(len(board)):
            for ind, row in enumerate(board[col]):
                if not isinstance(row, Piece):
                    continue

                piece = pieces_assets.get(f"{row.color}_{row.name}")
                if piece:
                    self.screen.blit(piece, (ind * CELLSIZE, col * CELLSIZE))

    def draw_selected_cell(self, pos_x, pos_y):
        if not pos_x and not pos_y:
            return

        col, row = self.pos_to_cell(pos_x, pos_y)

        highlight = pygame.Surface((CELLSIZE, CELLSIZE), pygame.SRCALPHA)
        highlight.fill((100, 200, 255, 150))
        self.screen.blit(highlight, (col * CELLSIZE, row * CELLSIZE))

    def draw_piece_moves(self, moves):
        for row, col in moves:
            highlight = pygame.Surface((CELLSIZE, CELLSIZE), pygame.SRCALPHA)
            highlight.fill((100, 255, 200, 150))
            self.screen.blit(highlight, (col * CELLSIZE, row * CELLSIZE))

    def download_assets(self, path="images/"):
        pieces = {}
        colors = ["white", "black"]
        piece_types = ["пешка", "ладья", "конь", "слон", "ферзь", "король"]

        for color in colors:
            for piece_type in piece_types:
                image = pygame.image.load(f"{path}{color}_{piece_type}.png")
                image = pygame.transform.scale(image, (CELLSIZE * 0.9, CELLSIZE * 0.9))
                pieces[f"{color}_{piece_type}"] = image

        return pieces

    def get_piece_moves(self, pos_x, pos_y, board):
        if not pos_x or not pos_y:
            return []

        col, row = self.pos_to_index(pos_x, pos_y)

        if board[col][row] and self.board[col][row].color != self.move_color:
            return []

        piece = board[col][row]

        if not piece:
            return []

        color, piece = piece.color, piece.name

        match piece:
            case "пешка":
                return Pawn(col, row, color).get_moves(self.board)
            case "слон":
                return Bishop(col, row, color).get_moves(self.board)
            case "конь":
                return Knight(col, row, color).get_moves(self.board)
            case "ладья":
                return Rook(col, row, color).get_moves(self.board)
            case "ферзь":
                return Queen(col, row, color).get_moves(self.board)
            case "король":
                return King(col, row, color).get_safe_moves(self.board)

        return []

    def check_for_move(self, moves, pos_x, pos_y):
        col, row = self.pos_to_index(pos_x, pos_y)
        return (col, row) in moves

    def move_piece(self, col, row, selected_piece):
        if not selected_piece:
            return

        self.board[col][row] = self.board[selected_piece[0]][selected_piece[1]]
        self.board[selected_piece[0]][selected_piece[1]] = 0

        self.board[col][row].col, self.board[col][row].row = col, row

        self.pos_x, self.pos_y = selected_piece[1] * CELLSIZE, selected_piece[0] * CELLSIZE

        self.move_color = "black" if self.move_color == "white" else "white"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                moves = self.get_piece_moves(self.pos_x, self.pos_y, self.board)

                pos = pygame.mouse.get_pos()
                self.pos_x, self.pos_y = pos

                col, row = self.pos_to_index(self.pos_x, self.pos_y)

                if self.board[col][row] and (col, row) not in moves:
                    self.selected_piece = (col, row)

                if self.check_for_move(moves, self.pos_x, self.pos_y):
                    self.move_piece(col, row, self.selected_piece)

        return True

    def run(self):
        begin = True

        while begin:
            begin = self.handle_events()

            self.draw_board()
            self.draw_selected_cell(self.pos_x, self.pos_y)
            self.draw_pieces(self.board, self.pieces_assets)
            moves = self.get_piece_moves(self.pos_x, self.pos_y, self.board)
            self.draw_piece_moves(moves)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()