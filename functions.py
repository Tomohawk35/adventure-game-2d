import pygame
import constants

# Helper function to scale image
def scale_img(image: pygame.Surface, scale: int):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# Function for outputting text onto the screen
def draw_text(text, font, text_col, x, y, screen):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function for displaying game info
def draw_info(screen, player, heart_full, heart_half, heart_empty, font, level):
    pygame.draw.rect(screen, constants.PANEL, (0, 0, constants.SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (constants.SCREEN_WIDTH, 50))
    # Draw lives
    half_heart_drawn = False
    for i in range(5):
        if player.health >= ((i + 1) * 20):
            screen.blit(heart_full, (10 + i * 50, 0))
        elif (player.health % 20 > 0) and half_heart_drawn == False:
            screen.blit(heart_half, (10 + i * 50, 0))
            half_heart_drawn = True
        else:
            screen.blit(heart_empty, (10 + i * 50, 0))
    # Level
    draw_text(f"LEVEL: {level}", font, constants.WHITE, constants.SCREEN_WIDTH / 2, 15)
    # Show score
    draw_text(f"X{player.score}", font, constants.WHITE, constants.SCREEN_WIDTH - 100, 15)

# Function to reset level
def reset_level(damage_text_group, arrow_group, item_group, fireball_group):
    damage_text_group.empty()
    arrow_group.empty()
    item_group.empty()
    fireball_group.empty()

    # Create empty tile list
    data = []
    for row in range(constants.ROWS):
        r = [-1] * constants.COLUMNS
        data.append(r)

    return data