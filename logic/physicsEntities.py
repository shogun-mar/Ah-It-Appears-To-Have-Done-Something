import os
import pygame as pg
from settings import *
from logic.collisionManager import CollisionManager, PlayerCollisionManager

class PhysicsEntity:
    def __init__(self, game, mass, sprite = None, rect = None):
        
        #Graphical representation of the entity
        self.sprite: pg.Surface = sprite
        self.rect: pg.Rect = rect
        
        #Physics variables
        self.mass: int = mass #The mass of the entity
        self.velocity: list[int] = [0, BASE_GRAVITY_PULL * mass] #The velocity of the entity in the x and y axis
        self.screen_rect: pg.Rect = game.screen_rect
        self.collision_manager: CollisionManager = CollisionManager(game.gameState.value)
    
        #Miscellaneous variables
        self.game = game
        self.level_num: int = game.gameState.value #The current level number

    def move(self):
        self.apply_gravity()

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

    def apply_gravity(self):
        desired_x, desired_y = self.rect.midbottom[0], self.rect.midbottom[1] + self.velocity[1]
        result = self.collision_manager.allow_movement(desired_x, desired_y)

        if result == 'allowed':
            self.rect.midbottom = (desired_x, desired_y)
        elif result == 'collision':
            self.velocity[1] = BASE_GRAVITY_PULL

