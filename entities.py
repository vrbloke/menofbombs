import pygame as pg

"""
Pro tips by virtuNat:
1. If you have an item that has its own logic, you probably need to make that a separate object.
2. Update logic should almost exclusively occur inside update methods of the relevant objects to make things easier to manage.
3. try-except is much faster in python than it is in other interpreted languages, don't be afraid to use it.
4. Try to imagine potential edge cases and undefined behavior in your head when implementing methods. If they can be achieved
over the course of execution, deal with them.
"""

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
        for dx, dy in ((0, 1) (1, 0), (0, -1), (-1, 0)):
            for i in range(reach + 1):
                tile = self.board[self.pos[0]+dx, self.pos[1]+dy]
                tile_type = tile.get_tile()
                if tile_type not in (1, 2, 4):
                    tile.set_tile(5)
                    if tile_type == 3:
                        self.respawn_fruit = True
                elif not self.power:
                    break
    
    def explode_square(self):
        for dy in range(-self.reach//2, self.reach//2 + 1):
            for dx in range(-self.reach//2, self.reach//2 + 1):
                try:
                    tile = self.board[self.pos[0]+dx, self.pos[1]+dy]
                except KeyError:
                    continue
                tile_type = tile.get_tile()
                if tile_type not in (1, 2, 4):
                    tile.set_tile(5)
                    if tile_type == 3:
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
        else:
            self.board[self.pos].set_tile(4)
        self.timer = min(0, self.timer - 1)


class Player(pg.sprite.Sprite):
    """The player sprite."""

    def __init__(self, board, pos, index):
        super().__init__()
        self.board = board
        self.pos = pos # List of 2 numbers
        self.number = index  # p1: 8, p2: 9
        self.state = 0 # -2: dead, +2: empowered
        self.movdir = 0
        self.bomb = None # Set to bomb reference, block more bombs till it blows!!

    def move(self): # 0: None, 1: Up, 2: Right, 3: Down, 4: Left
        oldpos = self.pos[:]
        self.pos[0] = (0, 0, 1, 0, -1)[self.movdir]
        self.pos[1] = (0, -1, 0, 1, 0)[self.movdir]
        if self.movdir and self.board[tuple(self.pos)].get_tile() not in (0, 3):
            self.pos[:] = oldpos 

    def place_bomb(self):
        if self.bomb is not None and self.state >= 0:
            self.bomb = Bomb(self)

    def update(self, other):
        self.move()
        if self.bomb and self.bomb.timer == 0:
            self.bomb = None
        tile_type = self.board[tuple(self.pos)].get_tile()
        if self.state < 0:
            if tile_type == 3:
                self.state = other.state = 0
            elif tile_type == 5:
                return True
        elif self.state == 0 and tile_type == 5:
            other.state = 2
            self.state = -2
            self.board.spawn_fruit()
        self.board[tuple(self.pos)].set_tile(self.number + self.state)
        return False
