import phys
import pygame
import pygame.image
import pygame.transform
import pygame.draw as PD

import obstacle

import color

import random

import math

import cutscenemanager


class Bubble(phys.PhysEntity):

    def __init__(self, i_x, i_y, w, v_x, v_y, camera, c, player, state):
        phys.PhysEntity.__init__(self, i_x, i_y, w, w, camera, state)
        self.player = player
        self.g = 0
        self.yvel = v_y
        self.xvel = v_x
        self.yacc = 0
        self.xacc = 0
        self.frame = pygame.image.load("../Images/bubble.png").convert()
        self.frame = pygame.transform.smoothscale(self.frame, (w, w))
        self.frame.set_colorkey((0, 0, 0))

    def update(self, dt):
        phys.PhysEntity.update(self, dt)
        self.xvel = math.sin(self.time) * 4
        if not self.in_update_area():
            self.player._delete_bubble(self)

    def draw(self, canvas):
        phys.PhysEntity.draw(self, canvas)

    def get_frame(self):
        return self.frame

    def _halt(self, name, reporter, target):
        if reporter == self:
            if isinstance(target, obstacle.Obstacle):
                self.player._delete_bubble(self)
            elif isinstance(target, cutscenemanager.cutscenemanager):
                self.player._delete_bubble(self)