class Player(PhysicsEntity):
    def __init__(self, game):
        super().__init__(game, mass=1)

        #Variables to keep track of animations
        self.current_animation_frame: int = 0
        self.animation_switching_delay: int = PLAYER_ANIMATION_SWITCHING_DELAY
        self.landing_sprite: pg.Surface = pg.image.load('graphics/assets/player/landing.png').convert_alpha()
        self.frame_mapping: dict[list[pg.Surface]] = {
        'left': self.load_animation_frames('graphics/assets/player/running/left'),
        'left airborne': self.load_animation_frames('graphics/assets/player/running/left'), 
        'right': self.load_animation_frames('graphics/assets/player/running/right'),
        'right airborne': self.load_animation_frames('graphics/assets/player/running/right'),
        'airborne': self.load_animation_frames('graphics/assets/player/airborne'),
        'standing': self.load_animation_frames('graphics/assets/player/standing')
        }
        
        #Variables to keep track of the player's physics
        self.collision_manager: PlayerCollisionManager = PlayerCollisionManager(self.level_num) #Create a collision manager for the player
        self.gravity_delay_counter: int = PLAYER_GRAVITY_PULL_DELAY #Counter to delay the gravity pull
        self.status: str = 'airborne' #Variable to keep track of the player's status (standing, left, right, airborne)
        self.sprite_width: int = self.frame_mapping.get(self.status)[self.current_animation_frame].get_width() #Width of the player's sprite
        self.moving_up: bool = False
        self.collision_line_x_coord: int = 0 #X coordinate of the collision line used to check if the player is standing on the ground

        #Variables to keep track of the player's graphical representation
        self.sprite: pg.Surface = self.frame_mapping.get(self.status)[self.current_animation_frame] #Initial sprite
        self.rect: pg.Rect = self.sprite.get_rect(midbottom = INITIAL_COORDS_PLAYER[self.level_num]) #Rect of the player

    def handle_input(self): #Input handling based on the get pressed method (There is no way to know the order of keys pressed, and rapidly pushed keys can be completely unnoticed between two calls)
        """Function that manages player related input by altering player's velocity list based on the pressed keys at the moment of the call."""
        
        keys: tuple[bool] = pg.key.get_pressed()
        CURRENT_SPEED_VALUE: int = PLAYER_SPEED_MID_AIR if self.moving_up else PLAYER_SPEED #Set the speed value based on the player's vertical velocity

        #Manage pressed keys
        if keys[PLAYER_LEFT_KEY] and keys[PLAYER_RIGHT_KEY]: 
            self.velocity[0] = 0 #Reset the player's horizontal velocity

        elif keys[PLAYER_LEFT_KEY]:
            if self.velocity[0] < -CURRENT_SPEED_VALUE: self.velocity[0] -= CURRENT_SPEED_VALUE #If the player was moving left add CURRENT_SPEED_VALUE to the player's velocity (this is done to keep eventual inertia)
            else: self.velocity[0] = int(-CURRENT_SPEED_VALUE) #If the player was not moving left set the player's velocity to CURRENT_SPEED_VALUE
        
        elif keys[PLAYER_RIGHT_KEY]:
            if self.velocity[0] > CURRENT_SPEED_VALUE: self.velocity[0] += CURRENT_SPEED_VALUE #If the player was moving right add CURRENT_SPEED_VALUE to the player's velocity (this is done to keep eventual inertia)
            else: self.velocity[0] = CURRENT_SPEED_VALUE #If the player was not moving right set the player's velocity to CURRENT_SPEED_VALUE

        if keys[PLAYER_JUMP_KEY] and self.status in ['standing', 'left', 'right'] and not self.has_just_landed():
            self.velocity[1] = BASE_JUMP_SPEED

        #Manage not pressed keys
        if not keys[PLAYER_LEFT_KEY]: #If the player was moving left remove CURRENT_SPEED_VALUE from the player's velocity (this is done to keep eventual inertia)
            if self.velocity[0] < 0: self.velocity[0] += CURRENT_SPEED_VALUE

        if not keys[PLAYER_RIGHT_KEY]: #If the player was moving right remove CURRENT_SPEED_VALUE from the player's velocity (this is done to keep eventual inertia)
            if self.velocity[0] > 0: self.velocity[0] -= CURRENT_SPEED_VALUE

    def move(self): 
        """Function that manages the player's movement complete of gravity based movement, inertia and collision detection."""

        # Inizialize desired coords based on player movement
        self.moving_up = self.velocity[1] < BASE_GRAVITY_PULL
        if self.status == 'left': # Moving left (second condition is to prevent the player from moving left right after landing)
            desired_x, desired_y = self.clamp_to_screen(self.rect.midleft[0] - abs(self.velocity[0]), self.rect.midleft[1])
        elif self.status == 'right': # Moving right (second condition is to prevent the player from moving left right after landing)
            desired_x, desired_y = self.clamp_to_screen(self.rect.midright[0] + abs(self.velocity[0]), self.rect.midright[1])
        elif self.status == 'left airborne' and self.moving_up:
            desired_x, desired_y = self.clamp_to_screen(self.rect.topleft[0] - abs(self.velocity[0]), self.rect.topleft[1] - abs(self.velocity[1])) #Has to be absolute value because in the settings values for moving updwards are negative so by subtracting a negative value the player would move downwards
        elif self.status == 'right airborne' and self.moving_up:
            desired_x, desired_y = self.clamp_to_screen(self.rect.topright[0] + abs(self.velocity[0]), self.rect.topright[1] - abs(self.velocity[1])) #Has to be absolute value because in the settings values for moving updwards are negative so by subtracting a negative value the player would move downwards")        
        elif self.status == 'airborne' and self.moving_up:
            desired_x, desired_y = self.clamp_to_screen(self.rect.midtop[0], self.rect.midtop[1] - abs(self.velocity[1])) #Has to be absolute value because in the settings values for moving updwards are negative so by subtracting a negative value the player would move downwards

        #Check if desired movement is possible
        if self.status == 'left':
            result = self.collision_manager.allow_movement(desired_x, desired_y)
            if result == 'allowed' and not self.has_just_landed():
                self.rect.midleft = desired_x, desired_y
            elif result == 'collision':
                self.velocity[0] = 0 #Stop the player's horizontal movement
            elif result == 'death':
                self.reset_position()
            
        elif self.status == 'right':
            result = self.collision_manager.allow_movement(desired_x, desired_y)
            if result == 'allowed' and not self.has_just_landed():
                self.rect.midright = desired_x, desired_y
            elif result == 'collision':
                self.velocity[0] = 0 #Stop the player's horizontal movement
            elif result == 'death':
                self.reset_position()
        
        elif self.status == 'left airborne' and self.moving_up:
            result = self.collision_manager.allow_movement(desired_x, desired_y)
            if result == 'allowed': self.rect.topleft = desired_x, desired_y
            elif result == 'death': self.reset_position()
            elif result == 'collision':
                initial_desired_y = desired_y
                for i in range(abs(self.velocity[1]), -1, -1):
                    desired_y = initial_desired_y + i
                    result = self.collision_manager.allow_movement(desired_x, initial_desired_y)
                    if result == 'allowed':
                        self.rect.topleft = desired_x, desired_y
                        break

                self.velocity = [0, BASE_GRAVITY_PULL] #Reset the player's velocity

        elif self.status == 'right airborne' and self.moving_up:  
            result = self.collision_manager.allow_movement(desired_x, desired_y)
            if result == 'allowed': self.rect.topright = desired_x, desired_y
            elif result == 'death': self.reset_position()
            elif result == 'collision':
                initial_desired_y = desired_y
                for i in range(abs(self.velocity[1]), -1, -1):
                    desired_y = initial_desired_y + i
                    result = self.collision_manager.allow_movement(desired_x, initial_desired_y)
                    if result == 'allowed':
                        self.rect.right = desired_x, desired_y
                        break

                self.velocity = [0, BASE_GRAVITY_PULL] #Reset the player's velocity

        elif self.status == 'airborne':
            if self.velocity[1] < 0:
                result = self.collision_manager.allow_movement(desired_x, desired_y)
                if result == 'allowed': self.rect.midtop = desired_x, desired_y
                elif result == 'death': self.reset_position()
                elif result == 'collision':
                    for i in range(abs(self.velocity[1])): #Iterate over the player's vertical velocity to find the first position where the player can move to
                        desired_y = self.rect.midtop[1] - i #without this loop the player would stop n pixels before the ceiling with n being the player's vertical velocity
                        result = self.collision_manager.allow_movement(desired_x, desired_y)
                        if result == 'allowed':
                            self.rect.midtop = (desired_x, desired_y)
                            break

                    self.velocity = [0, BASE_GRAVITY_PULL] #Reset the player's velocity

            elif self.velocity[1] == 0: #If the player has reached the apex of the jump
                self.velocity[1] = BASE_GRAVITY_PULL #Reset the vertical velocity to the base gravity pull
        
        self.apply_gravity() #Apply movement caused by gravity

        # Update the player's status based on the movement
        if self.velocity[0] < 0: #If the player is moving left
            if self.velocity[1] != BASE_GRAVITY_PULL: self.status = 'left airborne' 
            else: self.status = 'left'
        
        elif self.velocity[0] > 0: #If the player is moving right
            if self.velocity[1] != BASE_GRAVITY_PULL: self.status = 'right airborne'
            else: self.status = 'right'
        
        elif self.velocity[1] < 0: self.status = 'airborne' #If the player is moving upwards set the status to airborne (could have used self.moving_up but this is more uniform with the other checks)
        
        elif self.velocity[0] == 0 and self.velocity[1] == BASE_GRAVITY_PULL and self.status not in ['airborne', 'left airborne', 'right airborne']: self.status = 'standing'

    def apply_gravity(self):
        """Function that manages gravity based movement complete of sideways movement and collision detection."""
        
        self.gravity_delay_counter -= 1 #Decrease the delay
        if self.gravity_delay_counter == 0: #If the delay has passed
            self.gravity_delay_counter = PLAYER_GRAVITY_PULL_DELAY #Reset the delay

            if self.moving_up: #If the player is moving upwards (jumping) apply the gravity pull
                self.velocity[1] += FALLING_SPEED_INCR

            else: #If the player is falling

                #Initial default desired coords to avoid UnboundLocalError TOFIX TOREMOVE
                desired_x, desired_y = self.rect.midbottom[0], self.rect.midbottom[1] + (self.velocity[1] * FALLING_SPEED_INCR)

                #Calculate desired coords based on the player's velocity and movement
                hor_offset = 7 #Offset used to avoid the event in which the player falls through the ground if near a ledge it rapidly moves to the opposite side of the ledge
                if self.velocity[0] < 0: #If the player is moving left check the collision on the right side so that the player falls when it fully overcomes the obstacle
                    desired_x, desired_y = self.rect.bottomright[0] - hor_offset, self.rect.bottomright[1] + (self.velocity[1] * FALLING_SPEED_INCR)
                elif self.velocity[0] > 0: #If the player is moving right check the collision on the left side so that the player falls when it fully overcomes the obstacle
                    desired_x, desired_y = self.rect.bottomleft[0] + hor_offset, self.rect.bottomleft[1] + (self.velocity[1] * FALLING_SPEED_INCR)
                else:
                    desired_x, desired_y = self.rect.midbottom[0], self.rect.midbottom[1] + (self.velocity[1] * FALLING_SPEED_INCR)

                self.collision_line_x_coord = desired_x #Update the collision line coords TOFIX TOREMOVE FOR DEBUGGING

                #Check if the player can move to the desired position
                result = self.collision_manager.allow_movement(desired_x, desired_y)

                if result == 'allowed' and self.status != 'standing': #If the player is airborne and there is no collision with the ground
                    self.status = 'airborne' #Update the player's status
                    if self.velocity[0] < 0: #If the player is moving left
                        final_coords = desired_x - self.sprite_width, desired_y #The coords need to be adjusted because the desired coords were calculated so that the opposing side of the player during movement would be checked for collision
                        self.rect.bottomleft = final_coords #Update the player's position
                    elif self.velocity[0] > 0: #If the player is moving right
                        final_coords = desired_x + self.sprite_width, desired_y
                        self.rect.bottomright = final_coords #Update the player's position
                    else:
                        self.rect.midbottom = (desired_x, desired_y) #Update the player's position

                    self.velocity[1] = min(self.velocity[1] + FALLING_SPEED_INCR, MAX_DOWN_VELOCITY) #Apply gravity to the vertical velocity (if the velocity is less than the maximum allowed)

                elif result == 'death': #If the player collides with a death block
                    self.reset_position()

                elif result == 'collision' and self.status in ['airborne', 'left airborne', 'right airborne']: #If the player is airborne and collides with the ground
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
                    self.velocity = [0, BASE_GRAVITY_PULL] #Reset the player's velocity

                    self.sprite = self.landing_sprite #Set the sprite to the landing frame
                    self.current_animation_frame = 0 #Reset the animation frame
                    self.animation_switching_delay = int(PLAYER_ANIMATION_SWITCHING_DELAY * (0.8 + (self.velocity[1] / 10))) #Dinamically set the delay to make so the landing seems heavy
                    
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
        """"Function that takes care of updating the player's sprite to follow an animation loop based on the player's status."""
        
        # Animation frame switching
        self.animation_switching_delay -= 1
        if self.animation_switching_delay == 0: # If the delay has passed
            self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY  # Reset the delay

            # Update the current animation frame
            if (self.current_animation_frame < len(self.frame_mapping[self.status]) - 1):
                self.current_animation_frame += 1
            else:
                self.current_animation_frame = 0
            
            self.sprite = self.frame_mapping[self.status][self.current_animation_frame] # Update the sprite based on the current animation frame

    def load_animation_frames(self, path):
        """#Function that returns an array containing all the frames of an animation loaded as pygame surfaces"""

        frames_surfs = []
        frames = sorted(os.listdir(path))
        for frame_path in frames:
            final_path = os.path.join(path, frame_path)
            frames_surfs.append(pg.image.load(final_path).convert_alpha())
        
        return frames_surfs
    
    def clamp_to_screen(self, x, y):
        """"Function that clamps the desired x and y values to the screen dimensions to avoid IndexErrors and to keep the player on screen."""

        clamped_x = max(0, min(x, SCREEN_WIDTH - 1))
        clamped_y = max(0, min(y, SCREEN_HEIGHT - 1))
        return clamped_x, clamped_y

    def has_just_landed(self): 
        """"Function that returns whether the player has just landed or not based on the player's sprite, used to determine whether the player can move or not after landing, by not allowing the player to move for a few frames after landing to simulate a heavy landing."""
        return self.sprite == self.landing_sprite 

    def reset_position(self):
        """"Function that resets the player's position to the initial position in the current level and resets the frame counter to make the player's animation start from the beginning."""
        self.current_animation_frame = -1 #Reset the animation frame counter
        self.rect.midbottom = INITIAL_COORDS_PLAYER[self.level_num] #Reset the player's position to the initial values