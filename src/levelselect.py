import pygame.event as PE
import pygame.font as PF
import pygame.color as PC
import pygame.mixer as PM
import pygame as PG
import pygame.image as PI

import sys
import color
import game
import scores
import state
import settings
import menu
import bubblemanager
import trans


class LevelSelect(state.State):

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
        self.levels = [
            "../Levels/Level1.txt",
            "../Levels/Level2.txt",
            "../Levels/Level4.txt",
            "../Levels/Level5.txt",
            "../Levels/Level3.txt",
            "../Levels/finalcutscene.txt"
        ]
        self.bubblemanager = self._stateObject.BUBBLES

    def draw(self, screen):
        self._heights = []
        screen.blit(self._bg, (0, 0))
        (width, height) = screen.get_size()
        x = 250

        self.bubblemanager.draw(screen)

        for i in xrange(len(self.levels)):
            self._play = self._font.render(
                "Level " + str(i + 1), True, self._color)
            h = self._play.get_size()[1]
            y = (i) * height / 6 - h / 2 + self._size
            self._heights.append(y)
            screen.blit(self._play, (x, y))

        self._arrow = self._font.render(">", True, self._color)
        y = self._heights[self._selection]
        screen.blit(self._arrow, (x - 50, y - 5))

    def update(self, dt):
        self.bubblemanager.update(dt)

    def notify(self, event):
        if hasattr(event, "type") and hasattr(event, "key"):
            if (event.type, event.key) in self._callbacks:
                self._callbacks[(event.type, event.key)]()

    def __selection_down(self):
        self._selection = (self._selection + 1) % (len(self.levels))

    def __selection_up(self):
        self._selection = (self._selection - 1) % (len(self.levels))

    def __select(self):
        self.__to_game()

    def __to_menu(self):
        self._stateObject.STATE = trans.Transition(
            self._stateObject, "right", self,
            self._stateObject.MENU)

    def __to_game(self):
        PM.Channel(3).fadeout(200)
        PM.Channel(1).unpause()
        PM.Channel(1).stop()
        self._stateObject.GAME = game.Game(
            self._stateObject, self.levels[self._selection])
        self._stateObject.GAME.showtime = (self._selection == 0)
        self._stateObject.STATE = self._stateObject.GAME
        return
