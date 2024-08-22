from settings import pg, EFFECTS_ANIMATION_SWITCHING_DELAY

class SmokeEffect:
    def _init_(self, type, coords):

        self.animation_switching_delay = EFFECTS_ANIMATION_SWITCHING_DELAY

        match type:
            case 'landing':
                self.frames = [pg.image.load(f"graphics/effects/smoke/landing/{i}.png").convert_alpha() for i in range(1, 12)]
                self.sprite = self.frames[0]
                self.rect = self.sprite.get_rect(midbottom = coords)

    def update_animation(self):
        """Function that updates the animation of the smoke effect"""

        self.animation_switching_delay -= 1
        if self.animation_switching_delay == 0: #If the delay is over
            self.animation_switching_delay = EFFECTS_ANIMATION_SWITCHING_DELAY #Reset the delay

            self.current_frame += 1 #Progress the frame index
            if self.current_frame == 11: 
                self.current_frame = 0 #Reset the frame index if it exceeds the length of the animation

            self.sprite = self.frames[self.current_frame] #Update the current sprite
