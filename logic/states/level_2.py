import ctypes, time
from ctypes import wintypes
from threading import Thread, Event
from logic.states.gameState import GameState
from settings import PAUSE_KEY, BRIGHTNESS_CONTROL_INTERVAL, pg

windows_api_exception = False
monitoring_brightness_event = Event()  # Event to control the brightness monitoring thread

# Define necessary structures
class MONITORINFOEXW(ctypes.Structure):
    _fields_ = [
        ("cbSize", wintypes.DWORD),
        ("rcMonitor", wintypes.RECT),
        ("rcWork", wintypes.RECT),
        ("dwFlags", wintypes.DWORD),
        ("szDevice", wintypes.WCHAR * 32)
    ]

class PHYSICAL_MONITOR(ctypes.Structure):
    _fields_ = [("hPhysicalMonitor", wintypes.HANDLE),
                ("szPhysicalMonitorDescription", wintypes.WCHAR * 128)]

# Load necessary DLLs
user32 = ctypes.WinDLL('user32')
dxva2 = ctypes.WinDLL('dxva2')

# Define function prototypes
user32.MonitorFromWindow.restype = wintypes.HMONITOR
user32.MonitorFromWindow.argtypes = [wintypes.HWND, wintypes.DWORD]

user32.GetMonitorInfoW.restype = wintypes.BOOL
user32.GetMonitorInfoW.argtypes = [wintypes.HMONITOR, ctypes.POINTER(MONITORINFOEXW)]

dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR.restype = wintypes.BOOL
dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR.argtypes = [wintypes.HMONITOR, ctypes.POINTER(wintypes.DWORD)]

dxva2.GetPhysicalMonitorsFromHMONITOR.restype = wintypes.BOOL
dxva2.GetPhysicalMonitorsFromHMONITOR.argtypes = [wintypes.HMONITOR, wintypes.DWORD, ctypes.POINTER(PHYSICAL_MONITOR)]

dxva2.GetMonitorBrightness.restype = wintypes.BOOL
dxva2.GetMonitorBrightness.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(wintypes.DWORD)]

dxva2.SetMonitorBrightness.restype = wintypes.BOOL
dxva2.SetMonitorBrightness.argtypes = [wintypes.HANDLE, wintypes.DWORD]

# Function to get monitor brightness
def get_monitor_brightness(hmonitor):
    global windows_api_exception

    try:
        # Get number of physical monitors
        num_monitors = wintypes.DWORD()
        if not dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hmonitor, ctypes.byref(num_monitors)):
            raise ctypes.WinError()

        # Get physical monitor handles
        physical_monitors = (PHYSICAL_MONITOR * num_monitors.value)()
        if not dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, num_monitors.value, physical_monitors):
            raise ctypes.WinError()

        # Get brightness of the first monitor
        min_brightness = wintypes.DWORD()
        current_brightness = wintypes.DWORD()
        max_brightness = wintypes.DWORD()
        if not dxva2.GetMonitorBrightness(physical_monitors[0].hPhysicalMonitor, ctypes.byref(min_brightness), ctypes.byref(current_brightness), ctypes.byref(max_brightness)):
            raise ctypes.WinError()

        return current_brightness.value
    except Exception as e:
        print(f"An error occurred: {e}")
        windows_api_exception = True #Flip the flag that indicates an exception occurred in the Windows API
    finally:
        # Clean up
        if 'physical_monitors' in locals():
            dxva2.DestroyPhysicalMonitor(physical_monitors[0].hPhysicalMonitor)
        return

# Function to set monitor brightness
def set_monitor_brightness(hmonitor, brightness):
    global windows_api_exception

    try:
        # Get number of physical monitors
        num_monitors = wintypes.DWORD()
        if not dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hmonitor, ctypes.byref(num_monitors)):
            raise ctypes.WinError()

        # Get physical monitor handles
        physical_monitors = (PHYSICAL_MONITOR * num_monitors.value)()
        if not dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, num_monitors.value, physical_monitors):
            raise ctypes.WinError()

        # Set brightness of the first monitor
        if not dxva2.SetMonitorBrightness(physical_monitors[0].hPhysicalMonitor, brightness):
            raise ctypes.WinError()
    except Exception as e:
        print(f"An error occurred: {e}")
        windows_api_exception = True #Flip the flag that indicates an exception occurred in the Windows API
    finally:
        # Clean up
        if 'physical_monitors' in locals():
            dxva2.DestroyPhysicalMonitor(physical_monitors[0].hPhysicalMonitor)

