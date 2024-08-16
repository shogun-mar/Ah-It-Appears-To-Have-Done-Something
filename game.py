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
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Ah It Appears To Have Done Something")
        pg.display.set_icon(pg.image.load("graphics/loophole_icon.jpg"))
        pg.mouse.set_visible(False) #Hide the mouse cursor
        
        #Clock and time objects
        self.clock = pg.time.Clock()

        #Game variables
        self.gameState = GameState.START_MENU
        self.screen_rect=self.screen.get_rect()

        #Game objects
        self.player = Player(self)
        self.entities = []

        #Init assets
        self.init_assets()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                quit()
            
            if self.gameState == GameState.START_MENU:
                handle_start_menu_events(self, event)
            
    def update(self):
        pg.display.set_caption(f" Ah It Appears To Have Done Something - FPS: {int(self.clock.get_fps())}") #Set the window title to show the FPS

        if self.gameState == GameState.START_MENU:
            update_start_menu(self)

    def render(self):
        if self.gameState == GameState.START_MENU:
            render_start_menu(self)

        pg.display.flip()
        self.clock.tick(MAX_FPS)

    def init_assets(self):
        #Init start menu
        self.logo_font = pg.font.Font("graphics/font/silver.ttf", 58)
        self.logo_surf = self.logo_font.render("Ah It Appears To Have Done Something", True, 'black')
        self.logo_rect = self.logo_surf.get_rect(midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        self.level_button_surf = pg.image.load("graphics/assets/start menu/level.png").convert_alpha()
        self.level_button_rect = self.level_button_surf.get_rect(topleft = (100, self.logo_rect.midbottom[1] + 50))

        self.start_button_surf = pg.image.load("graphics/assets/start menu/start.png").convert_alpha()
        self.start_button_rect = self.start_button_surf.get_rect(topleft = (498, self.logo_rect.midbottom[1] + 50))

        self.start_menu_ground_surf = pg.image.load("graphics/assets/start menu/ground.png").convert_alpha()
        self.start_menu_ground_rect = self.start_menu_ground_surf.get_rect(bottomleft = (0, SCREEN_HEIGHT))

        self.cursor_surf = pg.image.load("graphics/assets/start menu/cursor.png").convert_alpha()

if __name__ == "__main__":
    Game().run()