import collections

import pygame
import pygame.event
import math

import entity
import obstacle

# TODO Make PhysEntity real subclass


class PhysEntity(entity.Entity):

    '''
    A physics entity. Can be subclasssed to give
    physics properties to a class.
    Provides gravity and movement capabilities.
    '''
    def __init__(self, i_x, i_y, w, h, camera, state):
        entity.Entity.__init__(self, i_x, i_y, w, h, camera, state)
        self.g = 9.81
        self.xvel = 0
        self.yvel = 0
        self.xacc = 0
        self.yacc = self.g
        self.groundborne = False
        self.airborne = True
        self.forces = []
        self.last_x = 0
        self.last_y = 0
        self.callbacks = {
            'COLLIDE': self._halt
        }
        self.init_x = i_x
        self.init_y = i_y

    def update(self, dt):
        dt *= 15
        entity.Entity.update(self, dt)
        self.last_x = self.xpos
        self.last_y = self.ypos
        self.xpos += self.xvel * dt + .5 * self.xacc * dt * dt
        self.ypos += self.yvel * dt + .5 * self.yacc * dt * dt
        self.xvel += self.xacc * dt
        self.yvel += self.yacc * dt

        self.rect.left = self.xpos
        self.rect.top = self.ypos

        if not self.groundborne:
            self.airborne = True
        else:
            self.airborne = False

        self.groundborne = False

    def notify(self, event):
        # TODO should check instance?
        if hasattr(event, "type") and hasattr(event, "key"):
            if (event.type, event.key) in self.callbacks:
                self.callbacks[(event.type, event.key)]()
        else:
            if isinstance(event, tuple):
                (nm, rpt, tgt) = event
                if nm in self.callbacks:
                    self.callbacks[nm](nm, rpt, tgt)

        if self.yvel != 0:
            self.airborne = True

    def _halt(self, name, reporter, target):
        if reporter == self:
            if isinstance(target, obstacle.Obstacle):
                if target.ty == "WALL":
                    self.xpos = self.last_x
                    self.rect.left = self.xpos
                    self.xvel = 0
                elif target.ty == "FLOOR":
                    self.ypos = self.last_y
                    self.rect.top = self.ypos
                    self.yvel = 0
                    self.airborne = False
                elif target.ty == "PLATFORM":
                    epsilon = 1
                    l = target.xpos - epsilon
                    r = target.xpos + target.width + epsilon
                    b = target.ypos + target.height + epsilon
                    t = target.ypos - epsilon
                    # character overlaps with platform in x direction
                    char_inside_platform_horiz = (
                        l < (reporter.xpos + reporter.width)
                        and (reporter.xpos + reporter.width) < r or
                        l < (reporter.xpos) and (reporter.xpos) < r)
                    # character overlaps with platform in y direction
                    char_inside_platform_vert = (
                        b > (reporter.ypos + reporter.height)
                        and (reporter.ypos + reporter.height) > t or
                        b > (reporter.ypos) and (reporter.ypos) > t)
                    floor = math.floor  # pep8 :(

                    char_above = ((target.ypos) >=
                                  floor(reporter.last_y + reporter.height))
                    char_below = ((target.ypos + target.height)
                                  <= (reporter.last_y))
                    if (char_inside_platform_horiz and
                            (not char_above and not char_below)):
                        self.xpos = self.last_x
                        self.rect.left = self.xpos
                        self.xvel = 0
                        char_left = math.ceil(
                            target.xpos) >= (
                                reporter.xpos +
                                reporter.width)
                        char_right = math.ceil(
                            target.xpos +
                            target.width) <= (
                                reporter.xpos)
                        if char_left or char_right or self.airborne:
                            self.xacc = 0
                            self.yacc = self.g
                            return
                    if char_inside_platform_vert:
                        if ((reporter.ypos + reporter.height) > t
                                and not char_below):
                            self.airborne = False
                            self.groundborne = True
                        self.ypos = self.last_y
                        self.rect.top = self.ypos
                        self.yvel = 0
                    self.xacc = 0
                    self.yacc = self.g
