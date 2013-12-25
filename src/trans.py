import state
import pygame


class Transition(state.State):
    def __init__(self, state, trans, state1, state2, dur=.14):
        self.state = state
        self.trans = trans.lower()
        self.state1 = state1
        self.state2 = state2
        self.dur = dur
        self.time = 0
        self.canv1 = pygame.Surface((800, 600))
        self.canv2 = pygame.Surface((800, 600))
        state1.draw(self.canv1)
        state2.draw(self.canv2)

    def update(self, dt):
        self.time += dt
        if self.time > self.dur:
            self.state.STATE = self.state2

    def draw(self, canvas):
        canvas.fill((0, 0, 0))
        prog = self.time / self.dur
        x1 = 0
        y1 = 0
        x2 = 800
        y2 = 0
        if self.trans == "left":
            x1 = -1 * prog * 800
            x2 = x1 + 800
        elif self.trans == "right":
            x1 = prog * 800
            x2 = x1 - 800
        elif self.trans == "black":
            if self.time <= 2:
                prog1 = 1 - (self.time / 2.0)
            else:
                prog1 = 0
            if self.time > 2:
                prog2 = (self.time - 2.0) / 2.0
            else:
                prog2 = 0
            self.canv1.set_alpha(255 * prog1)
            self.canv2.set_alpha(255 * prog2)
            x2 = 0

        canvas.blit(self.canv1, (x1, y1))
        canvas.blit(self.canv2, (x2, y2))
