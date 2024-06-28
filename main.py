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
character_sheet = False
inventory = False
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

mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"]
mob_animations = []
for mob in mob_types:
    temp_list = []
    for i in range(4):
        img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
        img = scale_img(img, constants.SCALE)
        temp_list.append(img)
    mob_animations.append(temp_list)

# Create player
player = Character("Hero", x=constants.SCREEN_WIDTH // 2, y=constants.SCREEN_HEIGHT // 2, health=100, player_animations=player_animations, size=1)

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

                # Calculate player movement
                dx = 0
                dy = 0

                if moving_right == True:
                    dx = constants.SPEED
                if moving_left == True:
                    dx = -constants.SPEED
                if moving_down == True:
                    dy = constants.SPEED
                if moving_up == True:
                    dy = -constants.SPEED
                
                # Move player
                screen_scroll = player.move(dx, dy)

                # Update all objects
                player.update()

            # Draw objects on screen
            player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                pause_game = True
            if event.key == pygame.K_c:
                character_sheet = True
            if event.key == pygame.K_i:
                inventory = True

        # Take keyboard releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_c:
                character_sheet = False
            if event.key == pygame.K_i:
                inventory = False

    pygame.display.update()
    
pygame.quit()