#!/usr/bin/python

import pygame
import pygame.image as PI
import pygame.font as PF
import pygame.time
import pygame.event
import pygame.display
import pygame.key
import pygame.joystick

import game
import globState
import player
import enemy
import obstacle
import title
import config

import color

import random

import bubblemanager

'''
This module serves as the launcher to the game.
For now, all it does is adds some stuff to the scene
In the future, it will only be responsible for launching the game,
no scene stuff
'''


class Atlantic:

    def initialize(self):
        pygame.init()
        pygame.joystick.init()
        self._globalState = globState.GlobalState()
        self._globalState.DEBUG = False
        self._globalState.SCREEN = pygame.display.set_mode((800, 600))
        self._globalState.CLOCK = pygame.time.Clock()
        self._globalState.RUNNING = True
        self._globalState.FONT = "../Fonts/Devil Breeze Demi.otf"
        self._globalState.STATE = title.Title(self._globalState)
        self._globalState.CONFIG = config.Configuration()
        # self._globalState.CONFIG.reset()
        # self._globalState.CONFIG.save_config("../data/keys")
        self._globalState.CONFIG.load_config("../data/keys")

        if pygame.joystick.get_count() > 0:
            self._globalState.JOYSTICK = pygame.joystick.Joystick(0)
            self._globalState.JOYSTICK.init()

        self._globalState.BUBBLES = bubblemanager.BubbleManager(
            self._globalState)

    def transform_key(self, unmappedevent):
        mapping = self._globalState.CONFIG.keymapping
        mapped_event = unmappedevent
        if hasattr(unmappedevent, "key"):
            orig_key = unmappedevent.key
            if unmappedevent.key in mapping:
                key = mapping[unmappedevent.key]
            else:
                key = 1000000
            mapped_event = pygame.event.Event(
                unmappedevent.type,
                {"key": key, "orig_key": orig_key})
        return mapped_event

    def loop(self):
        clock = pygame.time.Clock()
        last_time = clock.tick()
        accumulated_time = 0.0
        INTERVAL = .005
        while self._globalState.RUNNING:
            frame_time = clock.tick() / 1000.0

            self._globalState.CLOCK.tick()
            self._globalState.SCREEN.fill(color.WHITE)
            self._globalState.STATE.draw(self._globalState.SCREEN)

            pygame.display.flip()

            accumulated_time += frame_time
            while accumulated_time > INTERVAL:
                self._globalState.STATE.update(INTERVAL)
                accumulated_time -= INTERVAL
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self._globalState.RUNNING = False
                    else:
                        event = None
                        a_conf = self._globalState.CONFIG.axis_scheme
                        b_conf = self._globalState.CONFIG.button_scheme
                        h_conf = self._globalState.CONFIG.hat_scheme
                        KD = pygame.KEYDOWN
                        KU = pygame.KEYUP
                        buttonupdownmap = {pygame.JOYBUTTONDOWN: KD,
                                           pygame.JOYBUTTONUP: KU}
                        if (e.type == pygame.JOYBUTTONDOWN
                                or e.type == pygame.JOYBUTTONUP):
                            raw = e.button
                            if raw in b_conf:
                                event = pygame.event.Event(
                                    buttonupdownmap[e.type],
                                    {'key': b_conf[raw]})
                        elif e.type == pygame.JOYAXISMOTION:
                            k = (e.axis, int(e.value))
                            if k in a_conf:
                                (kdir, kval) = a_conf[k]
                                event = pygame.event.Event(
                                    kdir,
                                    {'key': kval})

                        elif e.type == pygame.JOYHATMOTION:
                            if e.value in h_conf:
                                (kdir, kval) = h_conf[e.value]
                                event = pygame.event.Event(
                                    kdir,
                                    {'key': kval})
                        else:
                            event = e
                        if event:
                            self._globalState.STATE.notify(
                                self.transform_key(event))

    def end(self):
        pygame.joystick.quit()
        pygame.quit()


def main():
    a = Atlantic()
    a.initialize()
    a.loop()
    a.end()

if __name__ == "__main__":
    main()
