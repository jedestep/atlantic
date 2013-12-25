import random

import pygame.image
import pygame.transform

import math

import pygame.transform


class simplebub(object):
    def __init__(self):
        self.xinit = random.randint(0, 790)
        self.x = self.xinit
        self.y = random.randint(600, 1200)
        self.yvel = random.randint(1, 3)
        img = pygame.image.load("../Images/bubble.png").convert()
        img = pygame.transform.smoothscale(img, (10, 10))
        img.set_colorkey((0, 0, 0))
        self.img = img
        self.time = random.randint(1, 20) / (.5)
        self.movewidth = random.randint(1, 8)

    def update(self, dt):
        self.time += dt
        self.y -= self.yvel
        self.x = self.xinit + math.sin(self.time * 10) * self.movewidth

    def draw(self, canvas):
        canvas.blit(self.img, (self.x, self.y))


class BubbleManager(object):
    def __init__(self, state):
        self.state = state
        self.numbubs = 20
        self.bubs = set()
        self.w = 800
        self.h = 600
        self.width = self.height = 10
        self.drawablex = self.w - self.width
        self.drawabley = self.h
        self.title = pygame.image.load("../Images/title3d.png").convert_alpha()
        self.titx = random.randint(200, 600)
        self.tity = 600
        self.rottitle = self.title
        self.rotdir = random.choice([-1, 1])

        for i in xrange(self.numbubs):
            self.bubs.add(self.newbub())
        self.time = 0

    def draw(self, canvas):
        for bub in self.bubs:
            bub.draw(canvas)
        #  seriously
        canvas.blit(self.rottitle, (self.titx, self.tity))

    def update(self, dt):
        self.time += dt
        self.tity -= dt * 30
        if self.tity < -200:
            self.tity = 650
            self.titx = random.randint(200, 600)
            self.time += random.random() * 30
            self.rotdir = random.choice([-1, 1])
        self.rottitle = pygame.transform.rotate(
            self.title, self.rotdir * self.time * 4)
        for bub in self.bubs.copy():
            bub.update(dt)
            if bub.y < (-1 * self.height):
                self.bubs.remove(bub)
                self.bubs.add(self.newbub())

    def newbub(self):
        return simplebub()
