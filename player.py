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
        self.position = [80, 112]  # Initial position of the player
        self.current_frame = self.get_frame(13, 11)  # Initial frame
        self.target_position = self.position.copy()
        self.moving = False
        self.normal_step_size = 2
        self.sprint_step_size = 3 
        self.step_size = self.normal_step_size  # Default speed
        self.step_distance = 32  # Distance to move in one step
        self.direction = 'down'  # Initial direction
        self.frame_index = 0  # Index of the current animation frame
        self.frames_per_step = self.step_distance // self.normal_step_size
        self.animation_counter = 0  # Counter to track movement progress in frames
        self.animation_speed = 4  # Number of movement steps before changing animation frame

        # Define the frames for each direction
        self.frames = {
            'down': [self.get_frame(14, 10), self.get_frame(78, 10), self.get_frame(142, 10), self.get_frame(206, 10)],
            'left': [self.get_frame(14, 76), self.get_frame(78, 76), self.get_frame(142, 76), self.get_frame(206, 76)],
            'right': [self.get_frame(14, 140), self.get_frame(78, 140), self.get_frame(142, 140), self.get_frame(206, 140)],
            'up': [self.get_frame(14, 204), self.get_frame(78, 204), self.get_frame(142, 204), self.get_frame(206, 204)]
        }

        # Calculate the number of frames required to move the full distance
        self.frames_per_step = self.step_distance // self.step_size
        self.animation_speed = self.frames_per_step // len(self.frames['down'])  # Adjust this to match the number of frames in your animation cycle


    def get_frame(self, x, y):
        # Extract a frame from the sprite sheet at the given coordinates
        frame = self.sprite_sheet.subsurface((x, y, self.frame_width, self.frame_height))
        # Scale the frame to the desired size
        scaled_width = int(self.frame_width * self.scale_factor)
        scaled_height = int(self.frame_height * self.scale_factor)
        frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
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

            # Correctly position the collision rectangle at the feet or lower half
            collision_width = self.desired_width // 2  # Adjust to fit the lower half
            collision_height = self.desired_height // 4  # Focus on the bottom quarter for collisions
            player_rect = pygame.Rect(
                new_target_position[0] - (collision_width // 2),  # Center horizontally
                new_target_position[1] + (self.desired_height // 2)-32,  # Start from halfway down
                collision_width,
                collision_height
            )

            # Check for collision
            if not game_map.is_collidable(player_rect):
                # If not collidable, update the target position
                self.target_position = new_target_position
                self.direction = direction
                self.frame_index = 0  # Reset the animation frame index
                self.current_frame = self.frames[self.direction][self.frame_index]  # Set current frame
                self.moving = True

    def update(self, keys):
        # Check if the player is sprinting
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.step_size = self.sprint_step_size
        else:
            self.step_size = self.normal_step_size

        if self.moving:
            # Update position towards target
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

            # Update the animation frame based on movement progress
            if self.moving:
                self.animation_counter += self.step_size  # Accumulate based on step size
                if self.animation_counter >= self.step_distance / len(self.frames[self.direction]):
                    self.animation_counter = 0
                    self.frame_index = (self.frame_index + 1) % len(self.frames[self.direction])
                    self.current_frame = self.frames[self.direction][self.frame_index]

    def draw(self, screen, screen_width, screen_height):
        # Get the size of the current frame
        sprite_width, sprite_height = self.current_frame.get_size()
        # Adjust the position so that the bottom center of the sprite aligns with the center of the screen
        draw_x = screen_width // 2 - sprite_width // 2
        draw_y = screen_height // 2 - sprite_height + self.desired_height // 2
        # Draw the player frame on the screen at the calculated position
        screen.blit(self.current_frame, (draw_x, draw_y))