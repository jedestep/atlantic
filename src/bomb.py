import phys
import player
import color
import obstacle
import sheethelper
import pygame
import pygame.image
import pygame.transform
import pygame.mixer
import math
import random


class Bomb(phys.PhysEntity):

    def __init__(self, i_x, i_y, w, h, d, camera, state):
        phys.PhysEntity.__init__(self, i_x, i_y, w, h, camera, state)
        self.countdown = 300
        self.explosion = 30
        self.health = 30
        self.exploding = False

        self.frame = pygame.image.load("../Images/torpedo.png")
        self.frame.set_colorkey((255, 255, 255))
        self.frame = pygame.transform.scale(self.frame, (w, h))

        #  compute coordinates
        cx = i_x + w / 2
        cy = i_y + h / 2
        px = self.game().player.xpos
        py = self.game().player.ypos

        dy = py - cy
        dx = px - cx

        #  move towards player
        self.g = 0
        self.yacc = 0
        xmod = random.randint(10, 20)
        ymod = random.randint(10, 20)
        self.xacc = dx / (5 * xmod)
        self.yacc = dy / (5 * ymod)
        self.xvel = dx / (10 * xmod)
        self.yvel = dy / (10 * ymod)

        #  rotate towards player
        angle = math.atan2(self.yacc, self.xacc) * 180 / 3.1415926535

        self.frame = pygame.transform.rotate(
            self.frame, -1 * angle + -1 * 90)
        self._expframe = sheethelper.load_frames(
            "../Images/explosionsheet.png", 8, 0, 0,
            128, 128, colorkey=(0, 0, 0))
        self.expframe = []

        self.damaging = True

        #  TODO get a .ogg
        self.sound = pygame.mixer.Sound("../Sounds/bomb.wav")
        self.channel = pygame.mixer.Channel(3)

    def update(self, dt):
        phys.PhysEntity.update(self, dt)
        if not self.exploding:
            self.countdown -= 1
            if self.countdown == 0:
                self.explode()
        else:
            self.explosion -= 1
            if self.explosion == 0:
                self.finalize()

    def draw(self, surface):
        phys.PhysEntity.draw(self, surface)

    def get_frame(self):
        if not self.exploding:
            return self.frame
        else:
            if len(self.expframe) > 1:
                return self.expframe.pop()
            elif len(self.expframe) == 1:
                return self.expframe[0]

    def explode(self):
        #  TODO get an explosion
        self.frame = pygame.Surface((100, 100))
        self.frame.fill(color.RED)
        self.exploding = True

        self.channel.play(self.sound)

        for f in self._expframe:
            self.expframe.append(f.copy())

        self.xvel = 0
        self.yvel = 0
        self.xacc = 0
        self.yacc = 0

    def finalize(self):
        if self.game():
            self.expframe = []
            self.frame = None
            self.game().remove_entity(self)

    def _halt(self, name, reporter, target):
        if reporter == self:
            if isinstance(target, player.Player):
                if self.damaging:
                    if self.exploding:
                        target.take_dmg(25)
                        self.damaging = False
                    else:
                        self.explode()
            if isinstance(target, obstacle.Obstacle):
                if not self.exploding:
                    self.explode()
