import pygame as pg
from logic.states import GameState

class Game:
    def __init__(self):
        pg.init()

        #Screen settings
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Ah It Appears To Have Done Something")
        pg.display.set_icon(pg.image.load("graphics/loophole_icon.jpg"))
        
        #Clock and time objects
        self.clock = pg.time.Clock()

        #Game variables
        self.gameState = GameState.START_MENU

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
                self.handle_start_menu_events(self, event)
            

    def update(self):
        if self.gameState == GameState.START_MENU:
            self.update_start_menu(self)

    def render(self):
        if self.gameState == GameState.START_MENU:
            self.render_start_menu(self.screen)

        pg.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    Game().run()