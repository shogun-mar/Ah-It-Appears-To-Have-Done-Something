import pygame as pg
from settings import PLAYER_SPEED, JUMP_STRENGTH, GRAVITY_STRENGTH  

class Player:
    def __init__(self):
        self.sprite = 
        self.rect = 
        self.status = 'standing'
        self.speed = PLAYER_SPEED
        self.vertical_vel = 0

    def move(self, key):
        if key == pg.K_d: #Right
            self.rect.centerx += self.speed
        elif key == pg.K_a: #Left
            self.rect.centerx -= self.speed
        elif key == pg.K_SPACE and self.status != 'jumping': #Jump
            self.status = 'jumping'
            self.vertical_vel = -JUMP_STRENGTH

    def apply_gravity(self):
        if self.rect.bottom < 600:
            self.vertical_vel += GRAVITY_STRENGTH
            self.rect.centery += self.vertical_vel
        else:
            self.status = 'standing'
            self.rect.bottom = 600
            self.vertical_vel = 0

