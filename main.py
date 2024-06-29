import pygame
from pygame import mixer
import csv
import constants
from functions import scale_img, draw_text, draw_info, reset_level
from character import Character
from player_mob import PlayerMob
from damage_text import DamageText
from screen_fade import ScreenFade
from world import World

mixer.init()
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

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
hit_fx.set_volume(0.5)
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)
heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(0.5)

# Load button images
start_img = scale_img(pygame.image.load("assets/images/buttons/button_start.png").convert_alpha(), constants.BUTTON_SCALE)
exit_img = scale_img(pygame.image.load("assets/images/buttons/button_exit.png").convert_alpha(), constants.BUTTON_SCALE)
restart_img = scale_img(pygame.image.load("assets/images/buttons/button_restart.png").convert_alpha(), constants.BUTTON_SCALE)
resume_img = scale_img(pygame.image.load("assets/images/buttons/button_resume.png").convert_alpha(), constants.BUTTON_SCALE)

# Load heart images 
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.ITEM_SCALE)
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.ITEM_SCALE)
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.ITEM_SCALE)

# Load coin images
coin_images = []
for x in range(4):
    img = scale_img(pygame.image.load(f"assets/images/items/coin_f{x}.png").convert_alpha(), constants.ITEM_SCALE)
    coin_images.append(img)
    
# Load potion images
red_potion = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(), constants.POTION_SCALE)

item_images = []
item_images.append(coin_images)
item_images.append(red_potion)

# Load weapon images
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE)
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE)
fireball_image = scale_img(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), constants.FIREBALL_SCALE)

# Load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_list.append(tile_image)

# Compile animations
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

# Create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLUMNS
    world_data.append(r)

# Load in level data and create world
with open(f"levels/level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)



# Create player
player = Character("Hero", character_class=0)
# TODO: create character class selector
player_sprite = PlayerMob(player, x=constants.SCREEN_WIDTH // 2, y=constants.SCREEN_HEIGHT // 2, player_animations=player_animations, size=1)

world = World()
world.process_data(world_data, tile_list, item_images, player_animations, mob_animations, player)

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
                screen_scroll = player_sprite.move(dx, dy)

                # Update all objects
                player_sprite.update()

            # Draw objects on screen
            player_sprite.draw(screen)

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