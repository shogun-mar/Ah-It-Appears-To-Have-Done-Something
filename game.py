import pygame as pg

from logic.states.gameState import GameState
from logic.states.startMenu import init_start_menu, handle_start_menu_events, update_start_menu, render_start_menu

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

        #Generic assets
        self.generic_font = pg.font.Font("graphics/font/silver.ttf", 36)

        #Init game state specific assets
        init_start_menu()

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

if __name__ == "__main__":
    Game().run()