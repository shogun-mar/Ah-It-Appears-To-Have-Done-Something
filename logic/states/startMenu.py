import pygame as pg
from settings import *

beginning_of_jump_charge = 0  #Time when the player started charging the jump
current_broken_start_index = -1  #Index of the current broken start button (-1 so that the first call to update_start_menu will change it to 0)

def handle_start_menu_events(game, event):
    global beginning_of_jump_charge

    if event.type == pg.KEYDOWN:
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            game.player.movement[0] = True
        elif event.key == pg.K_d or event.key == pg.K_RIGHT:
            game.player.movement[1] = True
        elif event.key == pg.K_SPACE and game.player.velocity[1] == BASE_GRAVITY_PULL: #If the user presses space and the player is on the ground
            beginning_of_jump_charge = pg.time.get_ticks() #Set the time of when the user started charging the jump

    elif event.type == pg.KEYUP:
        if event.key == pg.K_a or event.key == pg.K_LEFT:
            game.player.movement[0] = False
        elif event.key == pg.K_d or event.key == pg.K_RIGHT:
            game.player.movement[1] = False
        elif event.key == pg.K_SPACE and game.player.velocity[1] == BASE_GRAVITY_PULL:
            #If the user releases the space key, calculate for how much time the player has been charging the jump
            jump_charge_time = pg.time.get_ticks() - beginning_of_jump_charge
            game.player.velocity[1] = min(BASE_JUMP_SPEED - (jump_charge_time // 1000 * 10), MAX_JUMP_SPEED)
            #print(jump_charge_time)
            #print(f"Initial jump velocity: {game.player.velocity[1]}")

def update_start_menu(game):
    global current_broken_start_index
    
    # Player
    game.player.move() #Move the player
    game.player.update_animation() #Update the player's animation

    # Environment
    if game.player.rect.colliderect(game.start_button_rect):
        print("Collided with start button")
        current_broken_start_index += 1
        if current_broken_start_index == 3:
            print("Starting game")
        else:
            game.start_button_surf = game.broken_start_button_surfs[current_broken_start_index]

def render_start_menu(game):
    screen = game.screen #Rename screen to make draw calls easier to read

    screen.fill('white')
    screen.blit(game.logo_surf, game.logo_rect) #Draw the logo
    screen.blit(game.start_menu_ground_surf, game.start_menu_ground_rect) #Draw the ground
    screen.blit(game.start_button_surf, game.start_button_rect) #Draw the start button
    screen.blit(game.player.sprite, game.player.rect) #Draw the player