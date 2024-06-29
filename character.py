import pygame, constants
from typing import Union

class Character:
    def __init__(self, name: str, character_class) -> None:
        self.name: str = name
        self.character_class = character_class
        self.level: int = 1
        self.experience = 0
        self.experience_cap = 100 * self.level
        # Base Stats
        self.strength: int = 10
        self.dexterity: int = 10
        self.intelligence: int = 10
        # Base Stats
        self.max_health: int = 10 * self.strength
        self.health = self.max_health
        self.attack_damage: int = 20
        # Statuses
        self.alive: bool = True
        self.hit: bool = False
        self.stunned: bool = False
        self.last_hit = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        

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

    def draw(self, surface) -> None: # TODO: Update to draw UI on screen
        # flipped_image = pygame.transform.flip(self.image, self.flip, False)
        # surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
        pass

    def level_up(self) -> None:
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack_damage += 5
        self.experience = 0
        self.experience_cap = 100 * self.level
        print(f"{self.name} has leveled up! Damage and Health have been increased.\n")
        # if self.level == 3:
        #     print("New ability unlocked: Kick (K to use)")