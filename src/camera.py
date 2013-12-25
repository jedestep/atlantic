import entity
import pygame.sprite as PS
import pygame.rect as PR
import pygame


class Camera(entity.Entity):

    def __init__(self, state):
        entity.Entity.__init__(self, 0, 0, 0, 0, self, state)
        self.xpos = 0
        self.ypos = 0
        self.xvel = 0
        self.yvel = 0
        self.last_x = self.xpos
        self.last_y = self.ypos
        self.rect = PR.Rect(0, 0, 800, 600)
        self.update_rect = self.rect.inflate(
            self.rect.width * 1.75, self.rect.height * 1.75)
        self.big_update_rect = self.rect.inflate(
            self.rect.width * 2, self.rect.height * 2)

    # TODO Move this out of here, BUT IT'S SO CONVEINANT :(
    def get_update_rect(self):
        return self.update_rect.copy()

    def get_big_update_rect(self):
        return self.big_update_rect.copy()

    def update(self, dt):
        self.rect.x = self.xpos
        self.rect.y = self.ypos
        self.update_rect = self.rect.inflate(
            self.rect.width * 1.75, self.rect.height * 1.75)
        self.big_update_rect = self.rect.inflate(
            self.rect.width * 2, self.rect.height * 2)

    def draw(self, surface):
        pass

    def notify(self, event):
        pass

    def in_camera(self):
        return True

    def can_collide(self):
        return False

    def should_update(self):
        return True
