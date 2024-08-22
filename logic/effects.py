from settings import pg, EFFECTS_ANIMATION_SWITCHING_DELAY

class SmokeEffect:
    def __init__(self, type, coords, game):

        self.animation_switching_delay = EFFECTS_ANIMATION_SWITCHING_DELAY
        self.game = game
        self.current_frame = 0

        match type:
            case 'landing':
                self.frames = [pg.image.load(f"graphics/assets/effects/landing/{i}.png").convert_alpha() for i in range(1, 10)]
                self.sprite = self.frames[self.current_frame]
                self.rect = self.sprite.get_rect(center = coords)
                self.num_frames = 8 #Number of frames in the animation (written here to avoid having to call len(self.frames) every frame)
            case 'jumping':
                self.frames = [pg.image.load(f"graphics/assets/effects/jumping/{i}.png").convert_alpha() for i in range(1, 10)]
                self.sprite = self.frames[self.current_frame]
                self.rect = self.sprite.get_rect(center = coords)
                self.num_frames = 8

    def update_animation(self):
        """Function that updates the animation of the smoke effect"""

        self.animation_switching_delay -= 1
        if self.animation_switching_delay == 0: #If the delay is over
            self.animation_switching_delay = EFFECTS_ANIMATION_SWITCHING_DELAY #Reset the delay

            self.current_frame += 1 #Progress the frame index
            if self.current_frame == self.num_frames: self.destroy()

            try:
                self.sprite = self.frames[self.current_frame] #Update the current sprite
            except IndexError:
                print(f"IndexError: {self.current_frame}")

    def destroy(self):
        """Function that destroys the smoke effect"""

        self.game.effects.remove(self)
        #No del self because that would only delete that reference to the effect inside this method
