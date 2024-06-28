import pygame
from character import Character

class CharacterSheet:
    def __init__(self, player: Character, x, y) -> None:
        self.player = player
        
