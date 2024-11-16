import pygame
import math

class Map:
    def __init__(self, tilesheet, base_tile_size, scaled_tile_size, map_array):
        self.tilesheet = tilesheet
        self.base_tile_size = base_tile_size  # Original tile size in the tilesheet
        self.scaled_tile_size = scaled_tile_size  # Desired tile size in the game
        self.tiles = {}
        self.map_array = map_array  # Store the map array in the Map object
        self.tile_metadata = {
            '0': {
                'position': (96, 2242),       # Position of the grass tile in the tilesheet
                'size': (32, 32),             # Size of the grass tile
                'anchor': 'top-left',         # Anchor point for grass
                'z_index': 0,                 # Z-index for grass (lower than tree)
                'collidable': False           # Whether the tile is collidable
            },
            'x': {
                'position': (14, 19),         # Position of the tree tile in the tilesheet
                'size': (36, 45),             # Size of the tree tile
                'anchor': 'bottom-center',    # Anchor point for tree
                'z_index': 2,                 # Z-index for tree (higher than grass)
                'collidable': True            # Tree tiles are collidable
            },
            # Add more tiles as needed
        }
        self.collision_rects = []  # List to store collision rectangles
        self.load_tiles()
        self.build_collision_rects()  # Build collision rectangles instead of collision map

    def load_tiles(self):
        sheet = pygame.image.load(self.tilesheet).convert_alpha()
        # Calculate scale factor
        scale_factor = self.scaled_tile_size / self.base_tile_size
        for key, data in self.tile_metadata.items():
            x, y = data['position']
            width, height = data['size']
            rect = pygame.Rect(x, y, width, height)
            tile = sheet.subsurface(rect)
            # Scale the tile to the desired size
            scaled_width = int(width * scale_factor)
            scaled_height = int(height * scale_factor)
            tile = pygame.transform.scale(tile, (scaled_width, scaled_height))
            self.tiles[key] = tile

    def print_collision_map(self):
        print("Collision Map:")
        for row in self.collision_map:
            line = ""
            for cell in row:
                if cell:
                    line += "X"  # Collidable
                else:
                    line += "."  # Non-collidable
            print(line)

    def build_collision_rects(self):
        for y, row in enumerate(self.map_array):
            for x, tile_keys in enumerate(row):
                if not isinstance(tile_keys, list):
                    tile_keys = [tile_keys]
                for tile_key in tile_keys:
                    if tile_key in self.tile_metadata and self.tile_metadata[tile_key]['collidable']:
                        data = self.tile_metadata[tile_key]
                        # Calculate scaled tile size
                        scale_factor = self.scaled_tile_size / self.base_tile_size
                        tile_width = data['size'][0] * scale_factor
                        tile_height = data['size'][1] * scale_factor
                        anchor = data.get('anchor', 'top-left')
                        base_x = x * self.scaled_tile_size
                        base_y = y * self.scaled_tile_size

                        # Adjust position based on anchor
                        if anchor == 'top-left':
                            collision_x = base_x
                            collision_y = base_y
                        elif anchor == 'bottom-center':
                            collision_x = base_x + (self.scaled_tile_size // 2) - (tile_width // 2)
                            collision_y = base_y + self.scaled_tile_size - tile_height
                        else:
                            collision_x = base_x
                            collision_y = base_y

                        collision_rect = pygame.Rect(collision_x, collision_y, tile_width, tile_height)
                        self.collision_rects.append(collision_rect)

    def build_collision_map(self):
        for y, row in enumerate(self.map_array):
            for x, tile_keys in enumerate(row):
                if not isinstance(tile_keys, list):
                    tile_keys = [tile_keys]
                for tile_key in tile_keys:
                    if tile_key in self.tile_metadata and self.tile_metadata[tile_key]['collidable']:
                        data = self.tile_metadata[tile_key]

                        # Calculate tile dimensions in grid units, rounding up to ensure full coverage
                        width_in_tiles = math.ceil(data['size'][0] / self.base_tile_size)
                        height_in_tiles = math.ceil(data['size'][1] / self.base_tile_size)

                        anchor = data.get('anchor', 'top-left')

                        if anchor == 'top-left':
                            leftmost_x = x
                            topmost_y = y
                        elif anchor == 'bottom-center':
                            leftmost_x = x - (width_in_tiles // 2)
                            topmost_y = y - (height_in_tiles - 1)
                        else:
                            leftmost_x = x
                            topmost_y = y

                        for dy in range(height_in_tiles):
                            for dx in range(width_in_tiles):
                                tx = leftmost_x + dx
                                ty = topmost_y + dy

                                # Only set the collision if within bounds
                                if 0 <= ty < len(self.collision_map) and 0 <= tx < len(self.collision_map[0]):
                                    self.collision_map[ty][tx] = True


    def is_collidable(self, player_rect):
        for collision_rect in self.collision_rects:
            if player_rect.colliderect(collision_rect):
                return True
        return False


    def draw_layer(self, surface, layer_type, camera_offset=(0,0)):
        camera_x, camera_y = camera_offset
        for y, row in enumerate(self.map_array):
            for x, tile_keys in enumerate(row):
                if not isinstance(tile_keys, list):
                    tile_keys = [tile_keys]
                for tile_key in tile_keys:
                    if tile_key in self.tiles:
                        z_index = self.tile_metadata[tile_key].get('z_index', 0)

                        # Determine if we should draw based on layer type
                        if (layer_type == 'base' and z_index == 0) or (layer_type == 'overlay' and z_index > 0):
                            tile = self.tiles[tile_key]
                            tile_width, tile_height = tile.get_size()

                            # Calculate the base position in world coordinates
                            base_x = x * self.scaled_tile_size
                            base_y = y * self.scaled_tile_size

                            # Adjust for anchor
                            anchor = self.tile_metadata[tile_key].get('anchor', 'top-left')
                            if anchor == 'bottom-center':
                                draw_x = base_x + (self.scaled_tile_size // 2) - (tile_width // 2) - camera_x
                                draw_y = base_y + self.scaled_tile_size - tile_height - camera_y
                            else:  # 'top-left' anchor
                                draw_x = base_x - camera_x
                                draw_y = base_y - camera_y

                            # Draw the tile on the surface
                            surface.blit(tile, (draw_x, draw_y))

    def draw_dynamic_overlay(self, surface, player, before_player=True, camera_offset=(0,0)):
        camera_x, camera_y = camera_offset
        player_world_y = player.position[1] + player.desired_height // 2  # Player's anchor point in world coordinates

        for y, row in enumerate(self.map_array):
            for x, tile_keys in enumerate(row):
                if not isinstance(tile_keys, list):
                    tile_keys = [tile_keys]
                for tile_key in tile_keys:
                    if tile_key in self.tiles:
                        z_index = self.tile_metadata[tile_key].get('z_index', 0)
                        if z_index > 0:  # Only consider overlay elements
                            tile = self.tiles[tile_key]
                            tile_width, tile_height = tile.get_size()

                            # Calculate the base position in world coordinates
                            base_x = x * self.scaled_tile_size
                            base_y = y * self.scaled_tile_size

                            # Adjust for anchor
                            anchor = self.tile_metadata[tile_key].get('anchor', 'top-left')
                            if anchor == 'bottom-center':
                                draw_x = base_x + (self.scaled_tile_size // 2) - (tile_width // 2) - camera_x
                                draw_y = base_y + self.scaled_tile_size - tile_height - camera_y
                            else:  # 'top-left' anchor
                                draw_x = base_x - camera_x
                                draw_y = base_y - camera_y

                            # Determine if we should draw before or after the player based on y-position
                            tile_bottom_y = base_y + self.scaled_tile_size  # Assuming the tile's bottom aligns with the grid line
                            if (before_player and tile_bottom_y <= player.position[1] + player.desired_height // 2) or \
                            (not before_player and tile_bottom_y > player.position[1] + player.desired_height // 2):
                                surface.blit(tile, (draw_x, draw_y))