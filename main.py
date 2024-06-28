import pygame
from pygame import mixer
import constants

pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("My Game")

# Create clock for maintaining frame rate
clock = pygame.time.Clock()

# Game variables
level = 1
start_game = True # Set true to jump straight in
pause_game = False
start_intro = False
screen_scroll = [0, 0]

# Define player movement variables
moving_left = False
moving_right = False
moving_up = False
moving_down = False

# Text font
font = pygame.font.Font("assets/fonts/Atariclassic.ttf", 20)

# Main Game Loop
run = True
while run:

    # Control frame rate
    clock.tick(constants.FPS)

    if start_game == False:
        screen.fill(constants.MENU_BG)
    else:
        if pause_game == True:
            screen.fill(constants.MENU_BG)
        else:
            screen.fill(constants.BG)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Take keyboard presses

        # Take keyboard releases

    pygame.display.update()
    
pygame.quit()