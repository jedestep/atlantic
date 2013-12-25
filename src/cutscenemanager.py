import entity
import pygame.image
import player
import pygame.rect
import pygame.mixer


class cutscenemanager(entity.Entity):

    def __init__(self, i_x, i_y, camera, state):
        entity.Entity.__init__(self, i_x, i_y, 2000, 600, camera, state)
        self.img = pygame.image.load("../Images/sunny.jpg").convert()
        self.airlevel = i_y + 600 - 10
        self.sound = pygame.mixer.Sound("../Sounds/level6_2.ogg")
        self.played = False
        self.subs = "Now what..."
        self.start = float('inf')
        self.time = 0

    def draw(self, canvas):
        entity.Entity.draw(self, canvas)

    def update(self, dt):
        self.time += dt
        entity.Entity.update(self, dt)
        if self.time - self.start > 5:
            self.game().load_level()

    def get_frame(self):
        return self.img

    def should_update(self):
        return True

    def notify(self, event):
        if isinstance(event, tuple):
            (nm, rpt, tgt) = event
            if isinstance(tgt, player.Player):
                if (tgt.ypos > self.airlevel):
                    tgt.jetpack.yp = 30
                    tgt.jetpack.ym = -35
                else:
                    tgt.jetpack.yp = 40
                    tgt.jetpack.ym = -8
                    if not self.played:
                        tgt.update_scoresheet()
                        self.played = True
                        self.sound.play()
                        self.game().titletext = self.subs
                        self.start = self.time
