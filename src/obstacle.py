import entity
import pygame as PG


class Obstacle(entity.Entity):

    '''
    A wall, a floor, anything that collides with other things
    '''
    def __init__(self, i_x, i_y, w, h, ty, camera, state):
        entity.Entity.__init__(self, i_x, i_y, w, h, camera, state)
        self.init_x = i_x
        self.init_y = i_y
        self.ty = ty
        self.color = (0, 0, 0)
        if ty == "DEATHTRIGGER":
            self.color = (255, 0, 0)
        self.motive = False

    def update(self, dt):
        entity.Entity.update(self, dt)

    def draw(self, surface):
        entity.Entity.draw(self, surface)
        #PG.draw.rect(surface, self.color, self.rect, 2)
