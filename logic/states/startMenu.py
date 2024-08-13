import pygame as pg
from settings import *

def handle_start_menu_events(game, event):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            game.player.movement[0] = True
        elif event.key == pg.K_d or event.key == pg.K_RIGHT:
            game.player.movement[1] = True
        elif event.key == pg.K_SPACE and game.player.velocity[1] == BASE_GRAVITY_PULL: #If the user presses space and the player is on the ground
            game.player.velocity[1] = MAX_JUMP_SPEED #Set the player vertical velocity to the jump strength (negative value because in pygame up is negative)

        game.player.switch_animation(event) #Switch the player's animation
    
    elif event.type == pg.KEYUP:
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            game.player.movement[0] = False
        elif event.key == pg.K_d or event.key == pg.K_RIGHT:
            game.player.movement[1] = False

        game.player.switch_animation(event) #Switch the player's animation
    
def update_start_menu(game):
    #Player
    game.player.move() #Move the player
    game.player.update_animation() #Update the player's animation

def render_start_menu(game):
    screen = game.screen #Rename screen to make draw calls easier to read

    screen.fill('white')
    screen.blit(game.logo_surf, game.logo_rect) #Draw the logo
    screen.blit(game.start_menu_ground_surf, game.start_menu_ground_rect) #Draw the ground
    screen.blit(game.start_button_surf, game.start_button_rect) #Draw the start button
    screen.blit(game.player.sprite, game.player.rect) #Draw the player
