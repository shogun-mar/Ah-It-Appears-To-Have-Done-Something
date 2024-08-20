from logic.states.gameState import GameState
from settings import *

def handle_level_one_events(game, event):
    """Function that handles events for the level one game state"""
    
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            game.generic_pause_event_handler()

    elif event.type == pg.WINDOWMOVED:
        game.last_window_position = game.current_window_position
        game.current_window_position = game.get_window_position()
        if game.player.should_float and game.player.controls_enabled == False: move_player_relative_to_window(game) #Moves the player of a relative amount of the difference between the last and current window position

def update_level_one(game):

    player = game.player

    #Player
    player.handle_input() #Handle player input
    player.move() #Move the player
    player.update_animation() #Update the player animation
    
    #Environment
    game.update_portal_animation() #Update the portal animation
    [grav_controller.update_animation() for grav_controller in game.level_one_grav_controllers] #Update the gravity controllers animations
    for grav_controller in game.level_one_grav_controllers: #Check for collision between the gravity controllers and the player
        if player.rect.colliderect(grav_controller.rect) and grav_controller.can_be_actived():
            exec(grav_controller.action)

def render_level_one(game):
    screen = game.screen

    screen.blit(game.level_one_ground_surf, game.level_one_ground_rect) #Draw the ground
    [screen.blit(grav_controller.sprite, grav_controller.rect) for grav_controller in game.level_one_grav_controllers] #Draw the gravity controllers
    screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
    screen.blit(game.player.sprite, game.player.rect) #Draw the player

def move_player_relative_to_window(game):
    """Function that moves the player of a relative amount of the difference between the last and current window position"""

    if game.last_window_position is not None:
        adj_x_diff = (game.current_window_position[0] - game.last_window_position[0])
        adj_y_diff = (game.current_window_position[1] - game.last_window_position[1])

        print(f"Current topleft pos: {game.player.rect.topleft} and moving to {game.player.rect.topleft[0] + adj_x_diff, game.player.rect.topleft[1] + adj_y_diff}")
        game.player.rect.topleft = (game.player.rect.topleft[0] + adj_x_diff, game.player.rect.topleft[1])
        #game.player.rect.topleft = (game.player.rect.topleft[0] + adj_x_diff, game.player.rect.topleft[1] + adj_y_diff)