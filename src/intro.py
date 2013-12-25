import pygame.image
import pygame
import entity
import pygame.transform
import cutscene


class Intro(cutscene.Cutscene):
    def __init__(self, camera, state):
        cutscene.Cutscene.__init__(self, 0, 0, 800, 600, camera, state, None)
        self.door = pygame.image.load("../Images/doors.png")
        self.scene = pygame.image.load("../Images/scene.png")
        self.hud = [pygame.image.load("../Images/HUD1.png"),
                    pygame.image.load("../Images/HUD2.png")]
        self.time = 0
        self.canvas = pygame.Surface((800, 600))
        self.anim_start = float("inf")

    def draw(self, final):
        canvas = self.canvas
        canvas.fill((0, 0, 0))
        offset = 0
        offset = (((self.time - self.anim_start) * 140)
                  if self.time > self.anim_start else 0)
        canvas.blit(self.door, (218, 106 - offset))
        canvas.blit(self.scene, (0, 0))
        if self.time > self.anim_start:
            canvas = pygame.transform.rotozoom(
                canvas, self.time - self.anim_start,
                (self.time - self.anim_start) / 5.0 + 1)
        x = ((self.time - self.anim_start) * 80
             if self.time > self.anim_start else 0)
        y = x * .7
        final.blit(canvas, (-1 * x, -1 * y))
        final.blit(self.hud[int(self.time) % 2], (0, 0))

    def update(self, dt):
        cutscene.Cutscene.update(self, dt)
        self.time += dt
        if self.time > self.anim_start + 7:
            self._stateObject.GAME.load_level()

    def notify(self, event):
        if hasattr(event, "type") and hasattr(event, "key") and \
                event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.anim_start == float('inf'):
                    self.anim_start = self.time
        if hasattr(event, "type") and hasattr(event, "key") and \
                event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._stateObject.GAME.load_level()
