import phys
import pygame
import pygame.draw as PD
import pygame.image
import pygame.transform

import lasercannon
import enemy

import obstacle
import waterlock

import color

import sheethelper

import math


class PlayerShot(phys.PhysEntity):

    def __init__(self, i_x, i_y, w, h, v, d, camera, c, player, state):
        phys.PhysEntity.__init__(self, i_x, i_y, w, h, camera, state)
        self.player = player
        self.g = 0
        self.yvel = 0
        self.xvel = 0
        self.yacc = 0
        self.xacc = 0
        #v=1
        self.dir = d
        if d == 'N':
            self.yvel = -1 * v
        elif d == 'E':
            self.xvel = v
        elif d == 'S':
            self.yvel = v
        elif d == 'W':
            self.xvel = -1 * v

        if c == color.RED:
            self.frames = [pygame.image.load("../Images/bullet_red.png")
                           .convert_alpha()]
        elif c == color.BLUE:
            self.frames = [pygame.image.load("../Images/bullet_blue.png")
                           .convert_alpha()]
        elif c == color.GREEN:
            self.frames = [pygame.image.load("../Images/bullet_green.png")
                           .convert_alpha()]
        elif c == color.YELLOW:
            self.frames = [pygame.image.load("../Images/bullet_yellow.png")
                           .convert_alpha()]
        else:
            self.frames = [pygame.Surface((w, h)).convert_alpha()]
            self.frames[0].fill((0, 0, 0, 1))

        self.c = c

        if d == 'N' or d == 'S':
            self.frames[0] = pygame.transform.scale(self.frames[0], (h, w))
            self.frames[0] = pygame.transform.rotate(self.frames[0], 90)
        else:
            self.frames[0] = pygame.transform.scale(self.frames[0], (w, h))

        self.numframes = 1
        self.dying = False
        self.dietimer = 40

    def update(self, dt):
        phys.PhysEntity.update(self, dt)
        if not self.in_update_area():
            self.player._delete_shot(self)
        elif self.dying:
            self.dietimer -= 1
            if (self.dietimer <= 0):
                self._stateObject.GAME.remove_entity(self)

    def draw(self, canvas):
        phys.PhysEntity.draw(self, canvas)

    def get_frame(self):
        return self.frames[int(self.time % self.numframes)]

    def _halt(self, name, reporter, target):
        if reporter == self and not self.dying:
            remove = False
            if isinstance(target, lasercannon.Lasercannon):
                target.take_dmg(10)
                self.dying = True
                remove = True
            if isinstance(target, enemy.Enemy):
                target.take_dmg(10)
                self.dying = True
                remove = True
            if isinstance(target, waterlock.WaterLock):
                target.take_dmg(10)
                self.dying = True
                remove = True
            if isinstance(target, obstacle.Obstacle):
                self.dying = True
                remove = True
            if remove:
                self.xvel = 0
                self.yvel = 0
                if self.c == color.GREEN:
                    self.frames = sheethelper.load_frames(
                        "../Images/sparks_green.png", 4, 0, 0,
                        64, 64)
                else:
                    self.frames = sheethelper.load_frames(
                        "../Images/sparks.png", 4, 0, 0,
                        64, 64)
                self.numframes = 4
                self.xpos -= 32
                self.ypos -= 32
