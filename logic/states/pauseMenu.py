from settings import *

def handle_pause_menu_events(game, event):
    """Function that handles events for the pause menu game state"""
    if event.type == pg.KEYDOWN and event.key == PAUSE_KEY:
        game.game_state = game.previous_game_state

def update_pause_menu(game):
    """Function that updates the pause menu game state"""
    pass

def render_pause_menu(game):
    """Function that renders the pause menu game state"""
    screen = game.screen #Rename screen to make draw calls easier to read
    screen.blit(game.pause_menu_background, (0, 0)) #Draw the pause menu background
    screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor
