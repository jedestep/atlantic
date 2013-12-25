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
import levelselect
import bubblemanager
import trans
import os
import confirmmenu


class Menu(state.State):

    def __init__(self, stateObject):
        self._stateObject = stateObject
        self._size = 60
        self._font = PF.Font(self._stateObject.FONT, self._size)
        self._bg = PI.load("../Images/ocean_bg.png").convert()
        self._sound = PM.Sound("../Sounds/menuLoop.ogg")
        self._color = color.WHITE
        self._time = 0
        self._fadein = 5
        self._selection = 0
        self._callbacks = {
            (PG.KEYDOWN, PG.K_DOWN): self.__selection_down,
            (PG.KEYDOWN, PG.K_UP): self.__selection_up,
            (PG.KEYDOWN, PG.K_RETURN): self.__select
        }
        PM.Channel(1).play(self._sound, -1)
        self.bubblemanager = self._stateObject.BUBBLES
        self.save = ""
        self.score = 0
        if os.path.exists("../data/save"):
            with open("../data/save") as f:
                lines = f.readlines()
                self.save = lines[0].strip()
                if len(lines) > 1:
                    self.score = float(lines[1].strip())
                else:
                    self.score = 0

    def draw(self, screen):
        self._heights = []
        screen.blit(self._bg, (0, 0))
        (width, height) = screen.get_size()
        x = 250

        self.bubblemanager.draw(screen)

        self._play = self._font.render("Play", True, self._color)
        h = self._play.get_size()[1]
        y = 0 * height / 6 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(self._play, (x, y))

        self._play = self._font.render(
            "Continue", True, self._color if self.save else (150, 150, 150))
        h = self._play.get_size()[1]
        y = height / 6 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(self._play, (x, y))

        self._play = self._font.render("Level Select", True, self._color)
        h = self._play.get_size()[1]
        y = 2 * height / 6 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(self._play, (x, y))

        self._settings = self._font.render("Settings", True, self._color)
        h = self._settings.get_size()[1]
        y = 3 * height / 6 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(self._settings, (x, y))

        self._scores = self._font.render("High Scores", True, self._color)
        h = self._scores.get_size()[1]
        y = 4 * height / 6 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(self._scores, (x, y))

        self._quit = self._font.render("Quit", True, self._color)
        h = self._quit.get_size()[1]
        y = 5 * height / 6 - h / 2 + self._size
        self._heights.append(y)
        screen.blit(self._quit, (x, y))

        self._arrow = self._font.render(">", True, self._color)
        y = self._heights[self._selection]
        screen.blit(self._arrow, (x - 50, y - 5))

    def update(self, dt):
        self.bubblemanager.update(dt)
        dt *= 10
        self._time += dt
        if self._time < self._fadein:
            ratio = self._time / self._fadein
            value = int(ratio * 255)
            self._color = PC.Color(value, value, value)

    def notify(self, event):
        if hasattr(event, "type") and hasattr(event, "key"):
            if (event.type, event.key) in self._callbacks:
                self._callbacks[(event.type, event.key)]()

    def __selection_down(self):
        self._selection = (self._selection + 1) % 6
        if self._selection == 1 and not self.save:
            self._selection += 1

    def __selection_up(self):
        self._selection = (self._selection - 1) % 6
        if self._selection == 1 and not self.save:
            self._selection -= 1

    def __select(self):
        {
            0: self.__to_game,
            1: self.__to_resume,
            2: self.__to_level_select,
            3: self.__to_settings,
            4: self.__to_scores,
            5: self.__quit
        }[self._selection]()

    def __to_game(self):
        self._sound.fadeout(200)
        if self._stateObject.GAME is None:
            if self.save:
                self._stateObject.STATE = trans.Transition(
                    self._stateObject, "left", self,
                    confirmmenu.ConfirmMenu(self._stateObject))
            else:
                self._stateObject.GAME = game.Game(self._stateObject)
                self._stateObject.STATE = self._stateObject.GAME
            return
        self._stateObject.GAME._channel.unpause()
        self._stateObject.STATE = self._stateObject.GAME

    def __to_resume(self):
        self._sound.fadeout(200)
        if self._stateObject.GAME is None:
            if self.save:
                self._stateObject.GAME = game.Game(
                    self._stateObject, self.save)
                self._stateObject.GAME.showtime = True
                self._stateObject.GAME.time = float(self.score)
                self._stateObject.STATE = self._stateObject.GAME
            return
        self._stateObject.GAME._channel.unpause()
        self._stateObject.STATE = self._stateObject.GAME

    def __to_level_select(self):
        self._stateObject.STATE = trans.Transition(
            self._stateObject, "left", self,
            levelselect.LevelSelect(self._stateObject))

    def __to_settings(self):
        self._stateObject.STATE = trans.Transition(
            self._stateObject, "left", self,
            settings.Settings(self._stateObject))

    def __to_scores(self):
        self._stateObject.STATE = trans.Transition(
            self._stateObject, "left", self,
            scores.Scores(self._stateObject, -1, False))

    def __quit(self):
        PE.post(PE.Event(PG.QUIT, {}))
