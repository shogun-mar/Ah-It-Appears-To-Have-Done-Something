import os
import pygame as pg
from settings import *

class PhysicsEntity:
    def __init__(self, game, speed, sprite = None, rect = None,):
        self.sprite = sprite
        self.rect = rect
        self.velocity = [0, 0]
        self.movement = [False, False]
        self.game = game
        self.screen_rect = game.screen_rect
        self.speed = speed

    def move(self):
        self.rect.centerx  += (self.movement[1] - self.movement[0]) * self.speed #Boolean values are implicitly converted to 1 or 0
        self.apply_gravity()

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

    def apply_gravity(self):
        collidable_objects_y_values = [rect.topleft[1] for rect in self.game.collidable_objects]
        player_foot_y = self.rect.midbottom[1]
        
        if player_foot_y < SCREEN_HEIGHT and player_foot_y not in collidable_objects_y_values:
            self.vertical_vel -= GRAVITY_STRENGTH
            self.rect.midbottom = (self.rect.midbottom[0], self.rect.midbottom[1] + self.vertical_vel)

class Player(PhysicsEntity):
    def __init__(self, game):
        super().__init__(game, speed = PLAYER_SPEED)

        #Animations (lists that keep all the frames of the animations)
        self.standing_frames = self.load_animation_frames('graphics/assets/player/standing')
        
        self.current_animation_frame = 0
        self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY
        self.sprite = self.standing_frames[self.current_animation_frame]
        self.rect = self.sprite.get_rect(midbottom = (50, SCREEN_HEIGHT - 125))
        self.status = 'standing'

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