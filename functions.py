import sys
import random
from classes import person, enemy, inventoryItem

def create_hero(input_name: str, input_class: str):
    return person(name=input_name, character_class=input_class.title())

def create_enemy(monsters: list[tuple[str, int, int, int]]) -> enemy:
    random_monster = random.choice(monsters)
    new_enemy = enemy(name = random_monster[0], base_health = random_monster[1], base_attack_damage = random_monster[2], base_experience_bounty = random_monster[3])
    return new_enemy

# def take_item(item_user: person, item: inventoryItem):
#     item_user.inventory.append(item)

# def use_item(item_user: person, item: inventoryItem) -> None:
#     item_user.health += item.health_boost
#     item_user.attack_damage += item.attack_boost

# def equip_item(item_user: person, item: inventoryItem):
#     if item.equipped_status: 
#         print(f"{item.name} is already equipped.")
#     else:
#         item.equipped_status = True
#         item_user.health += item.health_boost
#         item_user.attack_damage += item.attack_boost

# def unequip_item(item_user: person, item: inventoryItem):
#     if item.equipped_status: 
#         item.equipped_status = True
#         item_user.health -= item.health_boost
#         item_user.attack_damage -= item.attack_boost
#     else:
#         print(f"{item.name} is not equipped.")

# def select_item(item_user: person, item: inventoryItem):
#     pass

def fight(player_damage: int, player: person, enemy: enemy) -> None:
    enemy.take_damage(player_damage)
    print(f"You hit {enemy.name} and dealt {player_damage} damage! \nENEMY HP: {enemy.health}/{enemy.max_health}\n")
    enemy_damage = enemy.attack()
    player.take_damage(enemy_damage)
    print(f"{enemy.name} hit you and dealt {enemy_damage} damage! \nPLAYER HP: {player.health}/{player.max_health}\n")

# TODO: Need to exit fight monster is killed before they can attack
def battle(player: person, enemy: enemy):
    print("===== BATTLE START =====\n")
    print(f"A {enemy.name} has appeared!\n")
    enemy.display_info()
    while player.health >= 0 and enemy.health >= 0:
        print(f"PLAYER HP: {player.health}/{player.max_health} // {enemy.name} HP: {enemy.health}/{enemy.max_health}\n")
        action_choice = input("Choose your action:\n(A) Attack\n(K) Kick\n(P) Use Potion\n(I) View Player Info\n(E) Exit\n\nInput: ").lower()
        print()
        match action_choice:
            case "a":
                player_damage = player.attack()
                fight(player_damage, player, enemy)
            case "k":
                if player.level >= 3:
                    player_damage = player.kick()
                    fight(player_damage, player, enemy)
                else:
                    print("Careful! You aren't strong enough for that yet.")
            case "p":
                player.use_potion()
            case "i":
                player.display_info()
            case "e":
                sys.exit()
        print("   ///////////////////////////////////////////////////////////////\n")

    if enemy.health <= 0:
        print(f"You've slain the enemy {enemy.name}! Well done!\n")
        player.experience += enemy.experience_bounty
        if player.experience >= player.experience_cap:
            player.level_up()

    elif player.health <= 0:
        print("You fought valiantly but were defeated! \n\n ====== GAME OVER ======")
        sys.exit()