# Function to monitor brightness changes
def monitor_brightness_changes(callback, game_instance, interval=BRIGHTNESS_CONTROL_INTERVAL):
    global monitoring_brightness_event
    hmonitor = game_instance.hardware_monitor # Get the hardware monitor handle
    previous_brightness = get_monitor_brightness(hmonitor) # Get the initial brightness
    
    while not monitoring_brightness_event.is_set():

        time.sleep(interval) # Wait for the interval
        current_brightness = get_monitor_brightness(hmonitor) # Get the current brightness
        if current_brightness != previous_brightness: # If the brightness has changed

            if current_brightness - previous_brightness >= 50: # If the brightness has increased by 50 or more
                callback(game_instance, current_brightness) # Call the callback function

            previous_brightness = current_brightness # Update the previous brightness

# Callback function
def brightness_changed(game_instance, new_brightness):
    global monitoring_brightness_event
    game_instance.player.wake_up() #Wake up the player
    monitoring_brightness_event.set()  # Signal the brightness monitoring thread to stop

#Pause event handler
def pause_event_handler(game):
    if not game.player.is_in_air and game.player.status != 'asleep': #If the player is not in the air and not asleep
        game.player.status = 'standing'
    game.pause_sound.play() #Play the pause sound
    game.paused_game_state = game.game_state

    game.game_state = GameState.PAUSE_MENU
    pg.mixer.music.pause() #Pause the music

def handle_level_two_events(game, event):
        
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            pause_event_handler(game)

def update_level_two(game):
    
    player = game.player #Rename player to make code easier to read

    #Player
    player.handle_input() #Handle player input
    player.move() #Move the player
    player.update_animation() #Update the player animation

    #Environment
    game.update_portal_animation() #Update the portal animation
    game.level_two_blob.update_animation() #Update the jump pad animation
    [effect.update_animation() for effect in game.effects] #Update all the effects
    if player.rect.colliderect(game.level_two_blob.rect):
        exec(game.level_two_blob.action)

    #Exception handling
    if windows_api_exception and game.player.status == 'asleep': #If an exception occurred in the Windows API adn the player is asleep
        game.player.wake_up() #Wake up the player

def render_level_two(game):
    
    screen = game.screen
    
    screen.blit(game.level_two_ground_surf, game.level_two_ground_rect) #Draw the ground
    [screen.blit(effect.sprite, effect.rect) for effect in game.effects] #Draw all the effects
    screen.blit(game.player.sprite, game.player.rect) #Draw the player
    screen.blit(game.current_portal_sprite, game.portal_rect) #Draw the end of level portal
    screen.blit(game.level_two_blob.sprite, game.level_two_blob.rect) #Draw the jump pad

    if game.should_draw_cursor and game.player.status != 'asleep': screen.blit(game.cursor_surf, pg.mouse.get_pos()) #Draw the cursor
    if game.player.status == 'asleep': screen.blit(game.level_two_env_mask, (0, 0)) #Draw the environment mask

def init_level_two(game):
    global monitoring_brightness_event
    monitoring_brightness_event.clear()  # Reset the event when initializing the level
    game.player.status = 'asleep' #Set the player status to asleep in level 2
    game.player.controls_enabled = False #Disable player controls
    game.should_draw_cursor = False #Disable cursor drawing
    set_monitor_brightness(game.hardware_monitor, 0) #Set the monitor brightness to 0

    # Start monitoring brightness changes in a separate thread
    monitor_thread = Thread(target=monitor_brightness_changes, args=(brightness_changed, game)) # Create a thread to monitor brightness changes
    monitor_thread.daemon = True # Make the thread a daemon so it stops when the main thread stops
    monitor_thread.start() # Start the thread