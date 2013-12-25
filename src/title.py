import pygame.font as PF
import pygame.color as PC
import pygame.image as PI
import pygame.mixer as PM
import pygame as PG

import color
import game
import menu
import state


class Title(state.State):

    def __init__(self, stateObject):
        self._stateObject = stateObject
        self._size = 80
        self._font = PF.Font(self._stateObject.FONT, self._size)
        self._bg = PI.load("../Images/ocean_bg.png").convert()
        self._sound = PM.Sound("../Sounds/titleSound.ogg")
        self._color = color.BLACK
        self._time = 0
        self._fadein = 60
        self._callbacks = {
            (PG.KEYDOWN, PG.K_SPACE): self.__to_menu
        }
        self._sound.play()

    def draw(self, screen):
        screen.blit(self._bg, (0, 0))
        (width, height) = screen.get_size()
        # Uncenter the text so the rotation looks nicer
        surf = self._font.render("            Atlantic Rim",
                                 True,
                                 self._color)
        surf = PG.transform.rotozoom(surf, self._time / 3, 1)
        (w, h) = surf.get_size()
        screen.blit(surf, (width / 2 - w / 1.4 - self._time,
                           height / 2 - h / 2 - self._time))
        back = PG.surface.Surface(screen.get_size())
        back.set_alpha(255 * self._time / self._fadein)
        screen.blit(back, (0, 0))

    def update(self, dt):
        dt *= 10
        self._time += dt
        if self._time < self._fadein:
            ratio = self._time / self._fadein
            value = int(ratio * 255)
        else:
            self.__to_menu()

    def notify(self, event):
        if hasattr(event, "type") and hasattr(event, "key"):
            if (event.type, event.key) in self._callbacks:
                self._callbacks[(event.type, event.key)]()

    def __to_menu(self):
        self._sound.fadeout(500)
        self._stateObject.MENU = menu.Menu(self._stateObject)
        self._stateObject.STATE = self._stateObject.MENU
