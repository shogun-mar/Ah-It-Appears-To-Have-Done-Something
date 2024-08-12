import os
import pygame as pg
from settings import *
from logic.collisionManager import CollisionManager, PlayerCollisionManager

class PhysicsEntity:
    def __init__(self, game, speed, sprite = None, rect = None,):
        self.sprite = sprite
        self.rect = rect
        self.velocity = [0, 0]
        self.movement = [False, False]
        self.game = game
        self.screen_rect = game.screen_rect
        self.collision_manager = CollisionManager(game.current_level_num)
        self.speed = speed

    def move(self):
        self.apply_gravity()

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

    def apply_gravity(self):
        desired_x, desired_y = self.rect.midbottom[0], self.rect.midbottom[1] + GRAVITY_STRENGTH #The position the player would be in if gravity was applied
        result = self.collision_manager.allow_movement(desired_x, desired_y)
        if result == 'allowed':
            self.rect.midbottom = (desired_x, desired_y)

class Player(PhysicsEntity):
    def __init__(self, game):
        super().__init__(game, speed = PLAYER_SPEED)

        #Animations (lists that keep all the frames of the animations)
        self.standing_frames = self.load_animation_frames('graphics/assets/player/standing')
    
        self.current_animation_frame = 0
        self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY
        
        self.collision_manager = PlayerCollisionManager(game.current_level_num)
        self.sprite = self.standing_frames[self.current_animation_frame]
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
            print('Death')
            # Add death logic here

        self.apply_inertia() #Apply movement caused by inertia
        self.apply_gravity() #Apply gravity

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

    def apply_inertia(self):
        # Apply gravity to vertical velocity
        self.velocity[1] += GRAVITY_STRENGTH

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
        elif result == 'death':
            print('Death')
            # Add death logic here
        elif result == 'collision':
            # Handle collision by stopping the jump
            if self.velocity[1] > 0:  # If falling
                self.velocity[1] = 0
            elif self.velocity[1] < 0:  # If jumping
                self.velocity[1] = 0

        # Slow down the player's velocity (simulate friction)
        self.velocity[0] = max(0, self.velocity[0] - 1) if self.velocity[0] > 0 else min(0, self.velocity[0] + 1)
        self.velocity[1] = max(0, self.velocity[1] - 1) if self.velocity[1] > 0 else min(0, self.velocity[1] + 1)

    def apply_gravity(self):
        desired_x, desired_y = self.rect.midbottom[0], self.rect.midbottom[1] + self.velocity[1]
        result = self.collision_manager.allow_movement(desired_x, desired_y)
        if result == 'allowed':
            self.rect.midbottom = (desired_x, desired_y)
        elif result == 'collision':
            self.velocity[1] = 0 #Reset the vertical velocity
        elif result == 'death':
            print('Death')
            #Add death logic here

        # Slow down the player's vertical velocity
        self.velocity[1] = max(0, self.velocity[1] - 1) if self.velocity[1] > 0 else min(0, self.velocity[1] + 1)

    def update_animation(self):
        self.animation_switching_delay -= 1
        if self.animation_switching_delay == 0:
            self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY #Reset the delay
            #Switch the animation frame
            if self.current_animation_frame <= 4:
                self.current_animation_frame += 1
            else:
                self.current_animation_frame = 0
            try:
                self.sprite = self.standing_frames[self.current_animation_frame]
            except IndexError:
                self.current_animation_frame = 0
                self.sprite = self.standing_frames[self.current_animation_frame]

    def load_animation_frames(self, path): #Function that returns an array containing all the frames of an animation loaded as pygame surfaces
        frames_surfs = []
        frames = sorted(os.listdir(path))
        for frame in frames:
            frame_path = os.path.join(path, frame)
            frames_surfs.append(pg.image.load(frame_path).convert_alpha())
        
        return frames_surfs