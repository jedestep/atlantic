import entity
import obstacle
import phys
import playershot
import lasercannon
import enemy
import weapon
import jetpack

import scores
import menu
import color

import pygame.event
import pygame.mixer
import pygame.transform
import pygame.draw
import pygame

import sheethelper

import game

import random
import bubble


class Player(phys.PhysEntity):

    '''
    The player. This class handles player movement and what to do on collision
    '''
    # Takes initial position, bounding box, list of animation frames
    def __init__(self, i_x, i_y, w, h, camera, state):
        phys.PhysEntity.__init__(self, i_x, i_y, w, h, camera, state)
        KD = pygame.KEYDOWN
        KU = pygame.KEYUP
        self.bump_snd = pygame.mixer.Sound("../Sounds/short_chirp.ogg")
        self.facing = 1  # 1 = right, -1 = left
        self.callbacks.update({
            (KD, pygame.K_RIGHT): self.__go_right,
            (KU, pygame.K_RIGHT): self.__stop_right,
            (KD, pygame.K_LEFT): self.__go_left,
            (KU, pygame.K_LEFT): self.__stop_left,
            (KD, pygame.K_SPACE): self.__jump,
            (KD, pygame.K_w): self.__shoot_up,
            (KD, pygame.K_s): self.__shoot_down,
            (KD, pygame.K_a): self.__shoot_left,
            (KD, pygame.K_d): self.__shoot_right})
        self._numframes = 12

        self.score = 0
        self.invincible = 0
        self.scoresheet = None

        self.health = 100
        self._framecache = {
            "WALK": sheethelper.load_frames("../Images/playerwalksheet.png",
                                            self._numframes, 0, 0, 62, 46),
            "AIR": sheethelper.load_frames("../Images/playerwalksheet.png",
                                           1, 620, 0, 62, 46),
            "STAND": (sheethelper.load_frames("../Images/playeridle.png",
                                              1, 64, 0, 62, 46) * 3) +
                     (sheethelper.load_frames("../Images/playeridle.png",
                                              1, 128, 0, 62, 46) * 3)
        }
        self._frames = self._framecache["WALK"]

        self.weapon = None
        self.jetpack = None
        self.grav_mod = False

        self.bubble_freq = 0.005

        self.left_pressed = False
        self.right_pressed = False

    def update(self, dt):
        phys.PhysEntity.update(self, dt)
        self.camera.xpos = self.xpos - 400
        self.camera.ypos = self.ypos - 350
        if self.airborne:
            self._frames = self._framecache["AIR"]
            self._numframes = 1
        elif not self.airborne and self.xvel == 0:
            self._frames = self._framecache["STAND"]
            self._numframes = 6
        elif not self.airborne and self.xvel != 0:
            self._frames = self._framecache["WALK"]
            self._numframes = 12
        if self.invincible > 0:
            self.invincible -= 1
        if self.weapon is not None:
            self.weapon.update()
        if self.jetpack is not None and not self.grav_mod:
            self.jetpack.apply_gravity(self)
        l = self._stateObject.GAME.levelname
        if ((l == "../Levels/Level3.txt" or l == "../Levels/finalcutscene.txt")
                and random.random() < self.bubble_freq):
            b = bubble.Bubble(self.xpos + 20, self.ypos - 10, 10, 0, -5,
                              self.camera, color.BLUE, self, self._stateObject)
            self._add_bubble(b)
        if self.left_pressed:
            if self.xvel > -20:
                self.xvel = -20
        if self.right_pressed:
            if self.xvel < 20:
                self.xvel = 20

    def notify(self, event):
        was_airborne = self.airborne
        phys.PhysEntity.notify(self, event)
        if not was_airborne and self.airborne:  # change to midair animation
            self._frames = self._framecache["AIR"]
            self._numframes = 1
        elif not self.airborne and was_airborne:
            # change back to walking animation
            self._frames = self._framecache["STAND"]
            self._numframes = 6

    def draw(self, canvas):
        phys.PhysEntity.draw(self, canvas)
        # draw health bar
        pygame.draw.rect(canvas, color.RED,
                         pygame.Rect(self.xpos, self.ypos - 20, 50, 6), 0)
        pygame.draw.rect(canvas, color.GREEN,
                         pygame.Rect(self.xpos, self.ypos - 20,
                                     self.health / 2, 6), 0)

    def __go_right(self):
        self.right_pressed = True

    def __stop_right(self):
        self.right_pressed = False
        if not self.left_pressed:
            self.xvel = 0

    def __go_left(self):
        self.left_pressed = True

    def __stop_left(self):
        self.left_pressed = False
        if not self.right_pressed:
            self.xvel = 0

    def __jump(self):
        self.jetpack.jump(self)

    def __shoot_up(self):
        shot = self.weapon.get_shot(
            'N', self, (self.width, 18))
        if shot is not None:
            self._add_shot(shot)
            self.jetpack.push_down(self)

    def __shoot_down(self):
        shot = self.weapon.get_shot(
            'S', self, (self.width, 18))
        if shot is not None:
            self._add_shot(shot)
            self.jetpack.push_up(self)

    def __shoot_left(self):
        shot = self.weapon.get_shot(
            'W', self, (self.width, 18))
        if shot is not None:
            self._add_shot(shot)
            self.jetpack.push_right(self)

    def __shoot_right(self):
        shot = self.weapon.get_shot(
            'E', self, (self.width, 18))
        if shot is not None:
            self._add_shot(shot)
            self.jetpack.push_left(self)

    def _add_shot(self, shot):
        self._stateObject.GAME.add_entity(shot)
        self._stateObject.GAME.add_mid(shot)

    def _delete_shot(self, shot):
        if self._stateObject.GAME is not None:
            self._stateObject.GAME.remove_entity(shot)

    def _add_bubble(self, bubble):
        self._stateObject.GAME.add_entity(bubble)
        self._stateObject.GAME.add_mid(bubble)

    def _delete_bubble(self, bubble):
        if self._stateObject.GAME is not None:
            self._stateObject.GAME.remove_entity(bubble)

    def should_update(self):
        return True

    def get_frame(self):
        frame = self._frames[int(self.time % self._numframes)]
        if self.xvel > 0:
            self.facing = 1
        if self.xvel < 0:
            self.facing = -1
        if self.facing == -1:
            frame = pygame.transform.flip(frame, True, False)
        return frame

    def get_ammo(self):
        return self.ammo

    def take_dmg(self, h):
        if self.invincible > 0:
            return
        self.health -= h
        if self.health <= 0:
            self.game().player_die()

    def update_scoresheet(self):
        self.scoresheet = scores.Scores(
            self._stateObject, self.score, True)

    def _halt(self, name, reporter, target):
        phys.PhysEntity._halt(self, name, reporter, target)
        if reporter == self:
            if isinstance(target, obstacle.Obstacle):
                if target.ty == "WALL":
                    self.bump_snd.play()
                elif target.ty == "DEATHTRIGGER":
                    self.take_dmg(50)
                    self.xpos = self.init_x
                    self.ypos = self.init_y
                    self.xvel = 0
                    self.yvel = 0
                    self.rect.top = self.ypos
                    self.rect.left = self.xpos
                    self.airborne = True
                elif target.ty == "ENDLEVEL":
                    self.xvel = 0
                    self.yvel = 0
                    self.xpos = 0
                    self.ypos = 0
                    self.update_scoresheet()
                    self._stateObject.GAME.load_level()
                    self.rect.x = -100
                    self.rect.y = -100
            elif isinstance(target, enemy.Enemy) and self.invincible == 0:
                self.take_dmg(25)
                self.xvel = -40 * self.facing
                self.yvel = -40
                self.invincible = 20
                self.airborne = True
        #elif isinstance(reporter, playershot.PlayerShot):
            #if isinstance(target, lasercannon.Lasercannon):
                #target.take_dmg(10)
            #self._delete_shot(reporter)
