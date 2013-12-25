import random
import math

import entity
import playershot
import phys
import game
import playershot

import pygame
import pygame.image as PI
import pygame.display as PD
import pygame.transform as PT

import sheethelper

import obstacle


class Enemy(phys.PhysEntity):

    # Takes initial position, bounding box, list of animation frames
    def __init__(self, i_x, i_y, w, h, camera, state):
        phys.PhysEntity.__init__(self, i_x, i_y, w, h, camera, state)
        self.callbacks = {
            'COLLIDE': self._collide
        }
        self.myspeed = random.randint(10, 20)
        self._go_left()
        self.numframes = 9
        self._frames = sheethelper.load_frames("../Images/enemysheet.png",
                                               self.numframes, 0, 404, 60, 40)
        self.health = 30

    def update(self, dt):
        phys.PhysEntity.update(self, dt)
        #if (abs(self.ypos - self._stateObject.GAME.player.ypos) < 150 and
        #        abs(self.xpos - self._stateObject.GAME.player.xpos) < 300):
        if self.should_update():
            if self.xpos < self._stateObject.GAME.player.xpos:
                self._go_right()
            else:
                self._go_left()

    def notify(self, event):
        phys.PhysEntity.notify(self, event)

    def _go_right(self):
        self.xvel = self.myspeed

    def _stop(self):
        self.xvel = 0

    def _go_left(self):
        self.xvel = -self.myspeed

    def _switch_directions(self):
        self.xvel *= -1

    def get_frame(self):
        frame = self._frames[int(self.time % self.numframes)]
        if self.xvel < 0:
            frame = PT.flip(frame, True, False)
        return frame

    def take_dmg(self, h):
        self.health -= h
        if self.health <= 0:
            self._stateObject.GAME.remove_entity(self)

    def _collide(self, name, reporter, target):
        if reporter == self:
            if isinstance(target, obstacle.Obstacle):
                #print "Enemy floor collide!"
                if target.ty == "WALL":
                    self.xpos = self.last_x
                    self.rect.left = self.xpos
                    self._switch_directions()
                elif target.ty == "FLOOR" or target.ty == "DEATHTRIGGER":
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
                        #print "horiz collide"
                        self.xpos = self.last_x
                        self.rect.left = self.xpos
                        # self.xvel = 0
                        self._switch_directions()
                        char_left = (
                            target.xpos) >= (
                                reporter.xpos +
                                reporter.width)
                        char_right = math.ceil(
                            target.xpos +
                            target.width) <= (
                                reporter.xpos)
                        if char_left or char_right:
                            self.xacc = 0
                            self.yacc = self.g
                            return
                    if char_inside_platform_vert:
                        if (reporter.ypos + reporter.height) > t:
                            self.airborne = False
                        self.ypos = self.last_y
                        self.rect.top = self.ypos
                        self.yvel = 0
                    self.xacc = 0
                    self.yacc = self.g
