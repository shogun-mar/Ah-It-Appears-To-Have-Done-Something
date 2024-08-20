import pygame as pg
from settings import *

previous_player_coords = INITIAL_COORDS_PLAYER[1] #The previous coordinates of the player

def handle_level_two_events(game, event):
        
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            game.generic_pause_event_handler()

def update_level_two(game):
    global previous_player_coords
    
    player = game.player #Rename player to make code easier to read

    #Player
    player.handle_input() #Handle player input
    player.move() #Move the player
    if player.rect.topleft != previous_player_coords: 
        previous_player_coords = player.rect.topleft #Update the previous player coordinates
        update_player_mask(game)

    player.update_animation() #Update the player animation

    #Environment
    game.update_portal_animation() #Update the portal animation

def render_level_two(game):
    
    screen = game.screen
    
    screen.blit(game.level_two_ground_surf, game.level_two_ground_rect) #Draw the ground
    screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
    screen.blit(game.player.sprite, game.player.rect) #Draw the player

    screen.blit(game.level_two_env_mask, (0, 0)) #Draw the environment mask

    if game.should_draw_cursor: screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor


def update_player_mask(game): #TODO: Fix this function to work properly now it fill the screen with black
    cutout_origin_x, cutout_origin_y = game.player.rect.topleft

    game.level_two_env_mask.fill((0, 0, 0)) #Reset the mask

    for y in range(cutout_origin_y, cutout_origin_y + 64):
        for x in range(cutout_origin_x, cutout_origin_x + 32):
            game.level_two_env_mask.set_at((x, y), (0, 0, 0, 0))  # Set pixel to fully transparent

    game.level_two_env_mask.blit(game.level_two_player_mask, (cutout_origin_x, cutout_origin_y)) #Blit the player mask onto the final mask