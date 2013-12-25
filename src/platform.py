import entity
import color
import pygame.image
import pygame.mixer
import pygame as PG
import obstacle
import random
import pygame.draw
import waterdrop


class Platform(obstacle.Obstacle):

    '''
    A jumping platform
    '''
    dripsounds = None

    def __init__(self, i_x, i_y, w, h, ty, camera, imagefile, state):
        obstacle.Obstacle.__init__(self, i_x, i_y, w, h, ty, camera, state)
        self.sprite = pygame.Surface((w, h)).convert_alpha()
        self.sprite.fill((0, 0, 0, 0))
        self.tile = pygame.image.load(
            imagefile)
        self.tile = pygame.transform.smoothscale(self.tile, (50, 50))
        for y in range(0, h / 50):
            for x in range(0, w / 50):
                self.sprite.blit(self.tile, (x * 50, y * 50))
        self.ty = ty
        self.waterfreq = min(.1 * w / 50, .9)
        self.waterlogged = False
        if self.ty == "PLATFORM":
            self.waterlogged = random.random() < self.waterfreq
        self.dropint = random.randint(1, 3)
        self.droptime = random.randint(1, 100)
        self.ty = ty
        off = random.randint(0, w / 2)
        self.waterix = i_x + off
        self.wateriy = i_y + h
        self.waterwidth = random.randint(5, min(w - off, 50))
        self.drip_sound_timer = 0

        if Platform.dripsounds is None:
            Platform.dripsounds = [pygame.mixer.Sound("../Sounds/drip.ogg"),
                                   pygame.mixer.Sound("../Sounds/drip2.ogg")]
            for s in Platform.dripsounds:
                s.set_volume(0.45)
        self.channel = pygame.mixer.Channel(5)

    def update(self, dt):
        obstacle.Obstacle.update(self, dt)
        self.droptime += dt
        if self.waterlogged and self.dropint < self.droptime:
            self.droptime = 0
            self.spawndrop()
        if self.drip_sound_timer > 0:
            self.drip_sound_timer -= 1

    def draw(self, surface):
        obstacle.Obstacle.draw(self, surface)
        if self.waterlogged:
            pygame.draw.line(surface, color.DARKBLUE,
                            (self.waterix, self.wateriy),
                            (self.waterix + self.waterwidth,
                             self.wateriy))

    def get_frame(self):
        return self.sprite

    def in_update_area(self):
        return self.rect.colliderect(self.camera.get_big_update_rect())

    def spawndrop(self):
        if random.randint(1, 100) < 3:
            if self.channel.get_busy():
                self.drip_sound_timer = 100
            if self.drip_sound_timer == 0:
                self.channel.play(random.choice(Platform.dripsounds))
        drop = waterdrop.Waterdrop(
            self.waterix + self.waterwidth / 2,
            self.wateriy, self.camera, self._stateObject)
        self._stateObject.GAME.add_entity(drop)
        self._stateObject.GAME.add_mid(drop)
