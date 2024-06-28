import pygame
from pygame import mixer
import constants
from functions import scale_img
from character import Character

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

animation_types = ["idle", "run"]
player_animations = []
for animation in animation_types:
    temp_list = []
    for i in range(4):
        img = pygame.image.load(f"assets/images/characters/elf/{animation}/{i}.png").convert_alpha()
        img = scale_img(img, constants.SCALE)
        temp_list.append(img)
    player_animations.append(temp_list)

# Create player
player = Character("Hero", x=200, y=200, health=100, player_animations=player_animations, size=1)

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

            if player.alive:

                # Update all objects
                player.update()
                
            # Draw objects on screen
            player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Take keyboard presses

        # Take keyboard releases

    pygame.display.update()
    
pygame.quit()