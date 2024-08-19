import pygame as pg

class Interactibles:
    def __init__(self, game, sprite = None, rect = None):
        self.game = game
        self.sprite = sprite
        self.rect = rect

class GravityDisabler(Interactibles):
    def __init__(self, game, coords):
        super().__init__(game)

        self.frames = [pg.image.load(f"graphics/assets/smoke circle/version 1/{i}.png").convert_alpha() for i in range(1, 12)]
        self.current_frame = 0
        self.sprite = self.frames[self.current_frame]
        self.rect = self.sprite.get_rect(topleft = coords)
        self.switching_delay = 96 #Variable to keep track of when to progress the animation (with 6 the delay is 96 ms at 60 fps, with 10 the delay is 160 ms at 60 fps)

    def update_animation(self):
        """Function that updates the animation of the gravity disabler"""

        self.switching_delay -= 1
        if self.switching_delay == 0: #If the delay is over
            self.switching_delay = 10 #Reset the delay
        
            self.current_frame += 1 #Progress the frame index
            if self.current_frame == 11: 
                self.current_frame = 0 #Reset the frame index if it exceeds the length of the animation

            self.sprite = self.frames[self.current_frame] #Update the current sprite