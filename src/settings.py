import pygame.font as PF
import pygame.color as PC
import pygame as PG
import pygame.image as PI

import color
import state
import menu
import controls
import bubblemanager
import trans


class Settings(state.State):

    def __init__(self, stateObject):
        self._stateObject = stateObject
        self._size = 60
        self._font = PF.Font(self._stateObject.FONT, self._size)
        self._bg = PI.load("../Images/ocean_bg.png").convert()
        self._color = color.WHITE
        self._selection = 0

        self._callbacks = {
            (PG.KEYDOWN, PG.K_ESCAPE): self.__to_menu,
            (PG.KEYDOWN, PG.K_DOWN): self.__selection_down,
            (PG.KEYDOWN, PG.K_UP): self.__selection_up,
            (PG.KEYDOWN, PG.K_RETURN): self.__select
        }
        self.bubblemanager = self._stateObject.BUBBLES

    def draw(self, screen):
        self._heights = []
        screen.blit(self._bg, (0, 0))
        (width, height) = screen.get_size()
        x = 250

        self.bubblemanager.draw(screen)

        surf = self._font.render("Visual", True, self._color)
        h = surf.get_size()[1]
        y = height / 4 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(surf, (x, y))

        surf = self._font.render("Audio", True, self._color)
        h = surf.get_size()[1]
        y = 2 * height / 4 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(surf, (x, y))

        surf = self._font.render("Controls", True, self._color)
        h = surf.get_size()[1]
        y = 3 * height / 4 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(surf, (x, y))

        self._arrow = self._font.render(">", True, self._color)
        y = self._heights[self._selection]
        screen.blit(self._arrow, (x - 50, y - 5))

    def update(self, dt):
        self.bubblemanager.update(dt)

    def notify(self, event):
        if hasattr(event, "type") and hasattr(event, "key"):
            if (event.type, event.key) in self._callbacks:
                self._callbacks[(event.type, event.key)]()

    def __to_menu(self):
        self._stateObject.STATE = trans.Transition(
            self._stateObject, "right", self, self._stateObject.MENU)

    def __selection_down(self):
        self._selection = (self._selection + 1) % 3

    def __selection_up(self):
        self._selection = (self._selection - 1) % 3

    def __select(self):
        if (self._selection == 2):
            self._stateObject.STATE = trans.Transition(
                self._stateObject, "left", self,
                controls.ControlsMenu(self._stateObject))
