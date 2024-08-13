import os
import pygame as pg
from settings import *
from logic.collisionManager import CollisionManager, PlayerCollisionManager

class PhysicsEntity:
    def __init__(self, game, speed, sprite = None, rect = None,):
        self.sprite = sprite
        self.rect = rect
        self.velocity = [0, BASE_GRAVITY_PULL] #The velocity of the entity in the x and y axis
        self.movement = [False, False]
        self.game = game
        self.screen_rect = game.screen_rect
        self.collision_manager = CollisionManager(game.current_level_num)
        self.speed = speed

    def move(self):
        self.apply_gravity()

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

class Player(PhysicsEntity):
    def __init__(self, game):
        super().__init__(game, speed = PLAYER_SPEED)

        #Variables to keep track of animations
        standing_frames = self.load_animation_frames('graphics/assets/player/standing')
        running_left_frames = self.load_animation_frames('graphics/assets/player/running/left')
        running_right_frames = self.load_animation_frames('graphics/assets/player/running/right')
        jumping_frames = self.load_animation_frames('graphics/assets/player/jumping')
        self.animations = [standing_frames, running_left_frames, running_right_frames, jumping_frames]
        self.current_animation = 0
        self.current_animation_frame = 0
        self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY
        
        self.collision_manager = PlayerCollisionManager(game.current_level_num)
        self.gravity_pull_delay = PLAYER_GRAVITY_PULL_DELAY
        self.sprite = self.animations[self.current_animation][self.current_animation_frame]
        self.rect = self.sprite.get_rect(midbottom = (50, 500))

    def move(self):
        # Initialize desired position with the player's current position
        desired_x, desired_y = self.rect.centerx, self.rect.centery

        # Update desired position based on player movement
        if self.movement[0] and not self.movement[1]:  # Moving left
            desired_x = self.rect.midleft[0] - self.speed
            desired_y = self.rect.midleft[1]
        elif self.movement[1] and not self.movement[0]:  # Moving right
            desired_x = self.rect.midright[0] + self.speed
            desired_y = self.rect.midright[1]

        # Check if movement is allowed
        result = self.collision_manager.allow_movement(desired_x, desired_y)
        if result == 'allowed':
            if self.movement[0] and not self.movement[1]:  #Update the rect position based on the movement
                self.rect.midleft = desired_x, desired_y
            elif self.movement[1] and not self.movement[0]:  # Update the rect position based on the movement
                self.rect.midright = desired_x, desired_y
        elif result == 'death':
            self.reset_position()

        #if self.velocity[0] != 0 and self.velocity[1] > 0: self.apply_inertia() #Apply movement caused by inertia
        self.apply_gravity() #Apply gravity if player is standing or falling

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

    def apply_inertia(self):
        # Apply gravity to vertical velocity
        #self.velocity[1] += GRAVITY_STRENGTH

        # Clamp the velocity to a maximum value
        self.velocity[0] = max(min(self.velocity[0], MAX_SPEED), -MAX_SPEED)
        self.velocity[1] = max(min(self.velocity[1], MAX_FALL_SPEED), -MAX_JUMP_SPEED)

        # Calculate desired position based on velocity
        desired_x = self.rect.midtop[0] + self.velocity[0]
        desired_y = self.rect.midtop[1] + self.velocity[1]

        # Check for collisions and update position
        result = self.collision_manager.allow_movement(desired_x, desired_y)
        if result == 'allowed':
            self.rect.midtop = (desired_x, desired_y)
        elif result == 'collision':
            self.current_animation = 0 #Set the current animation to standing
            self.current_animation_frame = 0 #Reset the animation frame
        elif result == 'death':
            self.reset_position()

        # Slow down the player's velocity (simulate friction)
        self.velocity[0] = max(0, self.velocity[0] - 1) if self.velocity[0] > 0 else min(0, self.velocity[0] + 1)
        self.velocity[1] = max(0, self.velocity[1] - 1) if self.velocity[1] > 0 else min(0, self.velocity[1] + 1)

    def apply_gravity(self):
        self.gravity_pull_delay -= 1 #Decrease the delay
        if self.gravity_pull_delay == 0: #If the delay has passed
            self.gravity_pull_delay = PLAYER_GRAVITY_PULL_DELAY #Reset the delay

            # Apply gravity to vertical velocity
            desired_x, desired_y = self.rect.midbottom[0], self.rect.midbottom[1] + self.velocity[1]
            result = self.collision_manager.allow_movement(desired_x, desired_y)
            if result == 'allowed':
                self.rect.midbottom = (desired_x, desired_y)
                if self.velocity[1] <= MAX_FALL_SPEED:
                    self.velocity[1] += FALLLING_SPEED
                else: self.velocity[1] = MAX_FALL_SPEED

            elif result == 'collision':
                self.velocity[1] = BASE_GRAVITY_PULL #Reset the vertical velocity
                self.current_animation = 0 #Set the current animation to standing
                self.current_animation_frame = 0 #Reset the animation frame
            elif result == 'death':
                self.reset_position()
            

    def update_animation(self):
        #print(f"Current_animation : {self.get_current_animation_name()} and frame : {self.current_animation_frame}")

        # Check and switch animation based on player state
        if self.velocity[0] == 0 and self.velocity[1] == 0:  # Standing still
            if self.current_animation != 0:
                self.current_animation = 0
                self.current_animation_frame = 0  # Reset the animation frame to the first frame
        elif self.movement == [True, False]:  # Moving left
            if self.current_animation != 1:
                self.current_animation = 1
                self.current_animation_frame = 0  # Reset the animation frame to the first frame
        elif self.movement == [False, True]:  # Moving right
            if self.current_animation != 2:
                self.current_animation = 2
                self.current_animation_frame = 0  # Reset the animation frame to the first frame
        elif self.velocity[1] > BASE_GRAVITY_PULL:  # Jumping or falling
            if self.current_animation != 3:
                self.current_animation = 3
                self.current_animation_frame = 0  # Reset the animation frame to the first frame

        # Animation frame switching
        self.animation_switching_delay -= 1
        if self.animation_switching_delay == 0: # If the delay has passed
            self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY  # Reset the delay

            # Increment the animation frame
            if self.current_animation_frame < 3: self.current_animation_frame += 1
            else: self.current_animation_frame = 0

            # Update the sprite to the new frame
            self.sprite = self.animations[self.current_animation][self.current_animation_frame]

    def load_animation_frames(self, path): #Function that returns an array containing all the frames of an animation loaded as pygame surfaces
        frames_surfs = []
        frames = sorted(os.listdir(path))
        for frame_path in frames:
            final_path = os.path.join(path, frame_path)
            frames_surfs.append(pg.image.load(final_path).convert_alpha())
        
        return frames_surfs
    
    def reset_position(self):
        self.current_animation = 0
        self.current_animation_frame = 0
        self.rect.midbottom = (50, 500)

    def get_current_animation_name(self):
        if self.current_animation == 0: return 'standing'
        elif self.current_animation == 1: return 'running left'
        elif self.current_animation == 2: return 'running right'
        elif self.current_animation == 3: return 'jumping'
        else: return 'unknown'