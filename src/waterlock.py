import entity
import pygame.image
import pygame
import platform
import sheethelper
import random
import pygame.draw
import pygame.mixer
import color


class Drop(object):
    def __init__(self, x, y, xvel, yvel):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel

    def update(self):
        self.y += self.yvel
        self.x += self.xvel

    def pos(self):
        return (self.x, self.y)

    def draw(self, surf):
        pygame.draw.line(surf, color.DARKBLUE,
                         (self.x, self.y),
                         (self.x + self.xvel, self.y + 10))


class WaterLock(platform.Platform):

    def __init__(self, i_x, i_y, w, h, ty, camera, imagefile, state):
        platform.Platform.__init__(
            self, i_x, i_y, w, h, ty, camera, imagefile, state)
        #obstacle.Obstacle.__init__(self, i_x, i_y, w, h, ty, camera, state)
        self.sprite = pygame.image.load(imagefile)

        self.health = 50

        self.expframes = sheethelper.load_frames(
            "../Images/explosionsheet.png", 8, 0, 0,
            128, 128, colorkey=(0, 0, 0))
        self.explode = False
        self.water = []
        self.fillh = 0
        self.startfill = 0
        self.startwhite = float("inf")
        self.statedwhite = False
        self.white = pygame.Surface((800, 600)).convert()
        self.white.fill(color.WHITE)
        self.explodedwall = pygame.image.load(
            "../Images/explodedfloor.png").convert()
        self.explodedwall = pygame.transform.scale(self.explodedwall, (h, 50))

        self.channel = pygame.mixer.Channel(6)
        self.sound = pygame.mixer.Sound("../Sounds/spray.ogg")

    def update(self, dt):
        platform.Platform.update(self, dt)
        if self.explode:
            if self.time - self.lastdrop > .1:
                for i in xrange(100):
                    x = self.xpos + random.randint(0, self.width)
                    y = self.ypos + random.randint(0, self.height)
                    yvel = 3 + random.randint(0, 2)
                    xvel = -1 + random.randint(0, 2)
                    self.water.append(Drop(x, y, xvel, yvel))
                    self.lastdrop = self.time
            for idx, drop in enumerate(self.water[:]):
                drop.update()
                if not self.camera.get_update_rect().collidepoint(drop.pos()):
                    self.water.pop(idx)
            if self.time - self.startfill > 5 and not self.statedwhite:
                self.startwhite = self.time
                self.statedwhite = True
                self.game().add_post_step(self.fadewhite)
                if self.game().player is not None:
                    self.game().player.invincible = 100000
            if self.time - self.startwhite > 5:
                self.channel.stop()
                self.game().load_level()

    def draw(self, surface):
        platform.Platform.draw(self, surface)
        for drop in self.water:
            drop.draw(surface)

    def get_frame(self):
        if not self.explode:
            return self.sprite
        elif self.time - self.explodestart < .8:
            return self.expframes[
                int((self.time - self.explodestart) * 8) % len(self.expframes)]
        else:
            return self.explodedwall

    def in_update_area(self):
        return self.rect.colliderect(self.camera.get_update_rect())

    def take_dmg(self, h):
        self.health -= h
        if self.health <= 0:
            if not self.explode:
                self.channel.play(self.sound)
                self.explode = True
                self.explodestart = self.time
                self.startfill = self.time
                self.lastdrop = self.time
                self.game().add_post_step(self.bluescreen)

    def bluescreen(self, canv):
        canv.fill(color.DARKBLUE,
                  pygame.Rect(0, 600 - self.fillh, 800, self.fillh))
        self.fillh += 1
        return True

    def fadewhite(self, canv):
        alpha = ((self.time - self.startwhite) / 5.0) * 255
        self.white.set_alpha(alpha)
        canv.blit(self.white, (0, 0))
        return True
