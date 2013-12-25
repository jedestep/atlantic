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

import pygame.key


def invertDictionary(orig_dict):
    result = {}  # or change to defaultdict(list)
    for k, v in orig_dict.iteritems():
        result.setdefault(v, []).append(k)
    return result


class ControlsMenu(state.State):

    def __init__(self, stateObject):
        self._stateObject = stateObject
        self._size = 60
        self._font = PF.Font(self._stateObject.FONT, self._size)
        self._bg = PI.load("../Images/ocean_bg.png").convert()
        self._color = color.WHITE
        self._selection = 0
        self._callbacks = {
            (PG.KEYDOWN, PG.K_ESCAPE): self.__esc,
            (PG.KEYDOWN, PG.K_DOWN): self.__selection_down,
            (PG.KEYDOWN, PG.K_UP): self.__selection_up,
            (PG.KEYDOWN, PG.K_RETURN): self.__select
        }
        self.config = self._stateObject.CONFIG
        self.options = self._stateObject.CONFIG.internal_buttons
        self.num_opts = len(self.options)
        self.waiting = False
        self.waiting_key = -1
        self.invdicts()
        self.just_reset = False
        self.bubblemanager = self._stateObject.BUBBLES
        self.controller = self._font.render("Controller", True, self._color)

    def invdicts(self):
        self.invdict = invertDictionary(self.config.keymapping)
        self.invjoybutton = invertDictionary(self.config.button_scheme)
        self.invaxis_scheme = invertDictionary(self.config.axis_scheme)
        self.invhat_scheme = invertDictionary(self.config.hat_scheme)

    def draw(self, screen):
        self._heights = []
        screen.blit(self._bg, (0, 0))
        (width, height) = screen.get_size()
        x1 = 20
        x2 = 450
        y = 265
        y2 = 320
        y3 = 375
        self.bubblemanager.draw(screen)

        #special
        if self._selection == self.num_opts:
            action = self._font.render("Reset to default", True, self._color)
            screen.blit(action, (x1, y))
            if self.just_reset:
                done = self._font.render("Done", True, self._color)
                screen.blit(done, (600, y))
        else:
            selected_internal_key = self.options[self._selection]
            action = self._font.render(
                self.config.keydesc[self.options[self._selection]] + ":",
                True, self._color)
            screen.blit(action, (x1, y))
            _keys = self.invdict.get(selected_internal_key, [])
            currkey = self._font.render(", ".join(
                pygame.key.name(x) for x in _keys if x >= 0),
                True, self._color)
            screen.blit(currkey, (x2, y))

            KD = pygame.KEYDOWN
            if selected_internal_key in self.invjoybutton:
                screen.blit(self.controller, (x1, y2))
                jb = self._font.render(
                    "Button " + str(
                        self.invjoybutton[selected_internal_key][0]),
                    True, self._color)
                screen.blit(jb, (x2, y2))
            elif (KD, selected_internal_key) in self.invaxis_scheme:
                screen.blit(self.controller, (x1, y2))
                val = self.invaxis_scheme[(KD, selected_internal_key)][0]
                jb = self._font.render("Axis " + str(val[0]),
                                       True, self._color)
                screen.blit(jb, (x2, y2))
                jb = self._font.render("Direction " + str(val[1]),
                                       True, self._color)
                screen.blit(jb, (x2, y3))
            elif (KD, selected_internal_key) in self.invhat_scheme:
                screen.blit(self.controller, (x1, y2))
                val = self.invhat_scheme[(KD, selected_internal_key)][0]
                jb = self._font.render("Hat " + str(val[0]), True, self._color)
                screen.blit(jb, (x2, y2))
                jb = self._font.render("Direction " + str(val[1]),
                                       True, self._color)
                screen.blit(jb, (x2, y3))

    def update(self, dt):
        self.bubblemanager.update(dt)

    def notify(self, event):
        if self.waiting:
            if hasattr(event, "type") and hasattr(event, "orig_key"):
                if event.type == pygame.KEYDOWN:
                    kc = event.orig_key
                    if (kc != pygame.K_RETURN
                            and kc != pygame.K_ESCAPE
                            and kc != pygame.K_UP
                            and kc != pygame.K_DOWN):
                        selected_key = event.orig_key
                        self.config.keymapping[selected_key] = self.waiting_key
                        self.waiting = False
                        self.config.restore_important_keys()
                        self.invdicts()

        else:
            if hasattr(event, "type") and hasattr(event, "orig_key"):
                if (event.type, event.orig_key) in self._callbacks:
                    self._callbacks[(event.type, event.orig_key)]()

    def __selection_down(self):
        self.just_reset = False
        self._selection = (self._selection + 1) % (len(self.options) + 1)

    def __selection_up(self):
        self.just_reset = False
        self._selection = (self._selection - 1) % (len(self.options) + 1)

    def __select(self):
        if self._selection == len(self.options):
            self.config.reset()
            self.invdicts()
            self.just_reset = True
        else:
            self.just_reset = False
            self.waiting = True
            self.waiting_key = self.options[self._selection]
            if self.waiting_key in self.invdict:
                for k in self.invdict[self.waiting_key]:
                    del self.config.keymapping[k]
                self.invdict[self.waiting_key] = []

    def __esc(self):
        if self.waiting:
            self.waiting = False
        else:
            self.__back()

    def __back(self):
        self._stateObject.CONFIG.save_config("../data/keys")
        self._stateObject.STATE = trans.Transition(
            self._stateObject, "right", self,
            settings.Settings(self._stateObject))
