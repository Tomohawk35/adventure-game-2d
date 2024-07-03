import pygame
import constants

# Screen fade class
class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
    
    def fade(self, screen):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: # Whole Screen Fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, constants.SCREEN_HEIGHT // 2 + self.fade_counter, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
        elif self.direction == 2: # Vertical Screen Fade Down
            pygame.draw.rect(screen, self.color, (0, 0, constants.SCREEN_WIDTH, 0 + self.fade_counter))
        
        if self.fade_counter >= (constants.SCREEN_WIDTH // 2):
            fade_complete = True

        return fade_complete