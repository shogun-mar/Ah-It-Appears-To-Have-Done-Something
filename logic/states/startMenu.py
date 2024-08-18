import pygame as pg
from settings import *
from logic.physicsEntities import PhysicsEntity

def handle_start_menu_events(game, event):
    """Function that handles events for the start menu game state"""
    global mouse_physics_entity

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if game.start_button_rect.collidepoint(pg.mouse.get_pos()):
            game.entities.append(PhysicsEntity(game=game, mass=1, sprite = game.cursor_surf, rect = pg.Rect(pg.mouse.get_pos(), (game.cursor_surf.get_width(), game.cursor_surf.get_height()))))
            
def update_start_menu(game):
    """Function that updates the start menu game state"""

    game.player.handle_input() #Handle player input
    game.player.move() #Move the player
    game.player.update_animation() #Update the player animation

    [entity.move() for entity in game.entities] #Move all the entities 

def render_start_menu(game):
    """Function that renders the start menu game state"""

    screen = game.screen #Rename screen to make draw calls easier to read

    screen.blit(game.logo_surf, game.logo_rect) #Draw the logo
    screen.blit(game.start_menu_ground_surf, game.start_menu_ground_rect) #Draw the ground
    screen.blit(game.level_button_surf, game.level_button_rect) #Draw the level button
    screen.blit(game.start_button_surf, game.start_button_rect) #Draw the start button
    screen.blit(game.player.sprite, game.player.rect) #Draw the player
    [screen.blit(entity.sprite, entity.rect) for entity in game.entities] #Draw all the entities
    screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor
    pg.draw.line(screen, 'red', (game.player.collision_line_x_coord, 0), (game.player.collision_line_x_coord, SCREEN_HEIGHT), 2) #Draw collision line