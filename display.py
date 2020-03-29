import pygame

'''
The Display class should be initialized with an array that corresponds to the game board:
This array should be filled with numbers: indexes in a list of sprites to draw on the board
There should also be support for a background image
Python function calls are pass-by-reference so let's hope to jesus this works the way I feel it should!

Alternate version for solid colors: Follow same interface!!
'''
class Display():
    def __init__(self, board, sprites, text, bg_image, board_size, square_size):
        self.board = board  # 2d array, [y][x]
        self.sprites = sprites  # list, holds sprite images or color 3-tuples: index 0 assumed to mean nothing
        self.text = text
        self.bg_image = bg_image  # pygame image, assumed same size as board
        self.board_size = board_size  # integer
        self.square_size = square_size  # Integer
        self.rects = [] # 2d array, [x][y]

    def initialize(self):
        self.screen = pygame.display.set_mode((self.board_size * self.square_size, self.board_size * (self.square_size + 3)))

        for i in range(self.board_size):
            new_row = []
            for j in range(self.board_size):
                new_rect = pygame.Rect(i * self.square_size, j * self.square_size, self.square_size, self.square_size)
                new_row.append(new_rect)
            self.rects.append(new_row)

        self.font = pygame.font.SysFont("Arial", 16)

    def blit(self):
        pass

    def blit_text(self):
        self.screen.blit(self.font.render(self.text, True, (255, 255, 255)), (self.board_size * self.square_size, 0))

    def draw_bg(self):
        pass

    def update(self):
        self.draw_bg()
        self.blit()
        #self.blit_text()
        pygame.display.flip()

class SpriteDisplay(Display):
    def blit(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    pass
                else:
                    index = self.board[i][j]
                    self.screen.blit(self.sprites[index], self.rects[i][j])

    def draw_bg(self):
        self.screen.blit(self.bg_image, pygame.Rect(0, 0, 0, 0))

class SolidColorDisplay(Display):
    def blit(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    pass
                else:
                    index = self.board[i][j]
                    self.screen.fill(self.sprites[index], self.rects[i][j])

    def draw_bg(self):
        self.screen.fill(self.bg_image, pygame.Rect(0, 0, self.board_size*self.square_size, self.board_size*self.square_size))