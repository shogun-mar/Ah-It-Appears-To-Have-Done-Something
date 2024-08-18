import contextlib
with contextlib.redirect_stdout(None): #Suppress pygame welcome message
    import pygame as pg
from logic.states.gameState import GameState
from logic.states.startMenu import handle_start_menu_events, update_start_menu, render_start_menu
from logic.physicsEntities import Player

from settings import *

class Game:
    def __init__(self):
        pg.init()

        #Screen settings
        self.screen: pg.Surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Ah It Appears To Have Done Something")
        pg.display.set_icon(pg.image.load("graphics/loophole_icon.jpg"))
        pg.mouse.set_visible(False) #Hide the mouse cursor
        
        #Clock and time objects
        self.clock: pg.Clock = pg.time.Clock()

        #Game variables
        self.gameState: GameState = GameState.START_MENU
        self.screen_rect: pg.Rect = self.screen.get_rect()

        #Game objects
        self.player = Player(self)
        self.entities = []

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
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                quit()
            
            if self.gameState == GameState.START_MENU:
                handle_start_menu_events(self, event)
            
    def update(self):
        """Function that updates generic values not specific to any game state and calls the appropriate update function by consulting the current game state"""

        pg.display.set_caption(f" Ah It Appears To Have Done Something - FPS: {int(self.clock.get_fps())}") #Update the window title to show the FPS

        
        if self.gameState == GameState.START_MENU:
            update_start_menu(self)

    def render(self):
        """Function that renders the game by calling the appropriate render function by consulting the current game state"""


        self.screen.fill('white') #Clear the screen
        
        if self.gameState == GameState.START_MENU:
            render_start_menu(self)

        pg.display.flip()
        self.clock.tick(MAX_FPS)

    def init_assets(self):
        """Function that initializes all the assets for the game"""

        #Init start menu
        self.logo_font: pg.Font = pg.font.Font("graphics/font/silver.ttf", 58)
        self.logo_surf: pg.Surface = self.logo_font.render("Ah It Appears To Have Done Something", True, 'black')
        self.logo_rect = self.logo_surf.get_rect(midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        self.level_button_surf: pg.Surface = pg.image.load("graphics/assets/start menu/level.png").convert_alpha()
        self.level_button_rect: pg.Rect = self.level_button_surf.get_rect(topleft = (100, self.logo_rect.midbottom[1] + 50))

        self.start_button_surf: pg.Surface = pg.image.load("graphics/assets/start menu/start.png").convert_alpha()
        self.start_button_rect: pg.Rect = self.start_button_surf.get_rect(topleft = (498, self.logo_rect.midbottom[1] + 50))

        self.start_menu_ground_surf: pg.Surface = pg.image.load("graphics/assets/start menu/ground.png").convert_alpha()
        self.start_menu_ground_rect: pg.Rect = self.start_menu_ground_surf.get_rect(bottomleft = (0, SCREEN_HEIGHT))

        self.cursor_surf: pg.Surface = pg.image.load("graphics/assets/start menu/cursor.png").convert_alpha()

if __name__ == "__main__":
    Game().run()