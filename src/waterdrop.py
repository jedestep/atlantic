import phys
import pygame.draw
import obstacle
import pygame.rect


class Waterdrop(phys.PhysEntity):
    def __init__(self, x, y, camera, state):
        phys.PhysEntity.__init__(self, x, y, 1, 3, camera, state)
        self.time = 0
        self.yacc = 6

    def draw(self, canvas):
        phys.PhysEntity.draw(self, canvas)
        pygame.draw.line(canvas, (0, 0, 255),
                         (self.xpos, self.ypos),
                         (self.xpos, self.ypos + 3))

    def update(self, dt):
        phys.PhysEntity.update(self, dt)
        self.time += dt
        if self.time > 10 or not self.in_update_area():
            self.remove()

    def _halt(self, name, reporter, target):
        self.remove()

    def should_update(self):
        return True

    def remove(self):
        self.game().remove_entity(self)
