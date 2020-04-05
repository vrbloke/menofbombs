import pygame as pg
import display

"""
Pro tips by virtuNat:
1. If you have an item that has its own logic, you probably need to make that a separate object.
2. Update logic should almost exclusively occur inside update methods of the relevant objects to make things easier to manage.
3. try-except is much faster in python than it is in other interpreted languages, don't be afraid to use it.
4. Try to imagine potential edge cases and undefined behavior in your head when implementing methods. If they can be achieved
over the course of execution, deal with them.
"""

wall_tiles = (display.TILE_SWALL, display.TILE_HWALL, display.TILE_BOMB)

class Bomb(pg.sprite.Sprite):
    """The players' bombs."""

    def __init__(self, player):
        super().__init__()
        self.board = player.board
        self.pos = tuple(player.pos)
        self.timer = 20 if player.state == 0 else 13
        self.reach = 4
        self.power = player.state > 0
        self.respawn_fruit = False

    def explode_cross(self, reach):
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            for i in range(1, reach + 1):
                try:
                    tile = self.board[self.pos[0]+dx*i, self.pos[1]+dy*i]
                except KeyError:
                    break
                tile_type = tile.get_tile()
                if tile_type not in wall_tiles:
                    tile.set_tile(display.TILE_BOOM)
                    if tile_type == display.TILE_FRUIT:
                        self.respawn_fruit = True
                elif not self.power:
                    break
        self.board[self.pos].set_tile(5)
    
    def explode_square(self):
        for dy in range(-self.reach//2, self.reach//2 + 1):
            for dx in range(-self.reach//2, self.reach//2 + 1):
                try:
                    tile = self.board[self.pos[0]+dx, self.pos[1]+dy]
                except KeyError:
                    continue
                tile_type = tile.get_tile()
                if tile_type not in wall_tiles:
                    tile.set_tile(display.TILE_BOOM)
                    if tile_type == display.TILE_FRUIT:
                        self.respawn_fruit = True

    def explode(self):
        if self.power:
            self.explode_cross(self.reach * 2)
            self.explode_square()
        else:
            self.explode_cross(self.reach)
        if self.respawn_fruit:
            self.board.spawn_fruit()

    def update(self):
        if self.timer == 1:
            self.explode()
        self.timer = max(-2, self.timer - 1)


class Player(pg.sprite.Sprite):
    """The player sprite."""

    def __init__(self, board, pos, index):
        super().__init__()
        self.board = board
        self.pos = pos # List of 2 numbers
        self.number = index  # p1: 8, p2: 9
        self.state = 0 # -2: dead, +2: empowered
        self.movdir = None # 0: Up, 1: Right, 2: Down, 3: Left, None: None
        self.movstack = [] # Keeps track of key presses
        self.bomb = None # Set to bomb reference, block more bombs till it blows!!

        self.board[tuple(self.pos)].set_tile(self.number)

    def handle_movement(self, movdir, pressed):
        if pressed:
            self.movstack.append(movdir)
            self.movdir = movdir
        else:
            self.movstack.remove(movdir)
            try:
                self.movdir = self.movstack[-1]
            except IndexError:
                self.movdir = None

    def place_bomb(self):
        if self.bomb is None and self.state >= 0:
            self.bomb = Bomb(self)

    def move(self): 
        if self.movdir is not None:
            oldpos = tuple(self.pos)
            self.pos[0] += (0, 1, 0, -1)[self.movdir]
            self.pos[1] += (-1, 0, 1, 0)[self.movdir]
            if self.board[tuple(self.pos)].get_tile() not in (display.TILE_EMPTY, display.TILE_FRUIT):
                self.pos[:] = oldpos
            if self.bomb and oldpos == self.bomb.pos:
                self.board[oldpos].set_tile(4)
            else:
                self.board[oldpos].set_tile(0)

    def update(self, other):
        if self.bomb and self.bomb.timer == -2:
            self.board.clear_debris()
            self.bomb = None
        self.move()
        tile_type = self.board[tuple(self.pos)].get_tile()
        if tile_type == display.TILE_BOOM:
            if self.state < 0:
                return True
            if self.state == 0:
                other.state = 2
                self.state = -2
                self.board.spawn_fruit()
        elif tile_type == display.TILE_FRUIT:
            if self.state < 0:
                self.state = other.state = 0
            elif self.state > 0:
                self.board.spawn_fruit()
        self.board[tuple(self.pos)].set_tile(self.number + self.state)
        return False
