import pygame as pg
from settings import *
from logic.physicsEntities import PhysicsEntity

current_broken_start_index = -1  #Index of the current broken start button (-1 so that the first call to update_start_menu will change it to 0)
mouse_physics_entities = []

def handle_start_menu_events(game, event):
    global mouse_physics_entity

    #game.player.handle_input_event_based(event) #Handle player input

    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
        if game.start_button_rect.collidepoint(pg.mouse.get_pos()):
            game.entities.append(PhysicsEntity(game=game, mass=1, sprite = game.cursor_surf, rect = pg.Rect(pg.mouse.get_pos(), (game.cursor_surf.get_width(), game.cursor_surf.get_height()))))
            
def update_start_menu(game):

    game.player.handle_input_tuple_based() #Handle player input
    game.player.move() #Move the player
    game.player.update_animation() #Update the player animation

    [entity.move() for entity in game.entities] #Move all the entities 

def render_start_menu(game):
    screen = game.screen #Rename screen to make draw calls easier to read

    screen.fill('white')
    screen.blit(game.logo_surf, game.logo_rect) #Draw the logo
    screen.blit(game.start_menu_ground_surf, game.start_menu_ground_rect) #Draw the ground
    screen.blit(game.level_button_surf, game.level_button_rect) #Draw the level button
    screen.blit(game.start_button_surf, game.start_button_rect) #Draw the start button
    screen.blit(game.player.sprite, game.player.rect) #Draw the player
    [screen.blit(entity.sprite, entity.rect) for entity in game.entities] #Draw all the entities
    screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor
    pg.draw.line(screen, 'red', (game.player.collision_line_x_coord, 0), (game.player.collision_line_x_coord, SCREEN_HEIGHT), 2) #Draw collision line