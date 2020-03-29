import pygame, random, timeit
import entities, display

'''
Man of Bombs: Ghost Trick game:
Two bomb men run around stage (controlled with WASD and arrow keys). They place bombs in a classic
bomberman style arena
If one is hit by an explosion, he becomes DECEASED and his killer becomes an EXORCIST
The exorcist's explosions can go through walls and cause a 3x3 explosion square around them in addition to the beams
The deceased can move through walls
Game ends when both players are deceased or the deceased is hit by an exorcist bomb 
'''

'''
TODO:
Primary goal: Make system for translating arrays into 16x16 square graphics
'''

# FUNCTIONS
def random_coords():
    return (random.choice(range(1, board_size, 2)), random.choice(range(1, board_size, 2)))

# CONSTANTS
board_size = 17  # Must be uneven
square_size = 32
version = 0.1

# SPRITES
colors_old = ["Empty", (100, 100, 100), (120, 100, 100),
          (255, 255, 255), (100, 0, 0), (100, 100, 0),
          (0, 0, 100), (0, 100, 0), (0, 0, 200),
          (0, 200, 0), (100, 100, 255), (100, 255, 100)]
colors = [pygame.image.load("wall.png"), pygame.image.load("wall.png"), pygame.image.load("wall.png"),
          pygame.image.load("ghostfruit.png"), pygame.image.load("bomb.png"), pygame.image.load("explosion.png"),
          pygame.image.load("player1ghost.png"), pygame.image.load("player2ghost.png"), pygame.image.load("player1.png"),
          pygame.image.load("player2.png"), pygame.image.load("player1emp.png"), pygame.image.load("player2emp.png")]
for sprite in colors:
    sprite.set_colorkey((0, 0, 0))
# 0: nothing 1: wall 2: hardwall
# 3: ghostfruit 4: bomb 5: explosion
# 6: p1 ghost 7: p2 ghost 8: p1
# 9: p2  10: p1 emp 11: p2 emp
background = pygame.image.load("background.png")
background_old = (0, 0, 0)

# BOARD
board = []  # Holds entities represented by a number. The index is location.
for i in range(board_size):
    new_row = []
    for j in range(board_size):
        new_row.append(0)
    board.append(new_row)

# Edges of board wall. Odd numbered tiles also wall.
for i in range(board_size):
    for j in range(board_size):
        if i == 0 or j == 0 or i == board_size - 1 or j == board_size - 1:
            board[i][j] = 2
        elif i % 2 == 0 and j % 2 == 0:
            board[i][j] = 1
        else:
            board[i][j] = 0

# TEXT CONTAINER
text = "Player 1"

# INIT STUFF
pygame.init()
pygame.display.set_caption(f"Men of Bombs: Ghost Trick v{version}")
gamescreen = display.SpriteDisplay(board, colors, text, background, board_size, square_size)
gamescreen.initialize()
random.seed()

# CREATE ACTORS & VARIABLES
player_one = entities.Player([3, 3], board, 8)
player_two = entities.Player([7,7], board, 9)
players = [player_one, player_two]
step_counter = 10
clean_board = [x.copy() for x in board]
fruit_present = False
fruitx = 0
fruity = 0

# GAME LOOP
running = True
while running:
    timer_start = timeit.default_timer()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_one.change_velocity(1)
            if event.key == pygame.K_d:
                player_one.change_velocity(2)
            if event.key == pygame.K_s:
                player_one.change_velocity(3)
            if event.key == pygame.K_a:
                player_one.change_velocity(4)
            if event.key == pygame.K_e:
                player_one.place_bomb()
            if event.key == pygame.K_UP:
                player_two.change_velocity(1)
            if event.key == pygame.K_RIGHT:
                player_two.change_velocity(2)
            if event.key == pygame.K_DOWN:
                player_two.change_velocity(3)
            if event.key == pygame.K_LEFT:
                player_two.change_velocity(4)
            if event.key == pygame.K_l:
                player_two.place_bomb()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_one.change_velocity(0)
            if event.key == pygame.K_d:
                player_one.change_velocity(0)
            if event.key == pygame.K_s:
                player_one.change_velocity(0)
            if event.key == pygame.K_a:
                player_one.change_velocity(0)
            if event.key == pygame.K_UP:
                player_two.change_velocity(0)
            if event.key == pygame.K_RIGHT:
                player_two.change_velocity(0)
            if event.key == pygame.K_DOWN:
                player_two.change_velocity(0)
            if event.key == pygame.K_LEFT:
                player_two.change_velocity(0)

    if step_counter % 10 == 0:

        # Reset board to neutral state
        for row, clean_row in zip(board, clean_board):
            row[:] = clean_row

        # Resolve bomb men
        for player in players:

            # Movement
            player.move()

            # Bombs
            player.bomb_update()

        for player in players:
            board[player.pos[0]][player.pos[1]] = player.number

        for player in players:
            if player.bomb_placed:
                board[player.bombpos[0]][player.bombpos[1]] = 4
            if player.explosion:
                for pos in player.explosion_tiles:
                    board[pos[0]][pos[1]] = 5

        if fruit_present:
            if board[fruitx][fruity] == 5:  # Move fruit if it is exploded so players cant just permablock it by explosions
                fruitx, fruity = random_coords()
            board[fruitx][fruity] = 3

        for player in players:
            # Deaths, fruits & power
            x = players.copy()
            x.remove(player)
            if board[player.pos[0]][player.pos[1]] == 5: # Player caught in explosion
                player.downgrade()
                fruitx, fruity = random_coords()
                fruit_present = True
                for t in x:
                    t.upgrade()
            if player.number < 6:  # Player double killed
                running = False
            if player.pos[0] == fruitx and player.pos[1] == fruity and player.number < 8:  # Player reached ghostfruit
                player.upgrade()
                fruit_present = False
                for t in x:
                    t.downgrade()

        # Reset counter
        step_counter = 0

    # Render board
    gamescreen.update()

    # Wait for framerate & update counter
    timer_end = 0
    while timer_end - timer_start < 1/60:
        timer_end = timeit.default_timer()
    step_counter += 1