import pygame

# Damage text class
class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color, font):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self, screen_scroll):
        # Reposition based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Move damage text up
        self.rect.y -= 1
        # Delete text after a few seconds
        self.counter += 1
        if self.counter > 30:
            self.kill()