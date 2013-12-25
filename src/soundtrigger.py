import trigger
import color
import pygame
import pygame.mixer
import pygame.font


class SoundTrigger(trigger.Trigger):
    def __init__(self, i_x, i_y, w, h, camera, state):
        trigger.Trigger.__init__(self, i_x, i_y, w, h, camera, state)
        self.sound = None
        self.channel = pygame.mixer.Channel(2)
        self.channel.set_endevent(pygame.USEREVENT + 2)

    def trigger(self):
        if self.sound is not None:
            self.channel.play(self.sound)

    def notify(self, event):
        note = trigger.Trigger.notify(self, event)
        if note == 1:
            self.game().titletext = self.text
            return
        elif note == -1:
            if event.type == pygame.USEREVENT + 2:
                self.game().titletext = ""

    def set_sound(self, sound):
        self.sound = sound

    def set_text(self, text):
        self.text = text
