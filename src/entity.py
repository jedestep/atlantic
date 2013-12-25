import pygame.sprite as PS
import pygame.rect as PR
import pygame as PG
import math
import envmanager

ZONEBUFFER = 5
# Use a few pixels so that if we are right
# on the edge of a zone we are included in it.
# Worst thing that happens is we do a few extra update checks


class Entity(PS.Sprite):
    """
    The generic entity. Everything in the game will be an entity
    """
    # Takes initial position, bounding box, list of animation frames
    def __init__(self, i_x, i_y, w, h, camera, state):
        PS.Sprite.__init__(self)
        self._stateObject = state
        self.last_camera_x = 0
        self.last_camera_y = 0
        self.xpos = i_x
        self.ypos = i_y
        self.width = w
        self.height = h
        self.rect = PR.Rect(i_x, i_y, w, h)
        self.ent_last_rect = self.rect.copy()
        self.ent_last_rect.x -= 1
        # Make sure that we update the grids the first time always

        self.buckets = set()

        self.time = 0.0
        self.camera = camera

        self.deleteme = False
        self.motive = True

    def rect_equals(self, rect):
        return (self.rect.topleft == rect.topleft
                and self.rect.size == rect.size)

    def game(self):
        return self._stateObject.GAME

    def update(self, dt):
        self.time += dt
        if (self.can_collide() and not
                self.rect_equals(self.ent_last_rect)):
            self.update_buckets()
        self.ent_last_rect = self.rect.copy()

    def calc_bucket(self, x, y):
        return (int(x / envmanager.GRIDY), int(y / envmanager.GRIDX))

    def update_buckets(self):
        bucket = self.calc_bucket
        rect = self.rect
        newbuckets = set()
        # TODO think about the edge cases (hehe, literally)
        for x in range(rect.left - ZONEBUFFER, rect.right + ZONEBUFFER,
                       envmanager.GRIDX) + [rect.right + ZONEBUFFER]:
            for y in range(rect.top - ZONEBUFFER, rect.bottom + ZONEBUFFER,
                           envmanager.GRIDY) + [rect.bottom + ZONEBUFFER]:
                newbuckets.add(bucket(x, y))
        # The copy here is important
        # since update_buckets clobbers it as an optimization
        self._stateObject.GAME.env_manager().update_buckets(
            self, newbuckets.copy())
        self.buckets = newbuckets

    def draw(self, surface):
        """
        Default draw calls get_frame and draws that to the screen
        """
        if self.in_camera():
            frame = self.get_frame()
            if frame is not None:
                surface.blit(frame, (self.xpos, self.ypos))
            if self._stateObject.DEBUG:
                PG.draw.rect(surface, (0, 0, 0), self.rect, 2)

    def notify(self, event):
        pass

    def can_collide(self):
        return True

    def in_camera(self):
        return PS.collide_rect(self, self.camera)

    def get_frame(self):
        return None

    def should_update(self):
        return self.in_update_area()

    def in_update_area(self):
        return self.rect.colliderect(self.camera.get_update_rect())

    def mark_deleted(self):
        self.deleteme = True

    def cleanup(self):
        if self.game():
            self._stateObject.GAME.env_manager().update_buckets(self, set())
