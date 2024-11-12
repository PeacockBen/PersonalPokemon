import pygame

class Player:
    def __init__(self, name, sprite_sheet_path, frame_width, frame_height):
        self.name = name
        self.inventory = []
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.desired_width = 32
        self.scale_factor = self.desired_width / self.frame_width
        self.desired_height = int(self.frame_height * self.scale_factor)
        self.position = [64, 64]  # Initial position of the player
        self.current_frame = self.get_frame(13, 11)  # Initial frame
        self.target_position = self.position.copy()
        self.moving = False
        self.step_size = 2
        self.step_distance = 32  # Distance to move in one stepself.step_distance = 32  # Distance to move in one step
        self.direction = 'down'  # Initial direction
        self.frame_index = 0  # Index of the current animation frame
        self.animation_speed = 30  # Number of frames to wait before switching to the next animation frame
        self.animation_counter = 0  # Counter to track the animation speed

        
        # Define the frames for each direction
        self.frames = {
            'down': [self.get_frame(13, 11), self.get_frame(77, 11), self.get_frame(141, 11), self.get_frame(205, 11)],
            'left': [self.get_frame(13, 77), self.get_frame(77, 77), self.get_frame(141, 77), self.get_frame(205, 77)],
            'right': [self.get_frame(13, 143), self.get_frame(77, 143), self.get_frame(141, 143), self.get_frame(205, 143)],
            'up': [self.get_frame(13, 200), self.get_frame(77, 200), self.get_frame(141, 200), self.get_frame(205, 200)]
        }

         # Calculate the number of frames required to move the full distance
        self.frames_per_step = self.step_distance // self.step_size
        self.animation_speed = self.frames_per_step // len(self.frames['down'])  # Adjust this to match the number of frames in your animation cycle
        self.animation_speed = self.animation_speed*2

    def get_frame(self, x, y):
        # Extract a frame from the sprite sheet at the given coordinates
        frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
        # Scale the frame to the desired width
        desired_width = 32
        scale_factor = desired_width / self.frame_width
        desired_height = int(self.frame_height * scale_factor)
        frame = pygame.transform.scale(frame, (int(desired_width), desired_height))
        return frame
    
    def move(self, direction, game_map):
        if not self.moving:
            new_target_position = self.target_position.copy()

            if direction == 'left':
                new_target_position[0] -= self.step_distance
            elif direction == 'right':
                new_target_position[0] += self.step_distance
            elif direction == 'up':
                new_target_position[1] -= self.step_distance
            elif direction == 'down':
                new_target_position[1] += self.step_distance

            # Convert position to map grid coordinates
            grid_x = new_target_position[0] // game_map.scaled_tile_size
            grid_y = new_target_position[1] // game_map.scaled_tile_size

            # Check if the new position is collidable
            if not game_map.is_collidable(grid_x, grid_y):
                # If not collidable, update the target position
                self.target_position = new_target_position
                self.direction = direction
                self.frame_index = 0  # Reset the animation frame index
                self.current_frame = self.frames[self.direction][self.frame_index]  # Set current frame
                self.moving = True

    def update(self, keys):
        if self.moving:
            if self.position[0] < self.target_position[0]:
                self.position[0] += self.step_size
                if self.position[0] > self.target_position[0]:
                    self.position[0] = self.target_position[0]
            elif self.position[0] > self.target_position[0]:
                self.position[0] -= self.step_size
                if self.position[0] < self.target_position[0]:
                    self.position[0] = self.target_position[0]
            elif self.position[1] < self.target_position[1]:
                self.position[1] += self.step_size
                if self.position[1] > self.target_position[1]:
                    self.position[1] = self.target_position[1]
            elif self.position[1] > self.target_position[1]:
                self.position[1] -= self.step_size
                if self.position[1] < self.target_position[1]:
                    self.position[1] = self.target_position[1]
            else:
                self.moving = False
                # If the button is not held down, reset to the first frame
                if not keys[pygame.K_a] and not keys[pygame.K_d] and not keys[pygame.K_w] and not keys[pygame.K_s]:
                    self.frame_index = 0
                    self.current_frame = self.frames[self.direction][self.frame_index]

            # Update the animation frame if still moving
            if self.moving:
                self.animation_counter += 1
                if self.animation_counter >= self.animation_speed:
                    self.animation_counter = 0
                    self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])
                    self.current_frame = self.frames[self.direction][self.frame_index]


    def get_name(self):
        return self.name

    def get_inventory(self):
        return self.inventory

    def add_to_inventory(self, item):
        self.inventory.append(item)
    
    def draw(self, screen):
        # Get the size of the current frame
        sprite_width, sprite_height = self.current_frame.get_size()
        # Adjust the position so that the bottom center of the sprite aligns with the player's position
        draw_x = self.position[0] + (32 - sprite_width) // 2
        draw_y = self.position[1] + 32 - sprite_height
        # Draw the player frame on the screen at the calculated position
        screen.blit(self.current_frame, (draw_x, draw_y))