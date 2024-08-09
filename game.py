import pygame as pg

from logic.states.gameState import GameState
from logic.states.startMenu import handle_start_menu_events, update_start_menu, render_start_menu
from logic.physicsEntities import Player
from logic.tilemap import Tilemap

from settings import *

class Game:
    def __init__(self):
        pg.init()

        #Screen settings
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Ah It Appears To Have Done Something")
        pg.display.set_icon(pg.image.load("graphics/loophole_icon.jpg"))
        
        #Clock and time objects
        self.clock = pg.time.Clock()

        #Game variables
        self.gameState = GameState.START_MENU
        self.screen_rect=self.screen.get_rect()

        #Game objects
        self.player = Player(self)
        self.tilemap = Tilemap()

        #Init assets
        self.init_assets()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            
            if self.gameState == GameState.START_MENU:
                handle_start_menu_events(self, event)
            
    def update(self):
        if self.gameState == GameState.START_MENU:
            update_start_menu(self)

    def render(self):
        if self.gameState == GameState.START_MENU:
            render_start_menu(self)

        pg.display.flip()
        self.clock.tick(60)

    def init_assets(self):
        #Init start menu
        self.logo_font = pg.font.Font("graphics/font/silver.ttf", 58)
        self.logo_surf = self.logo_font.render("Ah It Appears To Have Done Something", True, 'black')
        self.logo_rect = self.logo_surf.get_rect(midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

        self.start_button_surf = pg.image.load("graphics/buttons/start menu/start.png")
        self.start_button_rect = self.start_button_surf.get_rect(midtop = (SCREEN_WIDTH // 2, self.logo_rect.midbottom[1] + 50))
        
if __name__ == "__main__":
    Game().run()