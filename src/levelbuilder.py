import obstacle
import platform
import player
import enemy
import fishEnemy
import lasercannon
import pygame as PG
import pygame.sprite
import pygame.image
import pygame.mixer
import camera
import weapon
import jetpack
import cutscene
import color
import intro
import soundtrigger
import savepoint
import boss
import cutscenemanager
import waterlock

'''
this module reads in text files and then
creates the obstacle entities for the level
'''


class LevelBuilder():

    '''
    This takes a file and returns a group of sprites
    '''

    def __init__(self, state):
        self.state = state
        self.sounds = []
        self.titles = []

    def parse_weapon(self, filename):
        wfile = open("../Levels/" + filename).readlines()
        w = int(wfile[0])
        h = int(wfile[1])
        cd = int(wfile[2])
        vel = int(wfile[3])
        color = eval(wfile[4])
        return weapon.Weapon(w, h, cd, vel, color)

    def parse_jetpack(self, filename):
        wfile = open("../Levels/" + filename).readlines()
        x = int(wfile[0])
        yp = int(wfile[1])
        ym = int(wfile[2])
        jv = int(wfile[3])
        g = False
        if int(wfile[4]) == 1:
            g = True
        grav = float(wfile[5])
        return jetpack.Jetpack(x, yp, ym, jv, g, grav)

    def parse_sounds(self, filename):
        soundlist = open("../Levels/" + filename).readlines()
        for line in soundlist:
            fulltext = line.split("|")
            soundfile = fulltext[0]
            titletext = fulltext[1].strip()
            self.sounds.append(pygame.mixer.Sound(
                ("../Sounds/" + soundfile).strip()))
            self.titles.append(titletext)

    def buildLevel(self, filename):
        # create the variables
        x = 0
        y = 0
        cam = camera.Camera(self.state)
        sprites = []
        bossg = pygame.sprite.Group()
        back = pygame.sprite.Group()
        mid = pygame.sprite.Group()
        front = pygame.sprite.Group()

        # global variables that controls the character size to pixel conversion
        GLOBAL_WIDTH = 50
        GLOBAL_HEIGHT = 50
        # open the file to read from
        with open(filename) as f:
            content = f.readlines()
            playerdata = content[len(content) - 5:]
            content = content[0:len(content) - 6]
        weapon = self.parse_weapon(playerdata[0].strip())
        jetpack = self.parse_jetpack(playerdata[1].strip())
        level = playerdata[2].strip()
        bg = pygame.image.load("../Images/" + playerdata[3].strip())
        self.parse_sounds(playerdata[4].strip())
        sound_cache = []

        #go through each character in the file
        for row in content:
            x = 0
            for col in row:
                #floor
                if col == 'f':
                    temp = platform.Platform(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        16 * GLOBAL_WIDTH, GLOBAL_HEIGHT,
                        "PLATFORM", cam,
                        '../Images/' + level + '_floor.png', self.state)
                    sprites.append(temp)
                    back.add(temp)
                #death floor
                if col == 'd':
                    temp = platform.Platform(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        16 * GLOBAL_WIDTH, GLOBAL_HEIGHT,
                        "DEATHTRIGGER", cam,
                        '../Images/lava.jpg', self.state)
                    sprites.append(temp)
                    back.add(temp)
                #platform
                if col == 'p':
                    temp = platform.Platform(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH, GLOBAL_HEIGHT,
                        "PLATFORM", cam,
                        '../Images/' + level + '_block3.png', self.state)
                    sprites.append(temp)
                    back.add(temp)
                #large wall
                if col == '|':
                    temp = platform.Platform(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH, 12 * GLOBAL_HEIGHT,
                        "PLATFORM", cam,
                        '../Images/' + level + '_wall.png', self.state)
                    sprites.append(temp)
                    back.add(temp)
                #200 height wall
                if col == 'w':
                    temp = platform.Platform(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH, 4 * GLOBAL_HEIGHT,
                        "PLATFORM", cam,
                        '../Images/' + level + '_block1.png', self.state)
                    sprites.append(temp)
                    back.add(temp)
                #water lock
                if col == 'W':
                    temp = waterlock.WaterLock(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        3 * GLOBAL_WIDTH, 3 * GLOBAL_HEIGHT,
                        "PLATFORM", cam,
                        '../Images/' + level + 'waterlock.png', self.state)
                    sprites.append(temp)
                    front.add(temp)
                if col == '3':
                    temp = platform.Platform(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH, 3 * GLOBAL_HEIGHT,
                        "PLATFORM", cam,
                        '../Images/' + level + '_block3.png', self.state)
                    sprites.append(temp)
                    back.add(temp)
                #player
                if col == 'c':
                    temp = player.Player(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        54, 44, cam, self.state)
                    temp.weapon = weapon
                    temp.jetpack = jetpack
                    sprites.append(temp)
                    mid.add(temp)
                #enemy
                if col == 'e':
                    temp = enemy.Enemy(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        54, 38, cam, self.state)
                    sprites.append(temp)
                    mid.add(temp)
                if col == 'F':
                    temp = fishEnemy.Fish(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        54, 38, cam, self.state)
                    sprites.append(temp)
                    mid.add(temp)
                if col == 'v':
                    temp = platform.Platform(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH, GLOBAL_HEIGHT,
                        "ENDLEVEL", cam,
                        "../Images/door_0.png", self.state)
                    sprites.append(temp)
                    mid.add(temp)
                #lasercannons
                if col == 'l':
                    temp = lasercannon.Lasercannon(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH + 20, GLOBAL_HEIGHT + 20,
                        cam, 'S', self.state)
                    sprites.append(temp)
                    mid.add(temp)
                if col == 'L':
                    temp = lasercannon.Lasercannon(
                        x * GLOBAL_WIDTH - 1, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH + 20, GLOBAL_HEIGHT + 20,
                        cam, 'W', self.state)
                    sprites.append(temp)
                    mid.add(temp)
                if col == 'R':
                    temp = lasercannon.Lasercannon(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH + 20, GLOBAL_HEIGHT + 20,
                        cam, 'E', self.state)
                    sprites.append(temp)
                    mid.add(temp)
                if col == 'U':
                    temp = lasercannon.Lasercannon(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH + 20, GLOBAL_HEIGHT + 20,
                        cam, 'N', self.state)
                    sprites.append(temp)
                    mid.add(temp)
                if col == '!':
                    temp = intro.Intro(cam, self.state)
                    sprites.append(temp)
                    mid.add(temp)
                if col == 't':
                    sound = soundtrigger.SoundTrigger(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH, GLOBAL_HEIGHT,
                        cam, self.state)
                    sound_cache.append(sound)
                    sprites.append(sound)
                    mid.add(sound)
                if col == 'S':
                    save = savepoint.SavePoint(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH, GLOBAL_HEIGHT,
                        cam, self.state)
                    sprites.append(save)
                    mid.add(save)
                if col == 'B':
                    b = boss.Boss(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        GLOBAL_WIDTH, GLOBAL_HEIGHT,
                        cam, self.state)
                    sprites.append(b)
                    bossg.add(b)
                if col == 'm':
                    m = cutscenemanager.cutscenemanager(
                        x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT,
                        cam, self.state)
                    sprites.append(m)
                    back.add(m)
                x += 1
            y += 1
        sprites.append(cam)
        for i in xrange(len(sound_cache)):
            sound_cache[i].set_sound(self.sounds[i])
            sound_cache[i].set_text(self.titles[i])
        return (sprites,
                (x * GLOBAL_WIDTH, y * GLOBAL_HEIGHT),
                bossg, back, mid, front,
                bg)


def main():
    b = LevelBuilder()
    b.buildLevel("../Levels/basic.txt")

if __name__ == "__main__":
    main()
