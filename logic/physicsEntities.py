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
        self.current_animation_frame = 0
        self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY
        self.frame_mapping = {
        'left': self.load_animation_frames('graphics/assets/player/running/left'),
        'right': self.load_animation_frames('graphics/assets/player/running/right'),
        'airborne': self.load_animation_frames('graphics/assets/player/airborne'),
        'standing': self.load_animation_frames('graphics/assets/player/standing')
        }
        
        self.collision_manager = PlayerCollisionManager(game.current_level_num) #Create a collision manager for the player
        self.gravity_delay_counter = PLAYER_GRAVITY_PULL_DELAY #Counter to delay the gravity pull
        self.status = 'standing' #Variable to keep track of the player's status (standing, left, right, airborne)
        self.sprite = self.frame_mapping.get(self.status)[self.current_animation_frame] #Initial sprite
        self.rect = self.sprite.get_rect(midbottom = (50, 400)) #Initial position

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
        self.apply_gravity() #Apply gravity

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

    def apply_inertia(self):
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
            self.current_animation_frame = -1 #Reset the animation frame
        elif result == 'death':
            self.reset_position()

        # Slow down the player's velocity (simulate friction)
        self.velocity[0] = max(0, self.velocity[0] - 1) if self.velocity[0] > 0 else min(0, self.velocity[0] + 1)
        self.velocity[1] = max(0, self.velocity[1] - 1) if self.velocity[1] > 0 else min(0, self.velocity[1] + 1)

    def apply_gravity(self):
        self.gravity_delay_counter -= 1 #Decrease the delay
        if self.gravity_delay_counter == 0: #If the delay has passed
            self.gravity_delay_counter = PLAYER_GRAVITY_PULL_DELAY #Reset the delay

            # Apply gravity to vertical velocity
            desired_x, desired_y = self.rect.midbottom[0], self.rect.midbottom[1] + self.velocity[1]
            result = self.collision_manager.allow_movement(desired_x, desired_y)
            if result == 'allowed':
                self.status = 'airborne'
                self.rect.midbottom = (desired_x, desired_y)
                if self.velocity[1] <= MAX_FALL_SPEED:
                    self.velocity[1] += FALLLING_SPEED
                else: self.velocity[1] = MAX_FALL_SPEED

            elif result == 'collision' and self.status == 'airborne': #If the player is airborne and collides with the ground
                self.velocity[1] = BASE_GRAVITY_PULL #Reset the vertical velocity
                self.current_animation = 0 #Set the current animation to standing
                self.current_animation_frame = -1 #Reset the animation frame
                self.status = 'standing'
            elif result == 'death':
                self.reset_position()

    def update_animation(self):
        
        # Animation frame switching
        self.animation_switching_delay -= 1
        if self.animation_switching_delay == 0: # If the delay has passed
            self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY  # Reset the delay

            # Update the current animation frame
            if self.current_animation_frame < len(self.frame_mapping[self.status]) - 1: self.current_animation_frame += 1
            else: self.current_animation_frame = 0

            # Update the sprite based on the current animation frame
            self.sprite = self.frame_mapping[self.status][self.current_animation_frame]

    def load_animation_frames(self, path): #Function that returns an array containing all the frames of an animation loaded as pygame surfaces
        frames_surfs = []
        frames = sorted(os.listdir(path))
        for frame_path in frames:
            final_path = os.path.join(path, frame_path)
            frames_surfs.append(pg.image.load(final_path).convert_alpha())
        
        return frames_surfs
    
    def reset_position(self):
        self.current_animation_frame = 0
        self.rect.midbottom = (50, 400)