from logic.states.gameState import GameState
from settings import *

def handle_level_one_events(game, event):
    """Function that handles events for the level one game state"""
    
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            game.generic_pause_event_handler()

def update_level_one(game):
    
    #Player
    game.player.handle_input() #Handle player input
    game.player.move() #Move the player
    game.player.update_animation() #Update the player animation

    #Environment
    game.update_portal_animation() #Update the portal animation

def render_level_one(game):
    screen = game.screen

    screen.blit(game.level_one_ground_surf, game.level_one_ground_rect) #Draw the ground
    screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
    screen.blit(game.player.sprite, game.player.rect) #Draw the player