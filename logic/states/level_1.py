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

    player = game.player

    if game.last_window_position is not None:
        x_diff = (game.current_window_position[0] - game.last_window_position[0])
        y_diff = (game.current_window_position[1] - game.last_window_position[1])


    if game.level_one_grav_controller_y <= game.player.rect.centery - y_diff <= game.level_one_grav_controller_y + 128:  #If the player is in the y range of the gravity controller

        print("Player is in the y range of the gravity controller")

        #Reserve for loop in order to hopefully reduce iterations because its more probable that the point we are searching is farther away from the player
        for x_value in range(abs(x_diff), 0, -1): # (e.g if x_diff is 3, the range will be 3, 2, 1)

            #If the difference is positive the window has moved to the right and we want to move the player to the left and/or down,
            # if the difference is negative the window has moved to the left and we want to move the player to the right and/or up
            if x_diff > 0: current_point = (player.rect.centerx - x_value, player.rect.centery - y_diff) 
            else:  current_point = (player.rect.centerx + x_value, player.rect.centery + y_diff)

            for grav_controller in game.level_one_grav_controllers:
                if grav_controller.rect.collidepoint(current_point) and grav_controller.can_be_actived():
                    exec(grav_controller.action)
                    player.rect.center = (player.rect.centerx - x_diff, player.rect.centery - y_diff)
                    player.velocity[0] = 3 if x_diff > 0 else -3
                    return

    else:
        player.rect.center = (player.rect.centerx - x_diff, player.rect.centery - y_diff)




        # does_surpass_controller = False #Boolean to keep track of whether the new player position would surpass a gravity controller (because the player could be moved in a way that it would be pass a gravity controller but due to the window movement it would not be able to activate it)

        # for x in range(abs(adj_x_diff), -1, -1): #Reserve for loop in order to hopefully reduce iterations because its more probable that the point we are searching is farther away from the player
        #     if adj_x_diff > 0:current_point = (game.player.rect.midright[0] + x, game.player.rect.midright[1] - adj_y_diff)
        #     else:  current_point = (game.player.rect.midleft[0] - x, game.player.rect.midleft[1] - adj_y_diff)

        #     if game.level_one_grav_controller_y < current_point[1] < game.level_one_grav_controller_y + 128:
        #         for grav_controller in game.level_one_grav_controllers:
        #             if grav_controller.rect.collidepoint(current_point) and grav_controller.can_be_actived():
        #                 does_surpass_controller = True
        #                 exec(grav_controller.action)
        #                 break

        #     if does_surpass_controller: break
        #     else: game.player.rect.midleft = (game.player.rect.midleft[0] - adj_x_diff, game.player.rect.midleft[1] - adj_y_diff) #Minus because i want the player to move in the opposite direction of the window

        # print(f"Player position: {game.player.rect.midleft}")