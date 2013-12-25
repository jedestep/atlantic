import entity
import pygame.image
import pygame


class Cutscene(entity.Entity):
    def __init__(self, i_x, i_y, w, h, camera, state, imagefile):
        entity.Entity.__init__(self, i_x, i_y, w, h, camera, state)
        self.image = None
        if imagefile:
            self.image = pygame.image.load(imagefile).convert()

    def get_frame(self):
        return self.image

    def notify(self, event):
        if hasattr(event, "type") and hasattr(event, "key") and \
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._stateObject.GAME.load_level()
