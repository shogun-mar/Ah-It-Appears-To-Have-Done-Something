import pygame as pg
import os
from settings import PLAYER_SPEED, JUMP_STRENGTH, GRAVITY_STRENGTH, SCREEN_HEIGHT, PLAYER_ANIMATION_SWITCHING_DELAY

class Player:
    def __init__(self, screen_rect):
        #Animations (lists that keep all the frames of the animations)
        self.standing_frames = self.load_animation_frames('graphics/assets/player/standing')
        
        self.current_animation_frame = 0
        self.animation_switching_delay = PLAYER_ANIMATION_SWITCHING_DELAY

        self.sprite = self.standing_frames[self.current_animation_frame]
        self.rect = self.sprite.get_rect(midbottom = (50, SCREEN_HEIGHT - 125))
        self.status = 'standing'
        self.screen_rect = screen_rect
        self.speed = PLAYER_SPEED
        self.vertical_vel = 0

    def move(self, keys):
        if keys[pg.K_d]: #Right
            self.rect.centerx += self.speed
        elif keys[pg.K_a]: #Left
            self.rect.centerx -= self.speed
        elif keys[pg.K_SPACE] and self.status != 'jumping': #Jump
            self.status = 'jumping'
            self.vertical_vel = JUMP_STRENGTH

        self.apply_gravity()

        #Clamp the player rect to the screen rect to ensure that the player doesn't go off screen
        self.rect.clamp_ip(self.screen_rect)

    def apply_gravity(self):
        if self.rect.midbottom[1] < SCREEN_HEIGHT - 125:
            self.vertical_vel += GRAVITY_STRENGTH
            self.rect.midbottom = (self.rect.midbottom[0], self.rect.midbottom[1] + self.vertical_vel)
        if self.rect.midbottom[1] >= SCREEN_HEIGHT - 125:
            self.rect.midbottom = (self.rect.midbottom[0], SCREEN_HEIGHT - 125)
            self.vertical_vel = 0
            self.status = 'standing'

        #print(self.rect.midbottom[1])

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
        

