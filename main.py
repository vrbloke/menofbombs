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
    pg.display.set_caption(f"Men of Bombs: Ghost Trick v{__version__}")
    screen = pg.display.set_mode((board_size * square_size, board_size * (square_size + 3)), pg.HWSURFACE | pg.DOUBLEBUF)

    background = pg.image.load("sprites/background.png").convert()
    Tile.atlas = pg.image.load("sprites/spriteatlas.png").convert()
    Tile.atlas.set_colorkey(0x000000)

    board = Board(board_size, square_size)
    screen = Window(screen, board, background)
    clock = pg.time.Clock()
    randseed()

    config1 = {pg.K_w: 0, pg.K_d: 1, pg.K_s: 2, pg.K_a: 3}
    config2 = {pg.K_UP: 0, pg.K_RIGHT: 1, pg.K_DOWN: 2, pg.K_LEFT: 3}
    frame = 0

    # CREATE ACTORS & VARIABLES
    p1 = entities.Player(board, [3, 3], 8)
    p2 = entities.Player(board, [9, 9], 9)

    # GAME LOOP
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key in config1:
                    p1.handle_movement(config1[event.key], True)
                elif event.key == pg.K_e:
                    p1.place_bomb()
                elif event.key in config2:
                    p2.handle_movement(config2[event.key], True)
                elif event.key == pg.K_l:
                    p2.place_bomb()
            elif event.type == pg.KEYUP:
                if event.key in config1:
                    p1.handle_movement(config1[event.key], False)
                elif event.key in config2:
                    p2.handle_movement(config2[event.key], False)

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
