import pygame
import pygame.font

import color
import game


class DebugInfo(object):

    '''
    Shows debug info on the screen. For now just FPS
    Only displayed if Game.debug() is true
    '''

    def __init__(self):
        self._font = pygame.font.Font(None, 24)
        g = game.Game()
        self._clock = g.clock()
        g.input_manager().add_subscriber(self)
        self._show = g.debug()

    def notify(self, event):
        if (hasattr(event, 'type') and
                event.type == pygame.KEYDOWN and
                event.key == pygame.K_EQUALS):
            self._show = not self._show

    def update(self, dt):
        return

    def draw(self, screen):
        if self._show:
            surf = self._font.render("frames/second: %3.4f" %
                                     (self._clock.get_fps()),
                                     True,
                                     color.BLACK)
            screen.blit(surf, (24, 24))
