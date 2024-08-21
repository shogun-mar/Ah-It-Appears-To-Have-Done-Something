import contextlib, ctypes
with contextlib.redirect_stdout(None): #Suppress pygame welcome message
    import pygame as pg
del contextlib
from logic.states.gameState import GameState
from logic.states.startMenu import handle_start_menu_events, update_start_menu, render_start_menu
from logic.states.pauseMenu import handle_pause_menu_events, update_pause_menu, render_pause_menu
from logic.states.level_1 import handle_level_one_events, update_level_one, render_level_one, init_level_one
from logic.states.level_2 import handle_level_two_events, update_level_two, render_level_two, init_level_two, set_brightness
from logic.physicsEntities import Player
from logic.interactibles import GravityController

from settings import *

# Constants
_MONITOR_DEFAULTTOPRIMARY = 1

class Game:
    def __init__(self):
        pg.init()

    	#Game variables
        self.game_state: GameState = GameState.LEVEL_2
        #self.game_state: GameState = GameState.START_MENU
        self.current_level_num: int = self.game_state.value
        self.should_draw_cursor: bool = True
        self.user32 = ctypes.windll.user32

        #Screen settings
        self.screen: pg.Surface = pg.display.set_mode((LEVEL_RESOLUTIONS[self.current_level_num]))
        pg.display.set_caption("Ah It Appears To Have Done Something")
        pg.display.set_icon(pg.image.load("graphics/loophole_icon.jpg"))
        pg.mouse.set_visible(False) #Hide the mouse cursor

        #Clock and time objects
        self.clock: pg.Clock = pg.time.Clock()

        #Game objects
        self.player = Player(self)
        self.player.controls_enabled = True #FOR DEBUGGING PURPOSES ONLY
        self.entities = []

        #Init assets
        self.init_assets()

        init_level_two(self) #FOR DEBUGGING PURPOSES ONLY

    def run(self):
        """Main game loop"""	
        while True:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        """Function that handles generic events for the game which are not specific to any game state and by consulting the current game state, calls the appropriate event handling function"""
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == QUCK_EXIT_KEY):
                pg.quit()
                quit()

            elif event.type == pg.WINDOWLEAVE: self.handle_mouse_exit_event()
            elif event.type == pg.WINDOWENTER: self.handle_mouse_enter_event()
            
            match self.game_state:
                case GameState.START_MENU: handle_start_menu_events(self, event)
                case GameState.LEVEL_1: handle_level_one_events(self, event)
                case GameState.LEVEL_2: handle_level_two_events(self, event)
                case GameState.PAUSE_MENU: handle_pause_menu_events(self, event)
            
    def update(self):
        """Function that updates generic values not specific to any game state and calls the appropriate update function by consulting the current game state"""

        pg.display.set_caption(f" Ah It Appears To Have Done Something - FPS: {int(self.clock.get_fps())}") #Update the window title to show the FPS
        
        match self.game_state:
            case GameState.START_MENU: update_start_menu(self)
            case GameState.LEVEL_1: update_level_one(self)
            case GameState.LEVEL_2: update_level_two(self)
            case GameState.PAUSE_MENU: update_pause_menu(self)

    def render(self):
        """Function that renders the game by calling the appropriate render function by consulting the current game state""" 

        self.screen.fill('white') #Clear the screen
        
        match self.game_state:
            case GameState.START_MENU: render_start_menu(self)
            case GameState.LEVEL_1: render_level_one(self)
            case GameState.LEVEL_2: render_level_two(self)
            case GameState.PAUSE_MENU: render_pause_menu(self)

        pg.display.flip()
        self.clock.tick(MAX_FPS) #Could also use tick_busy_loop() for more accurate timing but it would use more CPU and regular tick accuracy is fine for this game

    def init_assets(self):
        """Function that initializes all the assets for the game"""

        #Init general assets
        self.cursor_surf: pg.Surface = pg.image.load("graphics/assets/cursor.png").convert_alpha()

            #Portal animation and sprites
        self.portal_coords: list[tuple] = [(800, 500), (950, 339), (949, 139)] #Coordinates of the portal in each level (bottomright) (DO NOT CHANGE) (result may appear strange but its because the portal sprite have extra width to accomodate the particles)
        self.portal_animation_current_frame: int = 0 #Variable to keep track of the index of the current frame of the portal animation
        self.portal_animation_switching_delay: int = PORTAL_ANIMATION_SWITCHING_DELAY #Variable to keep track of when to progress the animation
        self.portal_animation: list[pg.Surface] = [pg.image.load(f"graphics/assets/portal/{i}.png").convert_alpha() for i in range(1, 7)]
        self.current_portal_sprite: pg.Surface = self.portal_animation[self.portal_animation_current_frame] #Variable to keep track of the current sprite of the portal animation
        self.portal_rect: pg.Rect = self.current_portal_sprite.get_rect(bottomright = self.portal_coords[self.current_level_num]) 

        #Init start menu
        self.logo_font: pg.Font = pg.font.Font("graphics/font/silver.ttf", 58)
        self.logo_surf: pg.Surface = self.logo_font.render("Ah It Appears To Have Done Something", True, 'black')
        self.logo_rect = self.logo_surf.get_rect(midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        self.level_button_surf: pg.Surface = pg.image.load("graphics/assets/start menu/level.png").convert_alpha()
        self.level_button_rect: pg.Rect = self.level_button_surf.get_rect(topleft = (102, self.logo_rect.midbottom[1] + 50))

        self.start_button_surf: pg.Surface = pg.image.load("graphics/assets/start menu/start.png").convert_alpha()
        self.start_button_rect: pg.Rect = self.start_button_surf.get_rect(topleft = (502, self.logo_rect.midbottom[1] + 50))

        self.start_menu_ground_surf: pg.Surface = pg.image.load("graphics/assets/start menu/ground.png").convert_alpha()
        self.start_menu_ground_rect: pg.Rect = self.start_menu_ground_surf.get_rect(bottomleft = (0, LEVEL_RESOLUTIONS[0][1]))

        #Level 1 assets
        self.level_one_ground_surf: pg.Surface = pg.image.load("graphics/assets/level 1/ground.png").convert_alpha()
        self.level_one_ground_rect: pg.Rect = self.level_one_ground_surf.get_rect(bottomleft = (0, LEVEL_RESOLUTIONS[1][1]))
        self.level_one_grav_controller_y: int = 150
        self.level_one_grav_controllers: list[GravityController] = (GravityController(game = self, coords = (175, self.level_one_grav_controller_y), direction='left'),
                                                                    GravityController(game = self, coords = (743, self.level_one_grav_controller_y), direction='right'))
        
        #Level 2 assets
        self.level_two_ground_surf: pg.Surface = pg.image.load("graphics/assets/level 2/ground.png").convert_alpha()
        self.level_two_ground_rect: pg.Rect = self.level_two_ground_surf.get_rect(bottomleft = (0, LEVEL_RESOLUTIONS[2][1]))

        self.level_two_env_mask = pg.Surface(LEVEL_RESOLUTIONS[2], pg.SRCALPHA) #Surface to obscure the screen in level 2
        self.level_two_player_mask: pg.Surface = pg.image.load("graphics/assets/level 2/mask.png").convert_alpha() #Half transparent black circle used to show the player in the dark
        
        #Pause menu
        self.previous_game_state: GameState = self.game_state #Variable to keep track of the previous game state used to return to the previous game state when unpausing

    def update_portal_animation(self): #Written here so that it can be reused in all game states
        """Function that updates the portal animation"""
        self.portal_animation_switching_delay -= 1 #Decrease the delay
        if self.portal_animation_switching_delay == 0: #If the delay has reached 0
            self.portal_animation_switching_delay = PORTAL_ANIMATION_SWITCHING_DELAY #Reset the delay
            self.portal_animation_current_frame += 1 #Progress the frame index
            if self.portal_animation_current_frame == len(self.portal_animation): self.portal_animation_current_frame = 0 #Reset the frame index if it exceeds the length of the animation
            self.current_portal_sprite = self.portal_animation[self.portal_animation_current_frame] #Update the current sprite

    def advance_level(self):
        """Function that advances the level"""
        self.player.status = 'standing' #Reset the player status
        self.current_level_num += 1 #Advance the level counter
        self.game_state = GameState(self.current_level_num) #Update the game state

        match self.game_state: #Level specific entry settings
            case GameState.LEVEL_1:
                init_level_one(self)
            case GameState.LEVEL_2: 
                init_level_two(self)

        self.update_screen_dimensions() #Update the screen dimensions
        self.portal_rect = self.current_portal_sprite.get_rect(bottomright = self.portal_coords[self.current_level_num]) #Update the portal rect

    def generic_pause_event_handler(self):
        if not self.player.is_in_air: self.player.status = 'standing'
        self.previous_game_state = self.game_state
        self.game_state = GameState.PAUSE_MENU

    def update_screen_dimensions(self):
        """Function that updates the screen dimensions"""
        self.screen = pg.display.set_mode(LEVEL_RESOLUTIONS[self.current_level_num])	

    def get_window_position(self):
        """Function that gets the topleft window position"""
        ctypes.windll.user32.GetWindowRect(self.window_handle, ctypes.byref(self.hardware_window_rect))
        return (self.hardware_window_rect.left, self.hardware_window_rect.top)

    def clamp_to_screen(self, x, y):
        """Function that clamps the desired x and y values to the screen dimensions to avoid IndexErrors and to keep the player on screen."""
        
        SCREEN_WIDTH, SCREEN_HEIGHT = LEVEL_RESOLUTIONS[self.current_level_num]

        clamped_x = max(0, min(x, SCREEN_WIDTH - 1))
        clamped_y = max(0, min(y, SCREEN_HEIGHT - 1))

        return clamped_x, clamped_y

    def handle_mouse_exit_event(self):
        """Function that handles the focus lost event"""
        self.should_draw_cursor = False
        if not self.game_state == GameState.LEVEL_1: # If the game state is not level 1 pause the game
            self.generic_pause_event_handler()

    def handle_mouse_enter_event(self):
        """Function that handles the focus gained event"""
        self.should_draw_cursor = True
        self.game_state = self.previous_game_state

    def get_monitor_handle(self):
        hwnd = pg.display.get_wm_info()['window']
        hmonitor = self.user32.MonitorFromWindow(hwnd, _MONITOR_DEFAULTTOPRIMARY)
        if not hmonitor:
            raise ctypes.WinError(ctypes.get_last_error())
        return hmonitor

if __name__ == "__main__":
    Game().run()