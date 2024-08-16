import os
import pygame as pg
from settings import *
from logic.collisionManager import CollisionManager, PlayerCollisionManager

class PhysicsEntity:
    def __init__(self, game, mass, speed, sprite = None, rect = None):
        
        #Graphical representation of the entity
        self.sprite = sprite
        self.rect = rect
        
        #Physics variables
        self.mass = mass #The mass of the entity
        self.velocity = [0, BASE_GRAVITY_PULL * mass] #The velocity of the entity in the x and y axis
        self.movement = [False, False]
        self.screen_rect = game.screen_rect
        self.collision_manager = CollisionManager(game.gameState.value)
        self.speed = speed
    
        #Miscellaneous variables
        self.game = game
        self.level_num = game.gameState.value #The current level number

    def move(self):
        self.apply_gravity()

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

    def apply_gravity(self):
        desired_x, desired_y = self.rect.bottomleft[0], self.rect.bottomleft[1] + self.velocity[1]
        result = self.collision_manager.allow_movement(desired_x, desired_y)

        if result == 'allowed':
            self.rect.midbottom = (desired_x, desired_y)
        elif result == 'collision':
            self.velocity[1] = BASE_GRAVITY_PULL

class Player(PhysicsEntity):
    def __init__(self, game):
        super().__init__(game, speed = PLAYER_SPEED, mass=1)

        #Variables to keep track of animations
        self.current_animation_frame = 0
        self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY
        self.frame_mapping = {
        'left': self.load_animation_frames('graphics/assets/player/running/left'),
        'right': self.load_animation_frames('graphics/assets/player/running/right'),
        'airborne': self.load_animation_frames('graphics/assets/player/airborne'),
        'standing': self.load_animation_frames('graphics/assets/player/standing')
        }
        
        #Variables to keep track of the player's physics
        self.collision_manager = PlayerCollisionManager(self.level_num) #Create a collision manager for the player
        self.gravity_delay_counter = PLAYER_GRAVITY_PULL_DELAY #Counter to delay the gravity pull
        self.status = 'airborne' #Variable to keep track of the player's status (standing, left, right, airborne)
        #Miscellaneous
        self.beginning_of_jump_charge = 0 #Variable to keep track of when the player started charging the jump
        self.jump_charge_time = 0 #Variable to keep track of how long the player has been charging the jump

        #Variables to keep track of the player's graphical representation
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

        # Clamp desired_x and desired_y to the screen dimensions to avoid IndexErrors and to keep the player on screen
        desired_x = max(0, min(desired_x, SCREEN_WIDTH - 1))
        desired_y = max(0, min(desired_y, SCREEN_HEIGHT - 1))

        #Check if movement is possible
        result = self.collision_manager.allow_movement(desired_x, desired_y)
        if result == 'allowed':
            if self.movement[0] and not self.movement[1]:  #Update the rect position based on the movement
                self.rect.midleft = desired_x, desired_y
            elif self.movement[1] and not self.movement[0]:  # Update the rect position based on the movement
                self.rect.midright = desired_x, desired_y
        elif result == 'death':
            self.reset_position()

        if self.status == 'airborne' and self.velocity[1] < 0: #If moving upwards (jumping)
            desired_x, desired_y = self.rect.midtop[0], self.rect.midtop[1] - abs(self.velocity[1]) #Has to be absolute value because in the settings values for moving updwards are negative so by subtracting a negative value the player would move downwards-

            result = self.collision_manager.allow_movement(desired_x, desired_y)
            if result == 'allowed':
                self.rect.midtop = (desired_x, desired_y)
            elif result == 'collision':
                for i in range(abs(self.velocity[1])): #Iterate over the player's vertical velocity to find the first position where the player can move to
                    desired_y = self.rect.midtop[1] - i #without this loop the player would stop n pixels before the ceiling with n being the player's vertical velocity
                    result = self.collision_manager.allow_movement(desired_x, desired_y)
                    if result == 'allowed':
                        self.rect.midtop = (desired_x, desired_y)
                        break

                self.velocity[1] = BASE_GRAVITY_PULL
            elif result == 'death':
                self.reset_position()

        self.apply_gravity() #Apply movement caused by gravity

        #if self.velocity[0] != 0 and self.velocity[1] > 0: self.apply_inertia() #Apply movement caused by inertia

    def apply_gravity(self):
        self.gravity_delay_counter -= 1 #Decrease the delay
        if self.gravity_delay_counter == 0: #If the delay has passed
            self.gravity_delay_counter = PLAYER_GRAVITY_PULL_DELAY #Reset the delay

            if self.velocity[1] >= 0: #If the player is falling
                desired_x, desired_y = self.rect.midbottom[0], self.rect.midbottom[1] + (self.velocity[1] * FALLING_SPEED_INCR)
                result = self.collision_manager.allow_movement(desired_x, desired_y)

                if result == 'allowed' and self.status != 'standing': #If the player is airborne and there is no collision with the ground
                    self.status = 'airborne' #Update the player's status
                    self.rect.midbottom = (desired_x, desired_y) #Update the player's position
                    self.velocity[1] = min(self.velocity[1] + FALLING_SPEED_INCR, MAX_DOWN_VELOCITY) #Apply gravity to the vertical velocity (if the velocity is less than the maximum allowed)

                elif result == 'collision' and self.status == 'airborne': #If the player is airborne and collides with the ground
                    # Constants
                    initial_desired_y = self.rect.midbottom[1] + (self.velocity[1] * FALLING_SPEED_INCR)
                    desired_x = self.rect.midbottom[0]

                    for i in range(self.velocity[1]): #Iterate over the player's vertical velocity to find the first position where the player can land (not doing this would make the player land N pixels above the ground with N being the player's vertical velocity) 
                        desired_y = initial_desired_y - i
                        result = self.collision_manager.allow_movement(desired_x, desired_y)
                        if result == 'allowed':  # If the player can move to the desired position
                            self.rect.midbottom = (desired_x, desired_y)  # Update the player's position
                            break

                    self.status = 'standing' #Update the player's status
                    self.sprite = self.frame_mapping['airborne'][3] #Set the sprite to the landing frame
                    self.current_animation_frame = 0 #Reset the animation frame
                    self.animation_switching_delay = int(PLAYER_ANIMATION_SWITCHING_DELAY * (0.8 + (self.velocity[1] / 10))) #Dinamically set the delay to make so the landing seems heavy
                    #print(f"vertical velocity: {self.velocity[1]}, delay: {self.animation_switching_delay}\n")
                    self.velocity[1] = BASE_GRAVITY_PULL #Reset the vertical velocity

                elif result == 'death':
                    self.reset_position()

            else: #If the player is moving upwards (jumping) apply the gravity pull
                self.velocity[1] += FALLING_SPEED_INCR
    
    def apply_inertia(self):
        # Clamp the velocity to a maximum value
        self.velocity[0] = max(min(self.velocity[0], MAX_ENTITY_SPEED), -MAX_ENTITY_SPEED)
        self.velocity[1] = max(min(self.velocity[1], MAX_DOWN_VELOCITY), -BASE_JUMP_SPEED)

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

    def update_animation(self):

        # Update the player's status based on the movement
        if self.movement[0] and not self.movement[1]: self.status = 'left'
        elif self.movement[1] and not self.movement[0]: self.status = 'right'
        elif self.velocity[1] != BASE_GRAVITY_PULL: self.status = 'airborne'
        elif ((self.movement == [False, False]) or (self.movement == [True, True])) and self.status != 'airborne': self.status = 'standing'
        
        # Animation frame switching
        self.animation_switching_delay -= 1
        if self.animation_switching_delay == 0: # If the delay has passed
            self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY  # Reset the delay

            # Update the current animation frame
            if (self.current_animation_frame < len(self.frame_mapping[self.status]) - 1) and (self.status != 'airborne' and self.current_animation_frame != 2): 
                    self.current_animation_frame += 1
            else: self.current_animation_frame = 0
            
            self.sprite = self.frame_mapping[self.status][self.current_animation_frame]# Update the sprite based on the current animation frame

    def load_animation_frames(self, path): #Function that returns an array containing all the frames of an animation loaded as pygame surfaces
        frames_surfs = []
        frames = sorted(os.listdir(path))
        for frame_path in frames:
            final_path = os.path.join(path, frame_path)
            frames_surfs.append(pg.image.load(final_path).convert_alpha())
        
        return frames_surfs
    
    def reset_position(self):
        self.current_animation_frame = -1 #Reset the animation frame counter
        self.rect.midbottom = INITIAL_COORDS_PLAYER[self.level_num] #Reset the player's position to the initial values