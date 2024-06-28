# import random
import sys
# from dataclasses import dataclass
import pygame
import obsolete_button
# from classes import person, enemy, inventoryItem
# from functions import create_hero, create_enemy, fight, battle

# name / base_health / base_attack_damage / base_experience_bounty
monster_types: list[str, int]= [("Goblin", 30, 5, 10), 
                                ("Harpy", 25, 8, 10), 
                                ("Orc", 45, 10, 15),
                                ("Dragon", 80, 30, 80),
                                ("Frog", 10, 2, 2),
                                ("Zombie", 30, 10, 15)]

character_classes: list[str] = ["Knight", "Wizard", "Ranger"]

def main():
    pygame.init()

    # Create the game window
    screen_width = 1200
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Main Menu")

    # Game variables
    game_paused = False
    menu_state = "main"


    # Define fonts
    text_font = pygame.font.SysFont("arialblack", 40)

    # Define colors
    TEXT_COL = (255, 255, 255)

    # Load button images
    resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
    options_img = pygame.image.load("images/button_options.png").convert_alpha()
    quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
    video_img = pygame.image.load('images/button_video.png').convert_alpha()
    audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
    keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
    back_img = pygame.image.load('images/button_back.png').convert_alpha()

    # Create button instances
    resume_button = obsolete_button.Button(304, 125, resume_img, 1)
    options_button = obsolete_button.Button(297, 250, options_img, 1)
    quit_button = obsolete_button.Button(336, 375, quit_img, 1)
    video_button = obsolete_button.Button(226, 75, video_img, 1)
    audio_button = obsolete_button.Button(225, 200, audio_img, 1)
    keys_button = obsolete_button.Button(246, 325, keys_img, 1)
    back_button = obsolete_button.Button(332, 450, back_img, 1)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
    # player = pygame.Rect((300, 250, 50, 50))


    run = True
    while run:

        screen.fill((52, 78, 91))
        
        # Check if game is paused
        if game_paused == True:
            # Check menu state
            if menu_state == "main":
                # Draw pause menu buttons
                if resume_button.draw(screen):
                    game_paused = False
                if options_button.draw(screen):
                    menu_state = "options"
                if quit_button.draw(screen):
                    run = False
            if menu_state == "options":
                if video_button.draw(screen):
                    print("Video Settings")
                if audio_button.draw(screen):
                    print("Audio Settings")
                if keys_button.draw(screen):
                    print("Change Key Bindings")
                if back_button.draw(screen):
                    menu_state = "main"
        else:
            draw_text("Press SPACE to pause", font=text_font, text_col=TEXT_COL, x=160, y=250)


        #need clock
        # pygame.draw.rect(screen, (255, 0, 0), player)

        # key = pygame.key.get_pressed()
        # if key[pygame.K_a] == True:
        #     player.move_ip(-1, 0)
        # elif key[pygame.K_d] == True:
        #     player.move_ip(1, 0)
        # elif key[pygame.K_w] == True:
        #     player.move_ip(0, -1)
        # elif key[pygame.K_s] == True:
        #     player.move_ip(0, 1)

        # EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_paused = True
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    # input_name: str = input("\nWhat is your name? ").title()
    # input_class: str = input(f"What is your job: {character_classes[0]}, {character_classes[1]}, or {character_classes[2]}? ").strip().lower()
    # player1: person = create_hero(input_name, input_class)
    # print("\n===== A NEW HERO HAS ARRIVED! ===== \n")
    # print(f"Welcome to Evendale, {player1.name} the {player1.character_class}.\n")

    # while True: 
    #     user_input = input("What would you like to do:\n(F) Fight\n(E) Exit\n\nInput: ").lower()
    #     print()
    #     match user_input:
    #         case "e": 
    #             sys.exit()
    #         case "f":
    #             new_enemy = create_enemy(monster_types)
    #             battle(player1, new_enemy)

    pygame.quit()

if __name__ == "__main__":
    main()