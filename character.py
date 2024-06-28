import pygame, constants
from typing import Union

class Character:
    def __init__(self, name: str, x: int, y: int, health: int, player_animations, size) -> None:
        self.name: str = name
        self.level: int = 1
        self.flip: bool = False
        self.animation_list = player_animations
        self.frame_index: int = 0
        self.action: int = 0 # 0: Idle, 1: Run, 2: Attack
        self.update_time = pygame.time.get_ticks()
        self.running: bool = False
        self.health: int = health
        self.alive: bool = True
        self.hit: bool = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.stunned: bool = False

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)
    
    def move(self, dx: int, dy: int) -> list[int]:
        screen_scroll = [0, 0]
        # Check if moving
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
        
        # Control facing direction
        if dx < 0: 
            self.flip = True
        if dx > 0:
            self.flip = False

        # Check for collision with map in x direction
        self.rect.x += dx
        # for obstacle in obstacle_tiles:
        #     # Check for collisions
        #     if obstacle[1].colliderect(self.rect):
        #         # Check which side the collision is from
        #         if dx > 0:
        #             self.rect.right = obstacle[1].left
        #         if dx < 0:
        #             self.rect.left = obstacle[1].right
        self.rect.y += dy
        # for obstacle in obstacle_tiles:
        #     # Check for collisions
        #     if obstacle[1].colliderect(self.rect):
        #         # Check which side the collision is from
        #         if dy > 0:
        #             self.rect.bottom = obstacle[1].top
        #         if dy < 0:
        #             self.rect.top = obstacle[1].bottom

        # Update scroll based on player position
        # Move camera left and right
        if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
            screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
            self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
        if self.rect.left < (constants.SCROLL_THRESH):
            screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
            self.rect.left = constants.SCROLL_THRESH
        # Move camera up and down
        if self.rect.bottom > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
            screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.bottom
            self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
        if self.rect.top < (constants.SCROLL_THRESH):
            screen_scroll[1] = constants.SCROLL_THRESH - self.rect.top
            self.rect.top = constants.SCROLL_THRESH
        
        return screen_scroll

    def update(self):
        # Check if player has died
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        # Timer to reset player taking a hit
        hit_cooldown = 100
        if self.hit == True and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
            self.hit = False

        # Check what action the player is performing
        if self.running == True:
            self.update_action(1) # 1: Run
        else:
            self.update_action(0) # 0: Idle
        
        animation_cooldown = 70
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        
        # Check if animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        # Check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # Update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface) -> None:
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))