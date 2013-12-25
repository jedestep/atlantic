import trigger
import pygame.draw
import pygame.image
import pygame


class SavePoint(trigger.Trigger):

    def __init__(self, i_x, i_y, w, h, camera, state):
        trigger.Trigger.__init__(self, i_x, i_y, w, h, camera, state)

    def trigger(self):
        self.game().player.init_x = self.xpos
        self.game().player.init_y = self.ypos
