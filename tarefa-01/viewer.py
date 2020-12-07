import pygame
import sys
import time
import main
import numpy as np

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

screen = pygame.display.set_mode(size)

medium_font = pygame.font.Font("OpenSans-Regular.ttf", 28)
move_font = pygame.font.Font("OpenSans-Regular.ttf", 60)

state = main.get_initial_state()
path = None
solved = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(black)

    # Show title
    if path == None:
        title = "Searching for solution using A*"
    elif solved:
        title = f"Puzzle Solved"
    elif action == None:
        title = f"Solved in {len(path) - 1} Moves! Press to show path"
    else:
        title = f"Move '{action}', press for next move"

    title = medium_font.render(title, True, white)
    titleRect = title.get_rect()
    titleRect.center = ((width / 2), 30)
    screen.blit(title, titleRect)

    # Draw game board
    tile_size = 80
    tile_origin = (width / 2 - (1.5 * tile_size),
                   height / 2 - (1.5 * tile_size))
    tiles = []

    board = np.reshape(state, (3, 3))
    for i in range(3):
        row = []
        for j in range(3):
            rect = pygame.Rect(
                tile_origin[0] + j * tile_size,
                tile_origin[1] + i * tile_size,
                tile_size, tile_size
            )
            pygame.draw.rect(screen, white, rect, 3)

            move = move_font.render(
                " " if board[i][j] == 0 else str(board[i][j]), True, white)
            moveRect = move.get_rect()
            moveRect.center = rect.center
            screen.blit(move, moveRect)
            row.append(rect)
        tiles.append(row)

    # Check for a user move
    click, _, _ = pygame.mouse.get_pressed()
    if click == 1:
        if len(path):
            state, action = path.pop(0)
        else:
            solved = True
        time.sleep(0.2)

    pygame.display.flip()

    if path == None:
        search_time = time.perf_counter()
        path = main.search_a_star(state)
        search_time = time.perf_counter() - search_time
        print("Search Time (s)", search_time)
        state, action = path.pop(0)
