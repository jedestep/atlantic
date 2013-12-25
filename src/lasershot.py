import pygame
import pygame.locals
import phys
import pygame.rect as PR

import player
import obstacle

import color


class Lasershot(phys.PhysEntity):

    def __init__(self, i_x, i_y, w, h, v, d, par, camera, state):
        phys.PhysEntity.__init__(self, i_x, i_y, w, h, camera, state)
        self.parent = par
        self.g = 0
        self.yvel = 0
        self.xvel = 0
        self.yacc = 0
        self.xacc = 0
        self.ygrow = 0
        self.xgrow = 0
        self.do_update = True
        self.remove_timer = 300
        self.base_timer = 300
        self.life_timer = 0
        if d == 'N':
            self.ygrow = -1 * v
        elif d == 'E':
            self.xgrow = v
        elif d == 'S':
            self.ygrow = v
        elif d == 'W':
            self.xgrow = -1 * v

        self.frame = pygame.Surface((w, h))
        self.frame.fill(color.RED)

        self.alive = True

    def should_update(self):
        return True

    def update(self, dt):
        if self.alive and self.should_update():
            new_width = self.width + abs(int(self.xgrow * dt))
            new_height = self.height + abs(int(self.ygrow * dt))
            if (self.do_update
                    and (new_width != self.rect.width
                         or new_height != self.rect.height)):
                if self.xgrow < 0:
                    self.xpos += int(self.xgrow * dt)
                if self.ygrow < 0:
                    self.ypos += int(self.ygrow * dt)
                self.width = new_width
                self.height = new_height
                self.rect = PR.Rect(self.xpos, self.ypos,
                                    new_width, new_height)
                phys.PhysEntity.update(self, dt)
                self.life_timer += 1
            if self.life_timer >= self.base_timer:
                self.finalize()

    def draw(self, surface):
        if self.in_camera():
            frame = self.get_frame()
            if frame is not None:
                surface.blit(frame, (self.xpos, self.ypos),
                             None, pygame.locals.BLEND_ADD)
            if self._stateObject.DEBUG:
                PG.draw.rect(surface, (0, 0, 0), self.rect, 2)

    def get_frame(self):
        return self.frame

    def finalize(self):
        if self.game():
            self.parent.shot = None
            self.frame = None
            self.game().remove_entity(self)
            remove = False
            self.alive = False

    def _halt(self, name, reporter, target):
        if reporter == self:
            remove = False
            if isinstance(target, player.Player):
                if self.get_frame() is not None and not self.do_update:
                    target.take_dmg(50)
                    #remove = True
            if isinstance(target, obstacle.Obstacle):
                if self.remove_timer <= 0:
                    remove = True
                    self.remove_timer = 10000
                    #self.do_update = True
                else:
                    #we collided with an obstacle
                    if self.do_update:
                        self.frame = pygame.Surface(
                            (self.rect.width, self.rect.height))
                        self.frame.fill(color.RED)
                    self.do_update = False
                    self.remove_timer -= 1
            if isinstance(target, Lasershot):
                #remove = False
                pass
            if remove:
                self.finalize()
