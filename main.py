import pygame
from pygame import mixer
import csv
import constants
from functions import scale_img, draw_text, draw_info, reset_level
from character import Character
# from player_mob import PlayerMob
from damage_text import DamageText
from screen_fade import ScreenFade
from world import World
from button import Button
# from game_fonts import game_font

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
    animation_list = []
    for animation in animation_types:
        # Reset temporary list of images
        temp_list = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)
        animation_list.append(temp_list)
    mob_animations.append(animation_list)

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


world = World()
world.process_data(world_data, tile_list, item_images, player_animations, mob_animations, player)

# player_sprite = PlayerMob(player, x=constants.SCREEN_WIDTH // 2, y=constants.SCREEN_HEIGHT // 2, player_animations=player_animations, size=1)
player_sprite = world.player_mob

enemy_list = world.character_list

# Create sprite groups
damage_text_group = pygame.sprite.Group()
arrow_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

# score_coin = Item(constants.SCREEN_WIDTH - 115, 23, 0, coin_images, True)
# item_group.add(score_coin)

# Add items from the world data
# for item in world.item_list:
#     item_group.add(item)

# Create screen fades
intro_fade = ScreenFade(1, constants.BLACK, 4)
death_fade = ScreenFade(2, constants.PINK, 4)

# Create button
start_button = Button(constants.SCREEN_WIDTH // 2 - 145, constants.SCREEN_HEIGHT // 2 - 150, start_img)
exit_button = Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img)
restart_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 50, restart_img)
resume_button = Button(constants.SCREEN_WIDTH // 2 - 175, constants.SCREEN_HEIGHT // 2 - 150, resume_img)

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

            if character_sheet:
                player.show_character_sheet(screen)

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
                screen_scroll, level_complete = player_sprite.move(dx, dy, world.obstacle_tiles, world.exit_tile)

                # Update all objects
                world.update(screen_scroll)
                for enemy in enemy_list:
                    fireball = enemy.ai(player, player_sprite, world.obstacle_tiles, screen_scroll, fireball_image)
                    if fireball:
                        fireball_group.add(fireball)
                    if enemy.alive:
                        enemy.update()
                player.update()
                player_sprite.update(player)
                # arrow = bow.update(player)
                if arrow:
                    arrow_group.add(arrow)
                    shot_fx.play()
                for arrow in arrow_group:
                    damage, damage_pos = arrow.update(screen_scroll, world.obstacle_tiles, enemy_list)
                    if damage: 
                        damage_text = DamageText(damage_pos.centerx, damage_pos.y, str(damage), constants.RED)
                        damage_text_group.add(damage_text)
                        hit_fx.play()
                damage_text_group.update()
                fireball_group.update(screen_scroll, player)
                item_group.update(screen_scroll, player, coin_fx, heal_fx)

            # Draw objects on screen
            world.draw(screen)
            for enemy in enemy_list:
                enemy.draw(screen)
            player_sprite.draw(screen)
            # bow.draw(screen)
            for arrow in arrow_group:
                arrow.draw(screen)
            for fireball in fireball_group:
                fireball.draw(screen)
            damage_text_group.draw(screen)
            item_group.draw(screen)
            draw_info()
            # score_coin.draw(screen)

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
                if character_sheet:
                    character_sheet = False
                else: 
                    character_sheet = True
                print(f"Character Sheet: {character_sheet}")
            if event.key == pygame.K_i:
                if inventory:
                    inventory = False
                else: 
                    inventory = True
                print(f"Inventory: {inventory}")

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


    pygame.display.update()
    
pygame.quit()