import pygame, constants, math
from typing import Union
from character import Character

class PlayerMob:
    def __init__(self, player: Character, x: int, y: int, player_animations, size) -> None:
        self.player: Character = player
        self.flip: bool = False
        self.animation_list = player_animations
        self.frame_index: int = 0
        self.action: int = 0 # 0: Idle, 1: Run, 2: Attack
        self.update_time = pygame.time.get_ticks()
        self.running: bool = False
        # self.alive: bool = True
        # self.hit: bool = False
        # self.last_hit = pygame.time.get_ticks()
        # self.last_attack = pygame.time.get_ticks()
        # self.stunned: bool = False

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, constants.TILE_SIZE * size, constants.TILE_SIZE * size)
        self.rect.center = (x, y)
    
    def move(self, dx: int, dy: int, obstacle_tiles, exit_tile = None) -> list[int]:
        screen_scroll = [0, 0]
        level_complete = False
        # Check if moving
        self.running = False
        if dx != 0 or dy != 0:
            self.player.running = True
        
        # Control facing direction
        if dx < 0: 
            self.flip = True
        if dx > 0:
            self.flip = False

        # Check for collision with map in x direction
        self.rect.x += dx
        for obstacle in obstacle_tiles:
            # Check for collisions
            if obstacle[1].colliderect(self.rect):
                # Check which side the collision is from
                if dx > 0:
                    self.rect.right = obstacle[1].left
                if dx < 0:
                    self.rect.left = obstacle[1].right
        self.rect.y += dy
        for obstacle in obstacle_tiles:
            # Check for collisions
            if obstacle[1].colliderect(self.rect):
                # Check which side the collision is from
                if dy > 0:
                    self.rect.bottom = obstacle[1].top
                if dy < 0:
                    self.rect.top = obstacle[1].bottom

        # Check collision with exit ladder
        if exit_tile[1].colliderect(self.rect):
            # Ensure player is close to the center of the exit ladder
            exit_dist = math.sqrt(((self.rect.centerx - exit_tile[1].centerx) ** 2) + ((self.rect.centery - exit_tile[1].centery) ** 2))
            if exit_dist < 20:
                level_complete = True

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
        
        return screen_scroll, level_complete

    def update(self, player):

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