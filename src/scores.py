import pygame.font as PF
import pygame.color as PC
import pygame as PG
import pygame.image as PI

import color
import state
import menu
import bubblemanager
import trans


class Scores(state.State):

    def __init__(self, stateObject, newscore, enter, name=""):
        self._stateObject = stateObject
        self._newscore = newscore
        self._name = name
        if self._newscore == 0:
            enter = False
        self._enter = enter
        self._bg = PI.load("../Images/ocean_bg.png").convert()
        self._color = color.WHITE
        self._hl = color.RED
        self._callbacks = {
            (PG.KEYDOWN, PG.K_ESCAPE): self.__to_menu
        }
        self.bubblemanager = self._stateObject.BUBBLES
        if self._enter:
            self._size = 100
            self._font = PF.Font(self._stateObject.FONT, self._size)
            self._name = "___"
            self._char = 0
            self._time = 140
            self._blink = self._time
            return
        self._size = 40
        self._font = PF.Font(self._stateObject.FONT, self._size)
        self._selection = 0

    def draw(self, screen):
        if self._enter:
            self.enterName(screen)
            return
        self._heights = []
        screen.blit(self._bg, (0, 0))
        (width, height) = screen.get_size()
        x = 200

        self.bubblemanager.draw(screen)

        scorefile = open("../data/hs", 'r')
        self.scorelist = scorefile.readlines()
        isHS = False
        for i in xrange(0, len(self.scorelist)):
            score = self.scorelist[i].split(' ')[1]
            if float(score) == round(self._newscore, 3):
                color = self._hl
                isHS = True
            else:
                color = self._color
            surf = self._font.render(str(i + 1) + ". " + self.scorelist[i],
                                     True, color)
            h = surf.get_size()[1]
            y = ((i + 1) * height) / 10 - h / 2 + self._size - 20
            screen.blit(surf, (x, y))
        if not isHS and self._newscore > 0:
            surf = self._font.render("... " + self._name + " "
                                     + str(self._newscore), True, self._hl)
            h = surf.get_size()[1]
            y = (9 * height) / 10 - h / 2 + self._size - 20
            screen.blit(surf, (x, y))

    def enterName(self, screen):
        screen.blit(self._bg, (0, 0))
        (width, height) = screen.get_size()
        ins = self._font.render("Enter Name:", True, self._color)
        (w, h) = ins.get_size()
        screen.blit(ins, ((width / 2) - (w / 2), (height / 2) - h))

        name = self._font.render(self._name, True, self._color)
        (w, h) = name.get_size()
        screen.blit(name, ((width / 2) - (w / 2), (height / 2)))

    def update(self, dt):
        self.bubblemanager.update(dt)
        if self._enter:
            c = '_'
            if self._blink <= self._time / 2:
                c = ' '
            self._name = self._name[:self._char] + c \
                + self._name[self._char + 1:]
            self._name = self._name[:3]
            self._blink -= 1
            if self._blink <= 0:
                self._blink = self._time

    def notify(self, event):
        if hasattr(event, "type") and hasattr(event, "orig_key"):
            if self._enter and event.type == PG.KEYDOWN:
                key = PG.key.name(event.orig_key).upper()
                if key.isalpha() and len(key) == 1 and self._char < 3:
                    self._name = self._name[:self._char] + key \
                        + self._name[self._char + 1:]
                    self._char += 1
                if key == "BACKSPACE" and self._char > 0:
                    self._name = self._name[:self._char - 1] + '__' \
                        + self._name[self._char + 1:]
                    self._name = self._name[:3]
                    self._char -= 1
                if key == "RETURN" and self._char == 3:
                    self.saveScore()
                    self._stateObject.STATE = \
                        Scores(self._stateObject, self._newscore, False,
                               self._name)
            if (event.type, event.key) in self._callbacks:
                self._callbacks[(event.type, event.key)]()

    def saveScore(self):
        # formatted like "AAA ######"
        scorefile = open("../data/hs", 'r')
        self.scorelist = scorefile.readlines()
        self.scorelist.append(self._name + " " + str(self._newscore) + "\n")
# TODO: sort by int, not string
        self.scorelist.sort(key=lambda x: float(x.split()[1]))
        self.scorelist = self.scorelist[:8]
        scorefile.close()

        scorefile = open("../data/hs", 'w')
        for s in self.scorelist:
            scorefile.write(s)
        scorefile.close()

    def __to_menu(self):
        self._stateObject.STATE = trans.Transition(
            self._stateObject, "right", self, self._stateObject.MENU)
