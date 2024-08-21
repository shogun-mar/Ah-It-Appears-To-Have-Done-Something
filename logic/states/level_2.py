import pygame as pg
import ctypes
from ctypes import wintypes
from settings import *

import ctypes
from ctypes import wintypes

# Constants
dxva2 = ctypes.windll.dxva2

def get_brightness_value(game):
    hmonitor = game.get_monitor_handle()
    current_brightness = wintypes.DWORD()

    if dxva2.GetMonitorBrightness(hmonitor, ctypes.byref(current_brightness)):
        return current_brightness.value
    else:
        raise ctypes.WinError(ctypes.get_last_error())

def set_brightness(game, level):
    hmonitor = game.get_monitor_handle()
    if not dxva2.SetMonitorBrightness(hmonitor, wintypes.DWORD(level)):
        raise ctypes.WinError(ctypes.get_last_error())

def monitor_brightness(game):
    global previous_brightness

    if previous_brightness is None:
        previous_brightness = get_brightness_value(game)

    current_brightness = get_brightness_value(game)

    if previous_brightness != current_brightness:
        previous_brightness = current_brightness
        print(f"Brightness levels changed: {current_brightness} from {previous_brightness}")
        #update_player_mask(game, brightness=current_brightness)

# Brightness controls variables
previous_brightness = None
brightness_monitor_delay = 5

def handle_level_two_events(game, event):
        
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            game.generic_pause_event_handler()
        if event.key == pg.K_0:
            set_brightness(100)

def update_level_two(game):
    global brightness_monitor_delay
    
    player = game.player #Rename player to make code easier to read

    #Player
    player.handle_input() #Handle player input
    player.move() #Move the player
    player.update_animation() #Update the player animation

    #Environment
    game.update_portal_animation() #Update the portal animation
    brightness_monitor_delay -= 1 #Decrease the brightness monitor delay
    if brightness_monitor_delay == 0:
        brightness_monitor_delay = 10
        monitor_brightness(game) #Update the monitor brightness

def render_level_two(game):
    
    screen = game.screen
    
    screen.blit(game.level_two_ground_surf, game.level_two_ground_rect) #Draw the ground
    screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
    screen.blit(game.player.sprite, game.player.rect) #Draw the player

    screen.blit(game.level_two_env_mask, (0, 0)) #Draw the environment mask

    if game.should_draw_cursor: screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor

def init_level_two(game):
    game.player.status = 'asleep' #Set the player status to asleep in level 2
    game.player.controls_enabled = False #Disable player controls
    try:
        set_brightness(0)  # Set the monitor brightness to 0
    except Exception as e:
        print(f"Failed to set brightness: {e}")
    update_player_mask(game, brightness=0) #Update the playter mask with a brightness of 0

def update_player_mask(game, brightness):
    
    alpha_cannel = interpolate_alpha(brightness)
    relative_color = (0, 0, 0, alpha_cannel)  # Calculate the relative color based on the brightness (RGBA)

    # Lock the surface to modify pixel data
    game.level_two_env_mask.lock()

    game.level_two_env_mask.fill(relative_color)  # Fill the mask with black

    cutout_origin_x: int = game.player.rect.centerx - 32
    cutout_origin_y: int = game.player.rect.centery - 32
    width, height = 64, 64

    for x in range(cutout_origin_x, cutout_origin_x + width):
        for y in range(cutout_origin_y, cutout_origin_y + height):
            game.level_two_env_mask.set_at((x, y), (0, 0, 0, 0))  # Set pixel to fully transparent

    # Unlock the surface after modification
    game.level_two_env_mask.unlock()
    
    game.level_two_env_mask.blit(game.level_two_player_mask, (cutout_origin_x, cutout_origin_y)) #Blit the player mask onto the final mask

def interpolate_alpha(brightness):
    return int(pg.math.lerp(255, 128, brightness / 100))

def wake_up_player(player):
    player.status = 'standing' #Set the player status to standing
    player.controls_enabled = True #Enable player controls