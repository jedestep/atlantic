import pygame
import pygame.image
import entity
import lasershot

import color


class Lasercannon(entity.Entity):
    """
    The Lasercannon enemy that will sit on the ceiling and
    shoot down on a fixed interval
    """
    def __init__(self, i_x, i_y, w, h, camera, d, state):
        entity.Entity.__init__(self, i_x, i_y, w, h, camera, state)

        self.health = 10
        self.d = d
        if d == 'S':
            self.frame = pygame.image.load(
                "../Images/laserDown.png").convert()
        elif d == 'N':
            self.frame = pygame.image.load(
                "../Images/laserUp.png").convert()
        elif d == 'W':
            self.frame = pygame.image.load(
                "../Images/laserLeft.png").convert()
        elif d == 'E':
            self.frame = pygame.image.load(
                "../Images/laserRight.png").convert()
        else:
            #TODO need to get the sprite for the Lasercannon
            self.frame = pygame.Surface((w, h))
            self.frame.fill(color.BLUE)
        self.frame.set_colorkey((0, 0, 0))

        self.fire_time = 2
        self.shot = None

    def get_frame(self):
        return self.frame

    def update(self, dt):
        entity.Entity.update(self, dt)
        #check if its time to fire
        if self.time >= self.fire_time:
            self.time = 0
            self.__shoot()

    def take_dmg(self, h):
        self.health -= h
        if self.health <= 0:
            if self.shot is not None:
                self.shot.finalize()
            self._stateObject.GAME.remove_entity(self)

    def __shoot(self):
        if self.d == 'S':
            shot = lasershot.Lasershot(self.xpos + 5, self.ypos + 50,
                                       40, 10, 3000, self.d, self,
                                       self.camera, self._stateObject)
        elif self.d == 'E':
            shot = lasershot.Lasershot(self.xpos + 70, self.ypos + 10,
                                       10, 38, 3000, self.d, self,
                                       self.camera, self._stateObject)
        elif self.d == 'N':
            shot = lasershot.Lasershot(self.xpos + 5, self.ypos - 10,
                                       40, 10, 3000, self.d, self,
                                       self.camera, self._stateObject)
        elif self.d == 'W':
            shot = lasershot.Lasershot(self.xpos - 10, self.ypos + 10,
                                       10, 38, 3000, self.d, self,
                                       self.camera, self._stateObject)
        self.shot = shot
        self._stateObject.GAME.add_entity(shot)
        self._stateObject.GAME.add_mid(shot)
