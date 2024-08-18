import pygame as pg
from settings import *
from logic.physicsEntities import PhysicsEntity

def handle_start_menu_events(game, event):
    """Function that handles events for the start menu game state"""
    ...

def update_start_menu(game):
    """Function that updates the start menu game state"""

    #Player
    game.player.handle_input() #Handle player input
    game.player.move() #Move the player
    game.player.update_animation() #Update the player animation

    #Environment
    [entity.move() for entity in game.entities] #Move all the entities 
    game.update_portal_animation() #Update the portal animation

def render_start_menu(game):
    """Function that renders the start menu game state"""

    screen = game.screen #Rename screen to make draw calls easier to read

    screen.blit(game.logo_surf, game.logo_rect) #Draw the logo
    screen.blit(game.start_menu_ground_surf, game.start_menu_ground_rect) #Draw the ground
    screen.blit(game.level_button_surf, game.level_button_rect) #Draw the level button
    screen.blit(game.start_button_surf, game.start_button_rect) #Draw the start button
    [screen.blit(entity.sprite, entity.rect) for entity in game.entities] #Draw all the entities
    screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
    screen.blit(game.player.sprite, game.player.rect) #Draw the player
    
    screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor