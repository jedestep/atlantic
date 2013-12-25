#! /usr/bin/python
import pygame as PG
import pygame.display
import pygame.image as PI
import pygame.font as PF
import pygame.mixer as PM
import pygame.time
import pygame.event
import pygame.draw

import pygame.image
import pygame.transform

import debuginfo
import color
import phys
import inputmanager
import envmanager
import player
import obstacle
import platform
import enemy
import levelbuilder
import camera
import lasershot
import trigger

import state
import menu
import random
import cutscene

import trans


class Game(state.State):

    '''
    The main game class. This is in charge of handling the game loop and
    other important thing, like providing access to various services
    (eg, the input manager).
    '''

    def init(self):
        self._callbacks = {
            (PG.KEYDOWN, PG.K_ESCAPE): self.__to_menu,
            (PG.KEYDOWN, PG.K_EQUALS): self.load_level
        }
        self.init_input_manager()
        # self.init_debug_mode()
        self.init_level_builder()
        self.toadd = set()
        self.bg = None
        self.init_env_manager()
        self.init_entities(self.levelname)
        self.ambient = PI.load("../Images/waterTile.png").convert()

        self.clock = pygame.time.Clock()

        self.time = 0
        self.font = PF.Font(self._stateObject.FONT, 40)
        self.smallfont = PF.Font(self._stateObject.FONT, 26)
        self.nc = PG.Surface((self.level_w - 50, self.level_h),
                             pygame.SRCALPHA, 32)
        self.nc = self.nc.convert_alpha()
        self.posts = []

    def __init__(self, stateObject, levelname="../Levels/cutscene1.txt"):
        self._stateObject = stateObject
        self.levelname = levelname
        self.player = None
        #This is the list of functions to run after the update has completed
        #This is important because we typically don't
        #want to make any global changes to the state
        #in the middle of an update
        self.run_after_update = []
        self.init()
        self._channel = PM.Channel(1)
        self._intro = PM.Sound("../Sounds/mainIntro.ogg")
        self._sound = PM.Sound("../Sounds/mainLoop.ogg")
        #  mystery crash
        if self._channel is not None:
            self._channel.play(self._intro)
        self.showtime = False
        self._channel.set_endevent(pygame.USEREVENT + 1)
        self.titletext = ""

    def init_env_manager(self):
        self._env_manager = envmanager.EnvironmentManager(self._stateObject)

    def init_input_manager(self):
        self._input_manager = inputmanager.InputManager(self._stateObject)

    def init_debug_mode(self):
        self._debug = False
        self._debug_info = debuginfo.DebugInfo(self._stateObject)

    def init_level_builder(self):
        self._builder = levelbuilder.LevelBuilder(self._stateObject)

    def player_die(self):
        self.run_after_update.append(lambda: self.__player_die())

    def __player_die(self):
        self._channel.stop()
        self._stateObject.STATE = menu.Menu(self._stateObject)
        self._stateObject.GAME = None

    def add_post_step(self, func):
        self.posts.append(func)

    def load_level(self):
        changed = False
        if self.levelname == "../Levels/cutscene1.txt":
            changed = True
            self.levelname = "../Levels/Level1.txt"
            self.run_after_update.append(self.init)
            self.time = 0
            self.showtime = True
        elif self.levelname == "../Levels/Level1.txt":
            changed = True
            self.levelname = "../Levels/Level2.txt"
            self.run_after_update.append(self.init)
            if self.player is not None:
                score = self.player.score
                self.run_after_update.append(
                    lambda: self.update_player_score(score))
        elif self.levelname == "../Levels/Level2.txt":
            changed = True
            self.levelname = "../Levels/Level4.txt"
            self.run_after_update.append(self.init)
            if self.player is not None:
                score = self.player.score
                self.run_after_update.append(
                    lambda: self.update_player_score(score))
        elif self.levelname == "../Levels/Level4.txt":
            changed = True
            self.levelname = "../Levels/Level5.txt"
            self.run_after_update.append(self.init)
            if self.player is not None:
                score = self.player.score
                self.run_after_update.append(
                    lambda: self.update_player_score(score))
        elif self.levelname == "../Levels/Level5.txt":
            changed = True
            self.levelname = "../Levels/Level3.txt"
            self.run_after_update.append(self.init)
            if self.player is not None:
                score = self.player.score
                self.run_after_update.append(
                    lambda: self.update_player_score(score))
        elif self.levelname == "../Levels/Level3.txt":
            changed = True
            self.levelname = "../Levels/finalcutscene.txt"
            self.run_after_update.append(self.init)
            if self.player is not None:
                score = self.player.score
                self.run_after_update.append(
                    lambda: self.update_player_score(score))
        elif self.levelname == "../Levels/finalcutscene.txt":
            changed = True
            self.run_after_update.append(self.player_win)
        if changed:
            self.posts = []
            #Put stuff that happens on each level change here
            self._channel.stop()
            if self.showtime:
                with open("../data/save", 'w+') as f:
                    f.write(self.levelname + "\n")
                    if self.player is not None:
                        f.write(str(self.player.score))

    def player_win(self):
        self._stateObject.GAME._channel.stop()
        self._stateObject.STATE = trans.Transition(
            self._stateObject, "black", self,
            self.player.scoresheet, 4.0)
        self._stateObject.GAME = None

    def update_player_score(self, score):
        self.time = score
        self.player.score = score

    def process_after_update(self):
        for func in self.run_after_update:
            func()
        self.run_after_update = []

    def init_entities(self, levelname):
        self._entities = set()

        #build the level from the txt file
        t = self._builder.buildLevel(levelname)
        temp = t[0]
        self.level_w = t[1][0]
        self.level_h = t[1][1]
        self.boss = pygame.sprite.Group()
        self.boss = t[2]
        self.back = pygame.sprite.Group()
        self.back = t[3]
        self.mid = pygame.sprite.Group()
        self.mid = t[4]
        self.front = pygame.sprite.Group()
        self.front = t[5]
        self.bg = t[6]
        self.bgw = self.bg.get_width()
        self.bgh = self.bg.get_height()
        #print "(%d,%d)" % (self.level_w,self.level_h)

        #add the entities to the game
        for x in temp:
            self.add_entity(x)
            if(isinstance(x, player.Player)):
                self.player = x
                self.input_manager().add_subscriber(x)
                self.env_manager().add_subscriber(x)
            if(isinstance(x, enemy.Enemy)):
                self.env_manager().add_subscriber(x)
            if(isinstance(x, cutscene.Cutscene)):
                self.input_manager().add_subscriber(x)
            if(isinstance(x, trigger.Trigger)):
                self.input_manager().add_subscriber(x)
            if isinstance(x, camera.Camera):
                self.camera = x
                self.input_manager().add_subscriber(x)

    def notify(self, event):
        self.input_manager().update(event)
        if event.type == pygame.USEREVENT + 1:
            if not self._channel.get_busy():
                self._channel.play(self._sound, -1)
        if hasattr(event, "type") and hasattr(event, "key"):
            if (event.type, event.key) in self._callbacks:
                self._callbacks[(event.type, event.key)]()

    def update(self, dt):
        # self._debug_info.update(dt)
        # print len(self._entities)
        todelete = set()
        for ent in self._entities:
            if self._stateObject is None:
                break
            # self._input_manager.update(dt)
            if ent.should_update():
                ent.update(dt)
            if ent.deleteme:
                todelete.add(ent)
        if self.player:
            self.player.score = self.time

        self._env_manager.update(dt)

        # the copy so that we don't get
        # 'set changed during iteration' if someone adds inside an add
        for ent in self.toadd:
            self._entities.add(ent)
        self.toadd.clear()

        for ent in todelete:
            ent.cleanup()
            self._entities.remove(ent)
        todelete = None  # spur gc

        self.process_after_update()

    def draw(self, canvas):
        parallax = .5
        bgw = self.bgw
        bgh = self.bgh
        progx = (self.camera.xpos * parallax) % (bgw)
        progy = (self.camera.ypos * parallax) % (bgh)
        self.nc.blit(self.bg, (self.camera.xpos, self.camera.ypos),
                     pygame.Rect(progx, progy, bgw - progx, bgh - progy))
        self.nc.blit(self.bg, (self.camera.xpos + self.bgw - progx - 1,
                               self.camera.ypos),
                     pygame.Rect(0, progy, 800 - bgw + progx, bgh - progy))
        self.nc.blit(self.bg, (self.camera.xpos,
                               self.camera.ypos + self.bgh - progy - 1),
                     pygame.Rect(progx, 0, bgw - progx, 600 - bgh + progy))
        self.nc.blit(self.bg, (self.camera.xpos + self.bgw - progx - 1,
                               self.camera.ypos + self.bgh - progy - 1),
                     pygame.Rect(0, 0, 800 - bgw + progx, 600 - bgh + progy))

        if self._stateObject.DEBUG:
            pygame.draw.rect(self.nc, (255, 0, 0),
                             pygame.Rect(self.camera.xpos,
                                         self.camera.ypos, bgw - progx,
                                         bgh - progy), 5)
            pygame.draw.rect(self.nc, (0, 255, 0),
                             pygame.Rect(self.camera.xpos + self.bgw - progx,
                                         self.camera.ypos, 800 - bgw + progx,
                                         bgh - progy), 5)
            pygame.draw.rect(self.nc, (0, 0, 255),
                             pygame.Rect(self.camera.xpos,
                                         self.camera.ypos + self.bgh - progy,
                                         bgw - progx, 600 - bgh + progy), 5)
            pygame.draw.rect(self.nc, (255, 255, 0),
                             pygame.Rect(self.camera.xpos + self.bgw - progx,
                                         self.camera.ypos + self.bgh - progy,
                                         800 - bgw + progx,
                                         600 - bgh + progy), 5)

        if self._stateObject.DEBUG:
            self._env_manager.draw_grid(self.nc)
        for entity in self.boss:
            if entity.should_update():
                entity.draw(self.nc)
        for entity in self.back:
            if entity.should_update():
                entity.draw(self.nc)
        for entity in self.mid:
            if entity.should_update():
                entity.draw(self.nc)
        for entity in self.front:
            if entity.should_update():
                entity.draw(self.nc)
        r = pygame.Rect(self.camera.xpos,
                        self.camera.ypos, 800, 600)
        canvas.blit(self.ambient, (0, 0))
        canvas.blit(self.nc, (0, 0), r)

        if self.showtime:
            # draw the timer
            tsurf = self.font.render(str(self.time), True, color.WHITE)
            self.time += self.clock.tick() / 1000.0

            canvas.blit(tsurf, (25, 25))
        if self.titletext != "":
            tsurf = self.smallfont.render(str(self.titletext),
                                          True, color.WHITE)
            tw = tsurf.get_width() / 2
            canvas.blit(tsurf, (400 - tw, 500))
        for idx, post in enumerate(self.posts[:]):
            keep = post(canvas)
            if not keep:
                self.posts.pop(idx)

    def add_entity(self, ent):
        self.toadd.add(ent)

    def remove_entity(self, ent):
        if ent in self._entities:
            ent.mark_deleted()
            ent.kill()

    def input_manager(self):
        return self._input_manager

    def env_manager(self):
        return self._env_manager

    def debug(self):
        return self._debug

    def add_mid(self, s):
        self.mid.add(s)

    def add_front(self, s):
        self.front.add(s)

    def add_back(self, s):
        self.back.add(s)

    def add_boss(self, s):
        self.boss.add(s)

    def __to_menu(self):
        self._channel.pause()
        self._stateObject.MENU = menu.Menu(self._stateObject)
        self._stateObject.STATE = self._stateObject.MENU
