# from items import Item
# from character import Character
from player_mob import PlayerMob
from monster import Monster
import constants

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.player_mob = None
        self.character_list = []

    def process_data(self, data, tile_list, item_images, player_animations, mob_animations, player):
        self.level_length = len(data)
        # Iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                # Wall Tiles
                if tile == 7:
                    self.obstacle_tiles.append(tile_data)
                # Exit Tiles
                elif tile == 8:
                    self.exit_tile = tile_data
                # Coin Tiles
                elif tile == 9:
                    # coin = Item(image_x, image_y, 0, item_images[0])
                    # self.item_list.append(coin)
                    tile_data[0] = tile_list[0] # Replace tile image with plain floor tile
                elif tile == 10:
                    # potion = Item(image_x, image_y, 1, [item_images[1]])
                    # self.item_list.append(potion)
                    tile_data[0] = tile_list[0] # Replace tile image with plain floor tile
                elif tile == 11:
                    player_mob = PlayerMob(player, image_x, image_y, player_animations, 1)
                    # player_sprite = PlayerMob(player, x=constants.SCREEN_WIDTH // 2, y=constants.SCREEN_HEIGHT // 2, player_animations=player_animations, size=1)
                    self.player_mob = player_mob
                    tile_data[0] = tile_list[0] # Replace tile image with plain floor tile
                elif tile >= 12 and tile <= 16:
                    enemy = Monster(image_x, image_y, 100, mob_animations, tile - 11, False, 1)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0] # Replace tile image with plain floor tile
                elif tile == 17:
                    enemy = Monster(image_x, image_y, 100, mob_animations, 6, True, 2)
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]

                # Add image data to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])
            # tile_data = [image, image_rect, image_x, image_y]

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])