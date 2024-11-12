# import pygame

# class Map:
#     def __init__(self, tilesheet, base_tile_size, scaled_tile_size):
#         self.tilesheet = tilesheet
#         self.base_tile_size = base_tile_size  # Original tile size in the tilesheet (e.g., 19x19)
#         self.scaled_tile_size = scaled_tile_size  # Desired tile size in the game (e.g., 32x32)
#         self.tiles = {}
#         self.tile_metadata = {
#             'x': {'position': (14, 19), 'size': (36, 45), 'anchor': 'top-left'},     # Wall tile
#             '0': {'position': (96, 2242), 'size': (32, 32), 'anchor': 'top-left'},    # Floor tile
#             'tree': {'position': (0, 20), 'size': (38, 57), 'anchor': 'bottom-center'}, # Larger tile
#             # Add more tiles with their positions, sizes, and anchors
#         }
#         self.load_tiles()

#     def load_tiles(self):
#         sheet = pygame.image.load(self.tilesheet).convert_alpha()
#         scale_factor = self.scaled_tile_size / self.base_tile_size
#         for key, data in self.tile_metadata.items():
#             x, y = data['position']
#             width, height = data['size']
#             rect = pygame.Rect(x, y, width, height)
#             tile = sheet.subsurface(rect)
#             # Scale the tile to the desired size
#             scaled_width = int(width * scale_factor)
#             scaled_height = int(height * scale_factor)
#             tile = pygame.transform.scale(tile, (scaled_width, scaled_height))
#             self.tiles[key] = tile

#     def draw(self, surface, map_array):
#         for y, row in enumerate(map_array):
#             for x, tile_key in enumerate(row):
#                 if tile_key in self.tiles:
#                     tile = self.tiles[tile_key]
#                     tile_width, tile_height = tile.get_size()
#                     # Calculate the position
#                     draw_x = x * self.scaled_tile_size
#                     draw_y = y * self.scaled_tile_size
#                     # Adjust for larger tiles based on anchor
#                     anchor = self.tile_metadata[tile_key].get('anchor', 'top-left')
#                     if anchor == 'bottom-center':
#                         draw_x += (self.scaled_tile_size - tile_width) // 2
#                         draw_y += self.scaled_tile_size - tile_height
#                     # Draw the tile
#                     surface.blit(tile, (draw_x, draw_y))
#                 else:
#                     # Handle unknown tile identifiers
#                     pass
                
import pygame

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
        self.load_tiles()

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
        
    def is_collidable(self, x, y):
        # Check if the coordinates are within the map boundaries
        if y < 0 or y >= len(self.map_array) or x < 0 or x >= len(self.map_array[y]):
            return False  # Out of bounds, assume not collidable
        
        # Get the list of tile keys at the given position
        tile_keys = self.map_array[y][x]
        if not isinstance(tile_keys, list):
            tile_keys = [tile_keys]

        # Check if any tile at this position is collidable
        for tile_key in tile_keys:
            if tile_key in self.tile_metadata and self.tile_metadata[tile_key]['collidable']:
                return True
        
        return False

    def draw_layer(self, surface, layer_type):
        # Draw either base or overlay layer tiles based on layer_type
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
                            # Calculate the base position
                            base_x = x * self.scaled_tile_size
                            base_y = y * self.scaled_tile_size
                            # Adjust for anchor
                            anchor = self.tile_metadata[tile_key].get('anchor', 'top-left')
                            if anchor == 'bottom-center':
                                draw_x = base_x + (self.scaled_tile_size - tile_width) // 2
                                draw_y = base_y + self.scaled_tile_size - tile_height
                            else:  # 'top-left'
                                draw_x = base_x
                                draw_y = base_y
                            # Draw tile
                            surface.blit(tile, (draw_x, draw_y))