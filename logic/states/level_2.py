import pygame as pg
import ctypes, time
from ctypes import wintypes
from settings import *

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

def init_level_two(game):
    game.player.status = 'asleep' #Set the player status to asleep in level 2
    game.player.controls_enabled = False #Disable player controls
    set_brightness(0) #Set the monitor brightness to 0
    update_player_mask(game, brightness=0) #Update the playter mask with a brightness of 0

def update_player_mask(game, brightness):
    
    relative_color =  # Calculate the relative color based on the brightness (RGBA)

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

def get_monitor_handles():
    # Define necessary structures and constants
    class PHYSICAL_MONITOR(ctypes.Structure):
        _fields_ = [("hPhysicalMonitor", wintypes.HANDLE),
                    ("szPhysicalMonitorDescription", wintypes.WCHAR * 128)]

    # Load necessary DLLs
    user32 = ctypes.windll.user32
    dxva2 = ctypes.windll.dxva2

    # Get the number of monitors
    monitor_enum_proc = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HMONITOR, wintypes.HDC, ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)
    monitors = []

    def callback(hmonitor, hdc, lprect, lparam):
        monitors.append(hmonitor)
        return 1

    user32.EnumDisplayMonitors(None, None, monitor_enum_proc(callback), 0)

    physical_monitors = []

    for hmonitor in monitors:
        monitor_count = wintypes.DWORD()
        if not dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hmonitor, ctypes.byref(monitor_count)):
            continue

        physical_monitor_array = (PHYSICAL_MONITOR * monitor_count.value)()
        if not dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, monitor_count, physical_monitor_array):
            continue

        for physical_monitor in physical_monitor_array:
            physical_monitors.append(physical_monitor.hPhysicalMonitor)

    return physical_monitors

def set_brightness(brightness):
    dxva2 = ctypes.windll.dxva2
    monitors = get_monitor_handles()

    for monitor in monitors:
        dxva2.SetMonitorBrightness(monitor, brightness)
        dxva2.DestroyPhysicalMonitor(monitor)

def get_brightness_levels():

    # Define necessary structures and constants
    class PHYSICAL_MONITOR(ctypes.Structure):
        _fields_ = [("hPhysicalMonitor", wintypes.HANDLE),
                    ("szPhysicalMonitorDescription", wintypes.WCHAR * 128)]

    # Load necessary DLLs
    user32 = ctypes.windll.user32
    dxva2 = ctypes.windll.dxva2

    # Get the number of monitors
    monitor_enum_proc = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.HMONITOR, wintypes.HDC, ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)
    monitors = []

    def callback(hmonitor, hdc, lprect, lparam):
        monitors.append(hmonitor)
        return 1

    user32.EnumDisplayMonitors(None, None, monitor_enum_proc(callback), 0)

    brightness_levels = []

    for hmonitor in monitors:
        monitor_count = wintypes.DWORD()
        if not dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hmonitor, ctypes.byref(monitor_count)):
            continue

        physical_monitors = (PHYSICAL_MONITOR * monitor_count.value)()
        if not dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, monitor_count, physical_monitors):
            continue

        for physical_monitor in physical_monitors:
            min_brightness = wintypes.DWORD()
            current_brightness = wintypes.DWORD()
            max_brightness = wintypes.DWORD()
            if dxva2.GetMonitorBrightness(physical_monitor.hPhysicalMonitor, ctypes.byref(min_brightness), ctypes.byref(current_brightness), ctypes.byref(max_brightness)):
                brightness_levels.append(current_brightness.value)
            dxva2.DestroyPhysicalMonitor(physical_monitor.hPhysicalMonitor)

    return brightness_levels

def wake_up_player(player):
    player.status = 'standing' #Set the player status to standing
    player.controls_enabled = True #Enable player controls