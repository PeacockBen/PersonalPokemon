import pygame
from player import Player
from map import Map

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 832  # Adjusted to fit 26 tiles at 32px each
screen_height = 640  # Adjusted to fit 20 tiles at 32px each
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Game")

# Initialize the player
player = Player("Ash Ketchum", "assets/ash_sprite.png", frame_width=36, frame_height=50)

# Set up the clock
clock = pygame.time.Clock()
frame_rate = 60  # Frames per second

# Define the map array with layers
map_array = [
    # Each cell can be a list of tile keys to handle multiple tiles per cell
    [['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0'], ['0','x']],
    [['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x'], ['0','x']]
    # Add more rows as needed
]
# Initialize the map
game_map = Map('assets/pokemon_tileset32.png', base_tile_size=32, scaled_tile_size=32, map_array=map_array)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle user input
    keys = pygame.key.get_pressed()
    if not player.moving:
        if keys[pygame.K_a]:
            player.move('left', game_map)  # Pass the map to check collisions
        elif keys[pygame.K_d]:
            player.move('right', game_map)  # Pass the map to check collisions
        elif keys[pygame.K_w]:
            player.move('up', game_map)  # Pass the map to check collisions
        elif keys[pygame.K_s]:
            player.move('down', game_map)  # Pass the map to check collisions

    # Update game logic
    player.update(keys)

    # Render graphics in separate layers
    screen.fill((0, 0, 0))  # Fill the screen with black

    # Draw base layer (grass, paths, etc.)
    game_map.draw_layer(screen, 'base')

    # Draw overlay elements behind the player based on player position
    game_map.draw_dynamic_overlay(screen, player, before_player=True)

    # Draw player (in between base and overlay layers)
    player.draw(screen)

    # Draw overlay elements in front of the player based on player position
    game_map.draw_dynamic_overlay(screen, player, before_player=False)

    pygame.display.flip()  # Update the display
    # Cap the frame rate
    clock.tick(frame_rate)

# Quit the game
pygame.quit()