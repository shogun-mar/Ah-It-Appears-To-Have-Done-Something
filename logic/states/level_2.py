import ctypes, time
from ctypes import wintypes
from threading import Thread
from settings import PAUSE_KEY, pg #Import the pause key and the pygame module


# Define necessary constants
_MONITOR_DEFAULTTONEAREST = 2

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
def get_monitor_brightness(hwnd):
    hmonitor = user32.MonitorFromWindow(hwnd, _MONITOR_DEFAULTTONEAREST)
    
    # Get number of physical monitors
    num_monitors = wintypes.DWORD()
    dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hmonitor, ctypes.byref(num_monitors))
    
    # Get physical monitor handles
    physical_monitors = (PHYSICAL_MONITOR * num_monitors.value)()
    dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, num_monitors.value, physical_monitors)
    
    # Get brightness of the first monitor
    min_brightness = wintypes.DWORD()
    current_brightness = wintypes.DWORD()
    max_brightness = wintypes.DWORD()
    dxva2.GetMonitorBrightness(physical_monitors[0].hPhysicalMonitor, ctypes.byref(min_brightness), ctypes.byref(current_brightness), ctypes.byref(max_brightness))
    
    # Clean up
    dxva2.DestroyPhysicalMonitor(physical_monitors[0].hPhysicalMonitor)
    
    return current_brightness.value

# Function to set monitor brightness
def set_monitor_brightness(hwnd, brightness):
    hmonitor = user32.MonitorFromWindow(hwnd, _MONITOR_DEFAULTTONEAREST)
    
    # Get number of physical monitors
    num_monitors = wintypes.DWORD()
    dxva2.GetNumberOfPhysicalMonitorsFromHMONITOR(hmonitor, ctypes.byref(num_monitors))
    
    # Get physical monitor handles
    physical_monitors = (PHYSICAL_MONITOR * num_monitors.value)()
    dxva2.GetPhysicalMonitorsFromHMONITOR(hmonitor, num_monitors.value, physical_monitors)
    
    # Set brightness of the first monitor
    dxva2.SetMonitorBrightness(physical_monitors[0].hPhysicalMonitor, brightness)
    
    # Clean up
    dxva2.DestroyPhysicalMonitor(physical_monitors[0].hPhysicalMonitor)

# Function to monitor brightness changes
def monitor_brightness_changes(callback, interval=7):
    hwnd = user32.GetForegroundWindow()  # Get handle of the current window
    previous_brightness = get_monitor_brightness(hwnd)
    
    while True:
        time.sleep(interval)
        current_brightness = get_monitor_brightness(hwnd)
        if current_brightness != previous_brightness:
            callback(current_brightness)
            previous_brightness = current_brightness

# Callback function
def brightness_changed(new_brightness):
    print(f"Brightness changed to: {new_brightness}")

def handle_level_two_events(game, event):
        
    if event.type == pg.KEYDOWN:
        if event.key == PAUSE_KEY:
            game.generic_pause_event_handler()

def update_level_two(game):
    
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
    set_monitor_brightness(game.window_handle, 0) #Set the monitor brightness to 0
    update_player_mask(game, brightness=0) #Update the playter mask with a brightness of 0

    # Start monitoring brightness changes in a separate thread
    monitor_thread = Thread(target=monitor_brightness_changes, args=(brightness_changed,)) # Create a thread to monitor brightness changes
    monitor_thread.daemon = True # Make the thread a daemon so it stops when the main thread stops
    monitor_thread.start() # Start the thread

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