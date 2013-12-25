import playershot


class Weapon(object):
    def __init__(self, shot_w, shot_h, cooldown, velocity, c):
        self.shot_w = shot_w
        self.shot_h = shot_h
        self.cooldown = cooldown
        self.countdown = cooldown
        self.velocity = velocity
        self.color = c

    def get_shot(self, direction, shooter, (w, h)):
        if self.countdown == 0:
            self.countdown = self.cooldown
            x = shooter.xpos
            y = shooter.ypos
            wp = 0
            hp = 0
            if direction == 'E' or direction == 'W':
                wp = self.shot_h
                hp = self.shot_w
            else:
                wp = self.shot_w
                hp = self.shot_h
            return playershot.PlayerShot(
                x + w / 2, y + h,
                wp, hp,
                self.velocity, direction,
                shooter.camera, self.color, shooter,
                shooter._stateObject)

    def update(self):
        if self.countdown > 0:
            self.countdown -= 1
