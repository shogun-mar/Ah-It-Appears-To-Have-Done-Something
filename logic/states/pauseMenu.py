from logic.states.gameState import GameState
from settings import *

def handle_pause_menu_events(game, event):
    """Function that handles events for the pause menu game state"""
    if event.type == pg.KEYDOWN and event.key == PAUSE_KEY:
        game.game_state = game.previous_game_state

def update_pause_menu(game):
    """Function that updates the pause menu game state"""
    match game.previous_game_state:
        case GameState.START_MENU | GameState.LEVEL_1:
            game.update_portal_animation() #Update the portal animation
            game.player.update_animation() #Update the player animation

def render_pause_menu(game):
    """Function that renders the pause menu game state"""
    darkned_surf = pg.Surface(LEVEL_RESOLUTIONS[game.current_level_num]) #Create a surface to darken the screen
    darkned_surf.set_alpha(PAUSE_MENU_BACKGROUND_ALPHA) #Fill the surface with black

    screen = game.screen #Rename screen to make draw calls easier to read
    
    match game.previous_game_state:
        case GameState.START_MENU:
            #render_start_menu(game) #Could also do this but it would also draw the cursor (a fix could be moving the cursor drawing to the main render function in game.py)
            screen.blit(game.logo_surf, game.logo_rect) #Draw the logo
            screen.blit(game.start_menu_ground_surf, game.start_menu_ground_rect) #Draw the ground
            screen.blit(game.level_button_surf, game.level_button_rect) #Draw the level button
            screen.blit(game.start_button_surf, game.start_button_rect) #Draw the start button
            [screen.blit(entity.sprite, entity.rect) for entity in game.entities] #Draw all the entities

            screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
            screen.blit(game.player.sprite, game.player.rect) #Draw the player

        case GameState.LEVEL_1:    
            screen.blit(game.level_one_ground_surf, game.level_one_ground_rect) #Draw the ground
            screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
            screen.blit(game.player.sprite, game.player.rect) #Draw the player

        case GameState.LEVEL_2:
            screen.blit(game.level_two_ground_surf, game.level_two_ground_rect) #Draw the ground
            screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
            screen.blit(game.player.sprite, game.player.rect) #Draw the player

    screen.blit(darkned_surf, (0, 0)) #Darken the screen
    if game.should_draw_cursor: screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor
