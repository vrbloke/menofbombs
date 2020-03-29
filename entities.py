
class Player():
    def __init__(self, position, board, number):
        self.pos = position  # List of 2 numbers
        self.board = board
        self.number = number  # p1 neutral - 8. p2 neutral - 9
        self.velocity = [0, 0]
        self.bombpos = [0, 0]
        self.bomb_timer = 0
        self.bomb_range = 4
        self.explosion_tiles = []

        # Flags
        self.bomb_placed = False  # Set to true on bomb placement, block more bombs till it blows!!
        self.explosion = False
        self.power = False  # Set to true if empowered

    def getx(self):
        return self.pos[0]

    def gety(self):
        return self.pos[1]

    def downgrade(self):
        self.number -= 2

    def upgrade(self):
        self.number += 2

    def change_velocity(self, direction):
        self.velocity = direction

    def move(self):  # 1: Up, 2: Right, 3: Down, 4: Left
        if self.velocity == 1:  # Up
            if self.board[self.pos[0]][self.pos[1] - 1] in (0, 3):
                self.pos[1] -= 1
        elif self.velocity == 2:  # Right
            if self.board[self.pos[0] + 1][self.pos[1]] in (0, 3):
                self.pos[0] += 1
        elif self.velocity == 3:  # Down
            if self.board[self.pos[0]][self.pos[1] + 1] in (0, 3):
                self.pos[1] += 1
        elif self.velocity == 4:  # Left
            if self.board[self.pos[0] - 1][self.pos[1]] in (0, 3):
                self.pos[0] -= 1
        else:  # Stationary
            pass

    def place_bomb(self):
        if not self.bomb_placed and not self.explosion and self.number >= 8:
            self.bombpos = self.pos.copy()
            self.bomb_timer = 13 if not self.power else 20
            self.bomb_placed = True

    def bomb_update(self):
        if self.bomb_placed:
            self.bomb_timer -= 1
            if self.bomb_timer <= 0:
                self.bomb_placed = False
                self.explode()
        elif self.explosion:
                self.explosion = False
                self.explosion_tiles = []

    def explosion_cross(self, bomb_range):
        up = True
        right = True
        left = True
        down = True
        for i in range(bomb_range + 1):
            # I really dont want to rewrite this so i'll just put all these ifs in try blocks so i dont have to worry
            # about indexerrors :) :) :)
            # Up
            if up and (self.power or self.board[self.bombpos[0]][self.bombpos[1] - i] != 1) and self.board[self.bombpos[0]][self.bombpos[1] - i] != 2:
                self.explosion_tiles.append((self.bombpos[0], self.bombpos[1] - i))
            else:
                up = False
            # Right
            if right and (self.power or self.board[self.bombpos[0] + i][self.bombpos[1]] != 1) and self.board[self.bombpos[0] + i][self.bombpos[1]] != 2:
                self.explosion_tiles.append((self.bombpos[0] + i, self.bombpos[1]))
            else:
                right = False
            # Down
            if down and (self.power or self.board[self.bombpos[0]][self.bombpos[1] + i] != 1) and self.board[self.bombpos[0]][self.bombpos[1] + i] != 2:
                self.explosion_tiles.append((self.bombpos[0], self.bombpos[1] + i))
            else:
                down = False
            # Left
            if left and (self.power or self.board[self.bombpos[0] - i][self.bombpos[1]] != 1) and self.board[self.bombpos[0] - i][self.bombpos[1]] != 2:
                self.explosion_tiles.append((self.bombpos[0] - i, self.bombpos[1]))
            else:
                left = False

    def explosion_square(self, side):
        startx = self.bombpos[0] - int(side/2)
        starty = self.bombpos[1] - int(side/2)
        board_size = len(self.board[0])
        for i in range(side + 1):
            for j in range(side + 1):
                if startx + i > 0 and startx + i < board_size and starty + j > 0 and starty + j < board_size:
                    self.explosion_tiles.append((startx + i, starty + j))

    def explode(self):
        if self.number < 10:
            # Cross range 10
            self.explosion_cross(self.bomb_range)
        elif self.number >= 10:
            # Cross range 30 and 4x4 square
            self.explosion_cross(self.bomb_range * 4)
            self.explosion_square(4)
        self.explosion = True
