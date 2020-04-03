from typing import Tuple
from random import choice
import pygame as pg

"""
Pro tips by virtuNat:
1. Learn how to do proper object-oriented programming.
2. Always have the documentation of the 3rd party modules you're using open when programming.
3. Group surfaces and rects associated to the same sprite in the same sprite object.
4. Use pygame.sprite.Group instances to manage sprite displays.
5. Minimize the number of pixels blitted per frame.
6. Annotations are not necessary but help a lot in keeping track of what things are.
"""

class Tile(pg.sprite.Sprite):
    """Sprite tile on the board. Each tile is its own sprite."""
    __slots__ = ('image', 'rect', 'clip')
    atlas = None

    def __init__(self, size: int, x: int, y: int) -> None:
        super().__init__()
        self.image = self.atlas
        self.rect = pg.Rect(x*size, y*size, size, size)
        self.clip = self.rect.copy()

    def get_pos(self) -> Tuple[int, int]:
        return (self.rect.x // self.rect.w, self.rect.y // self.rect.h)

    def get_tile(self) -> int:
        return self.clip.x // self.clip.w

    def set_tile(self, index: int) -> None:
        self.clip.x = index * self.clip.w

    def draw(self, dest: pg.Surface) -> None:
        dest.blit(self.image, self.rect, self.clip)


class Board(pg.sprite.Group):
    """
    Container and handler of Tile sprites.
    Not the smartest idea to hold a literal grid of sprites but it's something.
    """

    def __init__(self, size: int) -> None:
        super.__init__()
        self._tiles = {
            (x, y): Tile(size, x, y) for y in range(size) for x in range(size)
            }
        self.size = size
        self.add(self._tiles.values())
        self.reset()

    def __getitem__(self, index: Tuple[int, int]) -> Tile:
        if not isinstance(index, tuple):
            raise TypeError('board indices must be tuples')
        return self._tiles.__getitem__(index)

    def reset(self) -> None:
        # Edges of board wall. Odd numbered tiles also wall.
        for y in range(self.size):
            for x in range(self.size):
                if x == 0 or x == self.size-1 or y == 0 or y == self.size-1:
                    self._tiles[x, y].set_tile(2)
                elif x & 1 or y & 1:
                    self._tiles[x, y].set_tile(0)
                else:
                    self._tiles[x, y].set_tile(1)

    def spawn_fruit(self) -> None:
        sprites = [sprite for sprite in self if sprite.get_tile() == 0]
        choice(sprites).set_tile(3)

    def draw(self, dest: pg.Surface) -> None:
        # This gets pretty horrendously slow pretty fucking quick.
        blitfunc = dest.blit
        for sprite in self._tiles.values():
            blitfunc(sprite.image, sprite.rect, sprite.clip)


class Window(object):
    """Screen handler object."""

    def __init__(self, screen: pg.Surface, board: Board, bg_image: pg.Surface) -> None:
        self.screen = screen
        self.bg_image = bg_image
        self.board = board
        self.font = pg.font.SysFont("Arial", 16)

    def blit_text(self, text: str, pos: tuple) -> None:
        self.screen.blit(self.font.render(text, True, (255, 255, 255)), pos)

    def update(self) -> None:
        self.screen.blit(self.bg_image, (0, 0))
        self.board.draw(self.screen)
        pg.display.flip()
