from dataclasses import dataclass
import random

@dataclass
class person:
    name: str
    character_class: str
    level: int = 1
    max_health: int = 50
    health: int = max_health
    attack_damage: int = 20
    experience: int = 0
    experience_cap: int = 100 * level
    potion_count: int = 3
    inventory = []
    # attack_choices: list[str, str] = [("A": "Attack"), ("P": "Use Potion")]

    def attack(self) -> int:
        return self.attack_damage + random.randint(-10, 10)
    
    def take_damage(self, damage) -> None:
        self.health -= damage
    
    def kick(self) -> int:
        if self.level >= 3:
            return self.attack_damage + random.randint(-5, 5) + 5
        else:
            print("Careful! You aren't strong enough for that yet.")
        
    def use_potion(self) -> None:
        if self.potion_count >= 1:
            self.potion_count -= 1
            self.health += 20 # TODO: make it so you can't go above max health
            print(f"You used a potion. You have {self.potion_count} potions left.")
            print(f"You are now at {self.health} health points.")
        else:
            print("You are out of potions.")

    def display_info(self) -> None:
        print(f"===== PLAYER INFO =====\nHP: {self.health}/{self.max_health} // LEVEL: {self.level} // POTIONS AVAILABLE: {self.potion_count} // PLAYER EXP: {self.experience}\n")

    def level_up(self) -> None:
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack_damage += 5
        self.experience = 0
        self.experience_cap = 100 * self.level
        print(f"{self.name} has leveled up! Damage and Health have been increased.\n")
        if self.level == 3:
            print("New ability unlocked: Kick (K to use)")

@dataclass
class enemy:
    name: str
    level: int = 1
    base_health: int = 50
    max_health: int = base_health + (20 * (level - 1))
    health: int = max_health
    base_attack_damage: int = 10
    attack_damage: int = base_attack_damage + (5 * (level - 1))
    base_experience_bounty: int = 50
    experience_bounty: int = base_experience_bounty * level

    def attack(self) -> int:
        return self.attack_damage + random.randint(-10, 10)
    
    def take_damage(self, damage) -> None:
        self.health -= damage

    def display_info(self) -> None:
        print(f"===== {self.name.upper()} INFO =====\nHP: {self.health}/{self.max_health} // LEVEL: {self.level}\n")


@dataclass
class inventoryItem:
    name: str
    health_boost: int
    attack_boost: int
    equipped_status: bool = False