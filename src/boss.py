import bomb
import math
import phys
import random
import color
import sheethelper

import pygame
import pygame.image
import pygame.transform
import pygame.mixer


class Boss(phys.PhysEntity):
    def __init__(self, i_x, i_y, w, h, camera, state):
        phys.PhysEntity.__init__(self, i_x, i_y, w, h, camera, state)
        self.missile_mod = 34
        self.frame = pygame.image.load("../Images/boss.png")
        self.frame.set_colorkey(self.frame.get_at((0, 0)))
        self.frame = pygame.transform.rotozoom(self.frame, 180, 1.3)

        self.default_frame = self.frame.copy()

        self.missile_timer = 500
        self.base_missile_timer = 500
        self.missile_list = []

        self.g = 0
        self.yacc = 0

        self.framecache = []
        self._framecache = []
        self.firing_loc = (0, 0)
        self._framecache = sheethelper.load_frames(
            "../Images/boss_shot.png", 6,
            2, 0, 20, 18, colorkey=(0, 0, 0))

        self.sound = pygame.mixer.Sound("../Sounds/boss_shot.ogg")
        self.channel = pygame.mixer.Channel(4)

    def should_update(self):
        return True

    def get_frame(self):
        return self.frame

    def update(self, dt):
        phys.PhysEntity.update(self, dt)
        if self.missile_timer >= 100:
            self.missile_timer -= 1
        else:
            if self.missile_timer % self.missile_mod == 0:
                self.missile()
            if self.missile_timer == 0:
                self.missile_timer = self.base_missile_timer
                self.frame = self.default_frame.copy()
            self.missile_timer -= 1
        if self.game().player is not None:

            cx = self.game().player.xpos - self.width
            cy = self.game().player.ypos - 250

            dx = cx - self.xpos
            dy = cy - self.ypos

            self.xvel = dx / 20
            self.yvel = dy / 20

        self.last_x = self.xpos
        self.last_y = self.ypos

        for i in xrange(len(self.missile_list)):
            (t, m) = self.missile_list[i]
            if t > 0:
                t -= 1
                self.missile_list[i] = (t, m)
            else:
                self._stateObject.GAME.add_entity(m)
                self._stateObject.GAME.add_mid(m)
                self.missile_list.remove((t, m))

    def draw(self, surface):
        frame = self.get_frame()
        if len(self.framecache) > 0:
            explosion = self.framecache.pop()
            frame.blit(explosion, self.firing_loc)
        else:
            frame = self.default_frame.copy()
        if frame is not None:
            surface.blit(frame, (self.xpos, self.ypos))
        if self._stateObject.DEBUG:
            PG.draw.rect(surface, (0, 0, 0), self.rect, 2)

    def missile(self):
        self.frame = self.default_frame.copy()

        px = self.game().player.xpos
        py = self.game().player.ypos

        missile_buffer = random.randint(0, 50)
        xdir = random.choice([-1, 1])

        self.framecache = []
        for f in self._framecache:
            frame = f.copy()
            self.framecache.append(frame)
        self.firing_loc = (2.26 * self.width + xdir * 59, 1)

        mx = px + (xdir * (missile_buffer + 300))
        my = py + (-1 * (missile_buffer + 400))

        self.channel.play(self.sound)

        missile = bomb.Bomb(mx, my, 40, 80, xdir,
                            self.camera,
                            self._stateObject)
        self.missile_list.append((20, missile))

    def _halt(self, name, reporter, target):
        pass
