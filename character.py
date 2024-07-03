import pygame
from constants import BLACK, WHITE, GOLD, SHEET_LEFT_COL, SHEET_OFFSET, SCREEN_HEIGHT, SCREEN_WIDTH
from typing import Union
from functions import draw_text
from screen_fade import ScreenFade
# from game_fonts import large_sheet_font, small_sheet_font

class Character:
    def __init__(self, name: str, character_class: str) -> None:
        self.name: str = name
        self.character_class: str = character_class
        self.level: int = 1
        self.experience = 0
        # self.experience_cap = 100 * self.level
        self.experience_cap = 100
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
        leveled_up = False
        # Check if player has died
        if self.health <= 0:
            self.health = 0
            self.alive = False
        if self.experience >= self.experience_cap:
            leveled_up = True
            self.level_up()
            
        # Timer to reset player taking a hit 
        hit_cooldown = 100
        if self.hit == True and (pygame.time.get_ticks() - self.last_hit) > hit_cooldown:
            self.hit = False # TODO: Remove hit cooldown? attacks should be tied to attack speed
        return leveled_up

    def draw(self, surface) -> None: # TODO: Update to draw UI on screen
        # flipped_image = pygame.transform.flip(self.image, self.flip, False)
        # surface.blit(flipped_image, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET))
        pass

    def level_up(self) -> bool:
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack_damage += 5
        self.experience = 0
        # self.experience_cap = 100 * self.level
        self.experience_cap = 100
        print(f"{self.name} has leveled up! Damage and Health have been increased.\n")
        # if self.level == 3:
        #     print("New ability unlocked: Kick (K to use)")


    def show_character_sheet(self, surface) -> None:
        small_sheet_font = pygame.font.Font("assets/fonts/Atariclassic.ttf", 12)
        large_sheet_font = pygame.font.Font("assets/fonts/Atariclassic.ttf", 20)
        character_sheet = pygame.draw.rect(surface, BLACK, pygame.Rect(SHEET_OFFSET, SHEET_OFFSET, (SCREEN_WIDTH // 2) - 100, SCREEN_HEIGHT - (SHEET_OFFSET * 2)), width=0, border_radius=10)
        draw_text(f"{self.name}", large_sheet_font, WHITE, SHEET_LEFT_COL, SHEET_OFFSET + 20, surface)
        draw_text(f"Level: {self.level}", small_sheet_font, WHITE, SHEET_LEFT_COL, SHEET_OFFSET + 50, surface)
        draw_text(f"Health: {self.health}/{self.max_health}", small_sheet_font, WHITE, SHEET_LEFT_COL, SHEET_OFFSET + 65, surface)
        draw_text(f"Experience: {self.experience}/{self.experience_cap}", small_sheet_font, WHITE, SHEET_LEFT_COL, SHEET_OFFSET + 80, surface)
        draw_text(f"Strength: {self.strength}", small_sheet_font, WHITE, SHEET_LEFT_COL, SHEET_OFFSET + 110, surface)
        draw_text(f"Dexterity: {self.dexterity}", small_sheet_font, WHITE, SHEET_LEFT_COL, SHEET_OFFSET + 125, surface)
        draw_text(f"Intelligence: {self.intelligence}", small_sheet_font, WHITE, SHEET_LEFT_COL, SHEET_OFFSET + 140, surface)
