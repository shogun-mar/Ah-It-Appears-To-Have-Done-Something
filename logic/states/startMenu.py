import pygame as pg
from settings import *

logo_surf = logo_rect = None
start_button_surf = start_button_rect = None
ground_surf = ground_rect = None

def init_start_menu():
    global logo_surf, logo_rect, \
           start_button_surf, start_button_rect, \
           ground_surf, ground_rect

    logo_font = pg.font.Font("graphics/font/silver.ttf", 58)

    logo_surf = logo_font.render("Ah It Appears To Have Done Something", True, 'black')
    logo_rect = logo_surf.get_rect(midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

    start_button_surf = pg.image.load("graphics/buttons/start menu/start.png")
    start_button_rect = start_button_surf.get_rect(midtop = (SCREEN_WIDTH // 2, logo_rect.midbottom[1] + 50))

    ground_surf = pg.image.load("graphics/assets/start menu/ground.png").convert_alpha()
    ground_rect = ground_surf.get_rect(bottomleft = (0, SCREEN_HEIGHT))

def handle_start_menu_events(game, event):
    pass   

def update_start_menu(game):
    pressed_keys = pg.key.get_pressed()
    
    #Player
    game.player.move(pressed_keys) #Move the player (would make more sense in the handle events function but that wouldn't allow for continuos movement)
    game.player.update_animation() #Update the player's animation

def render_start_menu(game):
    screen = game.screen #Rename screen to make draw calls easier to read

    screen.fill('white')
    screen.blit(logo_surf, logo_rect) #Draw the logo
    screen.blit(start_button_surf, start_button_rect) #Draw the start button
    screen.blit(ground_surf, ground_rect) #Draw the ground
    screen.blit(game.player.sprite, game.player.rect) #Draw the player
