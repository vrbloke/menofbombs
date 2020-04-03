from random import seed as randseed

import pygame as pg
from display import Tile, Board, Window
import entities

'''
Man of Bombs: Ghost Trick game:
Two bomb men run around stage (controlled with WASD and arrow keys). They place bombs in a classic
bomberman style arena
If one is hit by an explosion, he becomes DECEASED and his killer becomes an EXORCIST
The exorcist's explosions can go through walls and cause a 3x3 explosion square around them in addition to the beams
The deceased can move through walls
Game ends when both players are deceased or the deceased is hit by an exorcist bomb 
'''

"""
Pro tips by virtuNat:
1. You can make life easier for you by using from import syntax and aliasing.
2. pygame.display.set_mode needs to only be called exactly once.
3. Even if you lose the screen reference, you can get it back using pygame.display.get_surface.
4. All pygame.Surface related processing should happen after the display mode is set.
5. pygame.time.Clock is your friend for doing frame delays.
6. If certain logic does not need to happen every frame, don't make it happen every frame.
7. You do not have to redraw the entire screen every frame.
8. It is much better to consolidate all related sprites into a single atlas image file and use the
third argument of pygame.Surface.blit to just decide which portion will be blitted to a surface than
to have dozens of separate tiny image files in a textures folder.
9. Instead of hardcoding related keys in long if-elif-else chains, have a table that lets you run
what you need for each set of keys.
10. The main running loop should be in a function to avoid running your game when importing for
compilation into an executable.
"""

__version__ = "0.2 alpha"
__author__ = "vR"

def play_game():
    # CONSTANTS
    board_size = 8*2 + 1  # Must be odd number (2n + 1)
    square_size = 32

    # INIT STUFF
    pg.init()
    pg.display.set_caption(f"Men of Bombs: Ghost Trick v{version}")
    screen = pg.display.set_mode((board_size * square_size, board_size * (square_size + 3)), pg.HWSURFACE | pg.DOUBLEBUF)

    background = pg.image.load("sprites/background.png").convert()
    Tile.atlas = pg.image.load("sprites/spriteatlas.png").convert()
    Tile.atlas.set_colorkey((0, 0, 0))

    board = Board(board_size)
    screen = Window(screen, board, background)
    clock = pg.time.Clock()
    randseed()

    # CREATE ACTORS & VARIABLES
    p1 = entities.Player([3, 3], board, 8)
    p2 = entities.Player([7, 7], board, 9)
    players = (p1, p2)
    frame = 0

    config1 = {pg.K_w: 1, pg.K_d: 2, pg.K_s: 3, pg.K_a: 4}
    config2 = {pg.K_UP: 1, pg.K_RIGHT: 2, pg.K_DOWN: 3, pg.K_LEFT: 4}

    # GAME LOOP
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in config1:
                    p1.movdir = config1[event.key]
                elif event.key == pg.K_e:
                    p1.place_bomb()
                elif event.key in config2:
                    p2.movdir = config2[event.key]
                elif event.key == pg.K_l:
                    p2.place_bomb()
            elif event.type == pg.KEYUP:
                if p1.movdir and event.key in config1:
                    p1.movdir = 0
                elif p2.movdir and event.key in config2:
                    p2.movdir = 0

        if frame == 0:
            # Resolve bomb men
            if p1.bomb: p1.bomb.update()
            if p2.bomb: p2.bomb.update()
            if p1.update(p2):
                running = False
            if p2.update(p1):
                running = False

        # Wait for framerate & update counter & board
        screen.update()
        clock.tick(60)
        frame = (frame + 1) % 10

if __name__ == '__main__':
    play_game()
