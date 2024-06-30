import pygame
# import weapon
import constants
import math
from player_mob import PlayerMob

class Monster:
    def __init__(self, x: int, y: int, health, mob_animations, monster_type: int, boss: bool, size) -> None:
        self.monster_type: int = monster_type
        self.boss: bool = boss
        self.score: int = 0
        self.flip: bool = False
        self.animation_list = mob_animations[monster_type]
        self.frame_index: int = 0
        self.action: int = 0 # 0: Idle, 1: Run
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

    def move(self, dx: int, dy: int, obstacle_tiles, exit_tile = None) -> None:
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
            
        # Control facing direction
        if dx < 0:
            self.flip = True
        if dx > 0:
            self.flip = False

        # Control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) / 2)
            dy = dy * (math.sqrt(2) / 2)

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

    def ai(self, player, player_mob: PlayerMob, obstacle_tiles, screen_scroll, fireball_image):
        clipped_line = ()
        stun_cooldown = 100
        ai_dx = 0
        ai_dy = 0
        fireball = None
        # Reposition the mobs based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        # Create a line of sight from the enemy to the player
        line_of_sight = ((self.rect.centerx, self.rect.centery), (player_mob.rect.centerx, player_mob.rect.centery))
        # Check if line of sight passes through an obstacle tile
        for obstacle in obstacle_tiles:
            if obstacle[1].clipline(line_of_sight):
                clipped_line = obstacle[1].clipline(line_of_sight)
        # Check distance to player
        dist = math.sqrt(((self.rect.centerx - player_mob.rect.centerx) ** 2) + ((self.rect.centery - player_mob.rect.centery) ** 2))
        if not clipped_line and dist > constants.RANGE:
            if self.rect.centerx > player_mob.rect.centerx:
                ai_dx = -constants.ENEMY_SPEED
            if self.rect.centerx < player_mob.rect.centerx:
                ai_dx = constants.ENEMY_SPEED
            if self.rect.centery > player_mob.rect.centery:
                ai_dy = -constants.ENEMY_SPEED
            if self.rect.centery < player_mob.rect.centery:
                ai_dy = constants.ENEMY_SPEED
        
        if self.alive:
            if not self.stunned:
                # Move toward player
                self.move(ai_dx, ai_dy, obstacle_tiles)
                # Attack player
                if dist < constants.ATTACK_RANGE and player.hit == False:
                    player.health -= 10
                    player.hit = True
                    player.last_hit = pygame.time.get_ticks()
                # Boss enemies shoot fireballs
                fireball_cooldown = 700
                if self.boss:
                    if dist < 500:
                        if pygame.time.get_ticks() - self.last_attack >= fireball_cooldown:
                            # fireball = weapon.Fireball(fireball_image, self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                            self.last_attack = pygame.time.get_ticks()

            # Check if hit
            if self.hit == True:
                self.hit = False
                self.last_hit = pygame.time.get_ticks()
                self.stunned = True
                self.running = False
                self.update_action(0)

            if (pygame.time.get_ticks() - self.last_hit > stun_cooldown):
                self.stunned = False
        
        return fireball
    
    def update(self):
        # Check if character has died
        if self.health <= 0:
            self.health = 0
            self.alive = False

        # Check what action the player is performing
        if self.running == True:
            self.update_action(1) # 1: Run
        else: 
            self.update_action(0) # 0: Idle
        animation_cooldown = 70
        # Handle animation
        # Update image
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
    
    def draw(self, surface: pygame.Surface) -> None:
        flipped_image = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(flipped_image, self.rect)
