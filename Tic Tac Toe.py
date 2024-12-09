import pygame, sys
from pygame.locals import *
import random, time
import asyncio

pygame.init()

# SET UP
width = 700
height = 600

clock = pygame.time.Clock()

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("O's and X's")

# LOAD IMAGES
x = pygame.image.load('assets/x.png')
o = pygame.image.load('assets/o.png')

heading = pygame.image.load('assets/heading.png')

# Restart button assets
restart = pygame.image.load("assets/restart.png")
restart_rect = pygame.Rect(width-100, 150, 60, 60)

# Player icon assets
player_1 = pygame.image.load("assets/player-1.png")
player_2 = pygame.image.load("assets/player-2.png")

player_1_disable = pygame.image.load("assets/player-1-disabled.png")
player_2_disable = pygame.image.load("assets/player-2-disable.png")

player_1_win = [pygame.image.load("assets/player-1-win-1.png"),
                pygame.image.load("assets/player-1-win-2.png"),
                pygame.image.load("assets/player-1-win-3.png"),
                pygame.image.load("assets/player-1-win-4.png")]

player_2_win = [pygame.image.load("assets/player-2-win-1.png"),
                pygame.image.load("assets/player-2-win-2.png"),
                pygame.image.load("assets/player-2-win-3.png"),
                pygame.image.load("assets/player-2-win-4.png")]

player_1_coords = (20,height-140)
player_2_coords = (width-140,height-140)

player_1_rect = pygame.Rect(20, height-140, 120, 120)
player_2_rect = pygame.Rect(width-140, height-140, 120, 120)

# Board assets
board_img = pygame.image.load("assets/board.png")

blocks = [pygame.Rect(170,150,120,120),
    pygame.Rect(290,150,120,120),
    pygame.Rect(410,150,120,120),
    pygame.Rect(170,270,120,120),
    pygame.Rect(290,270,120,120),
    pygame.Rect(410,270,120,120),
    pygame.Rect(170,390,120,120),
    pygame.Rect(290,390,120,120),
    pygame.Rect(410,390,120,120)]

# Sound effects
thuds = [pygame.mixer.Sound("audio/thud1.wav"),
        pygame.mixer.Sound("audio/thud2.wav"),
        pygame.mixer.Sound("audio/thud3.wav")]

win_audio = pygame.mixer.Sound("audio/win_audio.wav")
draw_audio = pygame.mixer.Sound("audio/draw.wav")
restart_audio = pygame.mixer.Sound("audio/restart.wav")

for thud in thuds:
    thud.set_volume(0.3)

win_audio.set_volume(0.3)
restart_audio.set_volume(0.3)
draw_audio.set_volume(0.3)

def resetGame():
    global draw, board, run, game_finished

    screen.fill((255,255,255))

    screen.blit(board_img, (0,150))

    screen.blit(heading, (0,0))

    draw = 'o'
    screen.blit(restart, (width-100, 150))

    screen.blit(player_1, player_1_coords)
    screen.blit(player_2_disable, player_2_coords)

    run = True
    game_finished = False

    board =[[0,0,0],
            [0,0,0],
            [0,0,0]]

def check_win(player):
    global board

    win = [player, player, player]

    # check rows
    for row in board:
        if row == win:
            return True
    
    # check columns
    for column in range(3):
        if [board[0][column], board[1][column], board[2][column]] == win:
            return True
        
    if [board[0][0], board[1][1], board[2][2]] == win:
        return True
    
    if [board[0][2], board[1][1], board[2][0]] == win:
        return True
    
    return False

def check_game_over():
    for row in board:
        if 0 in row:
            return False
    return True

def check_draw():
    if not check_win("x") and not check_win("o") and check_game_over():
        return True
    return False

resetGame()

async def main():
    global run, game_finished, draw

    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                run = False

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                    
                if restart_rect.collidepoint(mouse_pos):
                    pygame.mixer.Sound.play(restart_audio)
                    time.sleep(0.2)
                    resetGame()
                    
                if not game_finished:
                    for block in blocks:
                        # if the user clicks on a block, check if the block is open
                        if block.collidepoint(mouse_pos) and board[blocks.index(block)//3][blocks.index(block) - 3*(blocks.index(block)//3)] == 0:
                            # set the value of the block to the symbol being played
                            board[blocks.index(block)//3][blocks.index(block) - 3*(blocks.index(block)//3)] = draw

                            # draw the symbol on the screen
                            if draw == 'x':
                                screen.blit(x, (block.x, block.y))
                                draw = 'o'
                                screen.blit(player_1, player_1_coords)
                                screen.blit(player_2_disable, player_2_coords)
                            else:
                                screen.blit(o, (block.x, block.y))
                                draw = 'x'

                                screen.blit(player_1_disable, player_1_coords)
                                screen.blit(player_2, player_2_coords)

                            # play a random sound effect
                            pygame.mixer.Sound.play(random.choice(thuds))

        if check_draw():
            if not game_finished:
                pygame.mixer.Sound.play(draw_audio)

            game_finished = True

            screen.blit(player_1_disable, player_1_coords)
            screen.blit(player_2_disable, player_2_coords)

        elif check_win('x'):        
            if not game_finished:
                pygame.mixer.Sound.play(win_audio)
                index = 0
                last = pygame.time.get_ticks()

            if index == 4:
                index = 0

            game_finished = True

            screen.blit(player_1_disable, player_1_coords)
            screen.blit(player_2_win[index], player_2_coords)

            if pygame.time.get_ticks() - last >= 100:
                index += 1
                last = pygame.time.get_ticks()

        elif check_win('o'):
            if not game_finished:
                pygame.mixer.Sound.play(win_audio)
                index = 0
                last = pygame.time.get_ticks()

            if index == 4:
                index = 0

            game_finished = True

            screen.blit(player_1_win[index], player_1_coords)
            screen.blit(player_2_disable, player_2_coords)

            if pygame.time.get_ticks() - last >= 100:
                index += 1
                last = pygame.time.get_ticks()
        
        pygame.display.update()

asyncio.run(main())