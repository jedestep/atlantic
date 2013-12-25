import entity
import player
import pygame.rect


class Trigger(entity.Entity):
    def __init__(self, i_x, i_y, w, h, camera, state):
        entity.Entity.__init__(self, i_x, i_y, w, h, camera, state)
        self.triggered = False
        self.rect = pygame.rect.Rect(i_x, i_y - 300, w, h + 600)

    def draw(self, canvas):
        pass

    def notify(self, event):
        if isinstance(event, tuple):
            (name, reporter, target) = event
            if name == "COLLIDE" and reporter == self:
                if isinstance(target, player.Player):
                    if not self.triggered:
                        self.triggered = True
                        self.trigger()
                        return 1
            return 0
        return -1

    def trigger(self):
        pass
