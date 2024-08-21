import contextlib, ctypes
with contextlib.redirect_stdout(None): #Suppress pygame welcome message
    import pygame as pg
del contextlib
from logic.states.gameState import GameState
from logic.states.startMenu import handle_start_menu_events, update_start_menu, render_start_menu
from logic.states.pauseMenu import handle_pause_menu_events, update_pause_menu, render_pause_menu
from logic.states.level_1 import handle_level_one_events, update_level_one, render_level_one, init_level_one
from logic.states.level_2 import handle_level_two_events, update_level_two, render_level_two, init_level_two
from logic.physicsEntities import Player
from logic.interactibles import GravityController, JumpPad

from settings import *

#Constants
_MONITOR_DEFAULTTONEAREST = 2

class Game:
    def __init__(self):
        pg.init()

    	#Game variables
        self.game_state: GameState = GameState.START_MENU
        self.current_level_num: int = self.game_state.value
        self.should_draw_cursor: bool = True

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
                
        # Load necessary DLLs
        self.user32 = ctypes.WinDLL('user32')
        self.dxva2 = ctypes.WinDLL('dxva2')

        # Get necessary window and monitor handles
        self.window_handle = pg.display.get_wm_info()['window'] # Get handle of the current window
        self.hardware_monitor = self.user32.MonitorFromWindow(self.window_handle, _MONITOR_DEFAULTTONEAREST) # Get handle of the monitor the game is running on

        #Init assets
        self.init_assets()

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
                self.quit_game()

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

        #If the player has just finished the damaged animation reset the player
        if self.player.status == 'damaged' and self.player.current_animation_frame == 3: self.player.reset()
        
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
        self.portal_coords: list[tuple] = [(800, 494), (950, 334), (949, 94)] #Coordinates of the portal in each level (bottomright) (DO NOT CHANGE) (result may appear strange but its because the portal sprite have extra width to accomodate the particles)
        self.portal_animation_current_frame: int = 0 #Variable to keep track of the index of the current frame of the portal animation
        self.portal_animation_switching_delay: int = PORTAL_ANIMATION_SWITCHING_DELAY #Variable to keep track of when to progress the animation
        self.portal_animation: list[pg.Surface] = [pg.image.load(f"graphics/assets/portal/{i}.png").convert_alpha() for i in range(1, 7)]
        self.current_portal_sprite: pg.Surface = self.portal_animation[self.portal_animation_current_frame] #Variable to keep track of the current sprite of the portal animation
        self.portal_rect: pg.Rect = self.current_portal_sprite.get_rect(bottomright = self.portal_coords[self.current_level_num]) 

        #Init start menu

        self.level_button_surf: pg.Surface = pg.image.load("graphics/assets/start menu/level.png").convert_alpha()
        self.level_button_rect: pg.Rect = self.level_button_surf.get_rect(topleft = (102, (SCREEN_HEIGHT // 4) + 100))

        self.start_button_surf: pg.Surface = pg.image.load("graphics/assets/start menu/start.png").convert_alpha()
        self.start_button_rect: pg.Rect = self.start_button_surf.get_rect(topleft = (502, (SCREEN_HEIGHT // 4) + 100))

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
        self.level_two_env_mask: pg.Surface = pg.image.load("graphics/assets/level 2/mask.png").convert_alpha() #Half transparent black circle used to show the player in the dark
        self.level_two_jump_pad: JumpPad = JumpPad(game = self, bottom_left_coords = (0, LEVEL_RESOLUTIONS[2][1]))
        
        #Pause menu
        self.paused_game_state: GameState = self.game_state #Variable to keep track of the previous game state used to return to the previous game state when unpausing
        self.darken_surf: pg.Surface = pg.Surface(LEVEL_RESOLUTIONS[0]) #Create a surface to darken the screen
        self.darken_surf.set_alpha(PAUSE_MENU_BACKGROUND_ALPHA) #Set the alpha value of the darken surface

        screen_center_x = LEVEL_RESOLUTIONS[0][0] // 2
        self.pause_menu_pause_text: pg.Surface = pg.image.load("graphics/assets/pause menu/pause.png").convert_alpha()
        self.pause_menu_pause_rect: pg.Rect = self.pause_menu_pause_text.get_rect(midtop = (screen_center_x, LEVEL_RESOLUTIONS[0][1] // 4))

        self.pause_menu_resume_text: pg.Surface = pg.image.load("graphics/assets/pause menu/resume.png").convert_alpha()
        self.pause_menu_resume_rect: pg.Rect = self.pause_menu_resume_text.get_rect(midtop = (screen_center_x, LEVEL_RESOLUTIONS[0][1] // 2 - 50))

        self.pause_menu_quit_text: pg.Surface = pg.image.load("graphics/assets/pause menu/quit.png").convert_alpha()
        self.pause_menu_quit_rect: pg.Rect = self.pause_menu_quit_text.get_rect(midtop = (screen_center_x, (LEVEL_RESOLUTIONS[0][1] // 4) * 3 - 100))

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
        self.darken_surf = pg.transform.scale(self.darken_surf, LEVEL_RESOLUTIONS[self.current_level_num]) #Update the darken surface
        self.portal_rect = self.current_portal_sprite.get_rect(bottomright = self.portal_coords[self.current_level_num]) #Update the portal rect

    def generic_pause_event_handler(self):
        if not self.player.is_in_air: self.player.status = 'standing'
        self.paused_game_state = self.game_state
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
        if not self.game_state == GameState.LEVEL_1 and not self.game_state == GameState.LEVEL_2: # If the game state is not level 1 pause the game
            self.generic_pause_event_handler()

    def handle_mouse_enter_event(self):
        """Function that handles the focus gained event"""
        self.should_draw_cursor = True
        self.game_state = self.paused_game_state

    def get_monitor_handle(self):
        """Function that gets the handle of the monitor the game is running on"""
        return self.user32.MonitorFromWindow(self.window_handle, 0)

    def quit_game(self):
        pg.quit()
        exit()
        quit()

if __name__ == "__main__":
    Game().run()