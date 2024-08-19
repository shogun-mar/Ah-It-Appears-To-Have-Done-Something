import pygame as pg
from settings import *
from logic.physicsEntities import PhysicsEntity
from logic.states.gameState import GameState

def handle_start_menu_events(game, event):
    """Function that handles events for the start menu game state"""
    
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            game.generic_pause_event_handler()
            
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if game.start_button_rect.collidepoint(event.pos):
            create_start_physics_entity(game)
        elif game.level_button_rect.collidepoint(event.pos):
            create_level_physics_entity(game) 

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

    screen.blit(game.start_menu_ground_surf, game.start_menu_ground_rect) #Draw the ground
    screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
    screen.blit(game.player.sprite, game.player.rect) #Draw the player
    
    screen.blit(game.logo_surf, game.logo_rect) #Draw the logo
    screen.blit(game.level_button_surf, game.level_button_rect) #Draw the level button
    screen.blit(game.start_button_surf, game.start_button_rect) #Draw the start button
    [screen.blit(entity.sprite, entity.rect) for entity in game.entities] #Draw all the entities

    
    screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor

    #pg.draw.line(screen, 'red', (game.player.gravity_x_coord, 0), (game.player.gravity_x_coord, SCREEN_HEIGHT), 2) #Draw the gravity line
    #pg.draw.rect(screen, 'green', game.player.rect, 2)  # Draw the player's rect with a red outline

def create_start_physics_entity(game):
    """Function that creates a physics entity at the player's position"""
    game.entities.append(PhysicsEntity(game = game, mass = 5, sprite = game.start_button_surf, \
                                        rect = game.start_button_rect.copy()))

def create_level_physics_entity(game):
    """Function that creates a physics entity at the level button's position"""
    game.entities.append(PhysicsEntity(game = game, mass = 5, sprite = game.level_button_surf, \
                                        rect = game.level_button_rect.copy()))