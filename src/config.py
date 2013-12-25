import pygame
import pickle


class Configuration(object):
    def __init__(self):
        self.button_scheme = {}
        self.keydesc = {
            pygame.K_SPACE: "Jump",
            pygame.K_LEFT: "Move Left",
            pygame.K_RIGHT: "Move Right",
            pygame.K_w: "Shoot Up",
            pygame.K_a: "Shoot Left",
            pygame.K_s: "Shoot Down",
            pygame.K_d: "Shoot Right",
        }
        self.internal_buttons = [
            pygame.K_SPACE,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_w,
            pygame.K_a,
            pygame.K_s,
            pygame.K_d]

    def load_config(self, filename):
        try:
            saved = None
            with open(filename, "r") as f:
                saved = pickle.load(f)
            self.button_scheme = saved["button_scheme"]
            self.axis_scheme = saved["axis_scheme"]
            self.hat_scheme = saved["hat_scheme"]
            self.keymapping = saved["keymapping"]
        except Exception:
            self.reset()

    def restore_important_keys(self):
        self.keymapping[pygame.K_RETURN] = pygame.K_RETURN
        self.keymapping[pygame.K_ESCAPE] = pygame.K_ESCAPE

    def reset(self):
        KD = pygame.KEYDOWN
        KU = pygame.KEYUP
        self.button_scheme = {
            0: pygame.K_a,
            1: pygame.K_s,
            2: pygame.K_d,
            3: pygame.K_w,
            4: pygame.K_RETURN,
            5: pygame.K_SPACE,
            9: pygame.K_ESCAPE
        }
        self.axis_scheme = {
            #axis num, axis val: key stuff
            (0, 0): (KU, pygame.K_RIGHT),
            (0, -1): (KD, pygame.K_LEFT),
            (0, 1): (KD, pygame.K_RIGHT),
            (1, 0): (KU, pygame.K_RIGHT),
            (1, -1): (KD, pygame.K_UP),
            (1, 1): (KD, pygame.K_DOWN)
        }
        self.hat_scheme = {
            (0, 0): (KU, pygame.K_RIGHT),
            (1, 0): (KD, pygame.K_RIGHT),
            (-1, 0): (KD, pygame.K_LEFT),
            (0, 1): (KD, pygame.K_UP),
            (0, -1): (KD, pygame.K_DOWN)
        }
        self.keymapping = {
            pygame.K_RETURN: pygame.K_RETURN,
            pygame.K_SPACE: pygame.K_SPACE,
            pygame.K_LEFT: pygame.K_LEFT,
            pygame.K_RIGHT: pygame.K_RIGHT,
            pygame.K_ESCAPE: pygame.K_ESCAPE,
            pygame.K_w: pygame.K_w,
            pygame.K_a: pygame.K_a,
            pygame.K_s: pygame.K_s,
            pygame.K_d: pygame.K_d,
            pygame.K_UP: pygame.K_UP,
            pygame.K_DOWN: pygame.K_DOWN
        }
        self.save_config("../data/keys")

    def save_config(self, filename):
        savedict = {
            "button_scheme": self.button_scheme,
            "keymapping": self.keymapping,
            "hat_scheme": self.hat_scheme,
            "axis_scheme": self.axis_scheme
        }
        with open(filename, "w+") as f:
            pickle.dump(savedict, f)
