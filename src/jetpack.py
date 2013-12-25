

class Jetpack(object):
    def __init__(self, xvel, yvel_plus, yvel_minus, jvel, ground, gravity):
        self.xvel = xvel
        self.yp = yvel_plus
        self.ym = yvel_minus
        self.jvel = jvel
        self.ground = ground
        self.gravity = gravity

    def jump(self, jumper):
        if not jumper.airborne:
            jumper.airborne = True
            jumper.yvel = self.jvel

    def apply_gravity(self, jumper):
        jumper.g = self.gravity
        jumper.yacc = self.gravity

    def push_down(self, jumper):
        if self.gravity == 0:
            jumper.yvel += self.yp
        elif jumper.airborne or self.ground:
            jumper.yvel += self.yp

    def push_up(self, jumper):
        if self.gravity == 0:
            jumper.yvel += self.ym
        elif ((jumper.airborne and jumper.yvel >= 0)
                or self.ground):
            jumper.yvel = self.ym

    def push_right(self, jumper):
        if self.gravity == 0:
            jumper.xvel += self.xvel
        elif jumper.airborne or self.ground:
            jumper.xvel += self.xvel

    def push_left(self, jumper):
        if self.gravity == 0:
            jumper.xvel -= self.xvel
        elif jumper.airborne or self.ground:
            jumper.xvel -= self.xvel
