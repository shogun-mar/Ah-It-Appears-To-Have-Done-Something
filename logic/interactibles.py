import pygame as pg

class Interactibles:
    def __init__(self, game, sprite = None, rect = None):
        self.game = game
        self.sprite = sprite
        self.rect = rect

class GravityController(Interactibles):
    def __init__(self, game, coords, direction):
        super().__init__(game)

        #Animation
        self.frames = [pg.image.load(f"graphics/assets/smoke circle/version 2/{direction}/{i}.png").convert_alpha() for i in range(1, 12)]
        self.current_frame = 0
        self.switching_delay = 10 #Variable to keep track of when to progress the animation (with 6 the delay is 96 ms at 60 fps, with 10 the delay is 160 ms at 60 fps)
        self.sprite = self.frames[self.current_frame]
        
        #Logic
        self.rect = self.sprite.get_rect(topleft = coords)
        self.direction = direction
        self.action = "game.player.should_float = not game.player.should_float; game.player.controls_enabled = not game.player.controls_enabled" #Exec strings have to be written through the perspective of the name space in which they will be executed (in this case level_1.py)
        self.last_activation_time = 0

    def update_animation(self):
        """Function that updates the animation of the gravity controller"""

        self.switching_delay -= 1
        if self.switching_delay == 0: #If the delay is over
            self.switching_delay = 10 #Reset the delay
        
            self.current_frame += 1 #Progress the frame index
            if self.current_frame == 11: 
                self.current_frame = 0 #Reset the frame index if it exceeds the length of the animation

            self.sprite = self.frames[self.current_frame] #Update the current sprite

    def can_be_actived(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_activation_time > 3000 or self.last_activation_time == 0: #If three seconds have passed since the last activation
            self.last_activation_time = current_time
            return True
        return False