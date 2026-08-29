import pygame

pygame.init()

WIDTH, HEIGHT = 800, 800
BOARD_SIZE = 8
CELLSIZE = WIDTH // BOARD_SIZE
BOARD_WHITE_COLOR = (240, 236, 183)
BOARD_BLACK_COLOR = (80, 40, 0)


class Game:
    def __init__(self):
        "Инициализация объекта класса"
        self.pos_x = None
        self.pos_y = None

        self.board = [
            ["black_ладья","black_конь","black_слон","black_ферзь","black_король","black_слон","black_конь","black_ладья"],
            ["black_пешка","black_пешка","black_пешка","black_пешка","black_пешка","black_пешка","black_пешка","black_пешка"],
            [0] * 8,
            [0] * 8,
            [0] * 8,
            [0] * 8,
            ["white_пешка","white_пешка","white_пешка","white_пешка","white_пешка","white_пешка","white_пешка","white_пешка"],
            ["white_ладья","white_конь","white_слон","white_ферзь","white_король","white_слон","white_конь","white_ладья"]
        ]

        self.pieces_assets = self.download_assets()

        self.clock = pygame.time.Clock()
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Название")

    def __end__(self):
        "При выходе из игры"
        pygame.quit()

    def pos_to_cell(self, pos_x, pos_y):
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
                piece = pieces_assets.get(row)
                if piece:
                    self.screen.blit(piece, (ind * CELLSIZE, col * CELLSIZE))

    def draw_selected_cell(self, pos_x, pos_y):
        if not pos_x and not pos_y:
            return

        col, row = self.pos_to_cell(pos_x, pos_y)

        highlight = pygame.Surface((CELLSIZE, CELLSIZE), pygame.SRCALPHA)
        highlight.fill((100, 200, 255, 150))
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

    def check_for_piece(self, pos_x, pos_y):
        col, row = self.pos_to_cell(pos_x, pos_y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                self.pos_x, self.pos_y = pos

        return True

    def run(self):
        begin = True

        while begin:
            begin = self.handle_events()

            self.draw_board()
            self.draw_selected_cell(self.pos_x, self.pos_y)
            self.draw_pieces(self.board, self.pieces_assets)

            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()