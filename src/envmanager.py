import event
import publisher
import pygame.sprite
import pygame.draw
import math
import pprint

GRIDX = 150
GRIDY = 150

GRIDCELLX = math.ceil(1600 / GRIDX)
GRIDCELLY = math.ceil(600 / GRIDY)


class EnvironmentManager(publisher.Publisher):

    '''
    Handles collisions between sprites
    '''

    def __init__(self, state):
        publisher.Publisher.__init__(self, state)
        self.update_grid = {}
        self.grid = {}

    def draw_grid(self, canvas):
        for gridpoint in self.update_grid:
            pygame.draw.circle(canvas, (0, 0, 0),
                               (gridpoint[0] * GRIDX, gridpoint[1] * GRIDY), 1)

    def calc_bucket(self, x, y):
        return (int(x / GRIDY), int(y / GRIDX))

    def find_update_buckets(self):
        bucket = self.calc_bucket
        rect = self._stateObject.GAME.camera.get_update_rect()
        # if rect.x != 0:
        #     import pdb; pdb.set_trace()
        self.update_grid = set()
        # TODO think about the + GRIDX here
        for x in range(rect.left, rect.right, GRIDX) + [rect.right]:
            for y in range(rect.top, rect.bottom, GRIDY) + [rect.bottom]:
                self.update_grid.add(bucket(x, y))

    def update(self, dt):
        publisher.Publisher.update(self, dt)
        self.find_update_buckets()
        self.do_collisions()

    def do_collisions(self):
        #print 'Update loop'
        #print 'grid:'
        #pprint.pprint(self.grid)
        i = 0
        for bucket in self.update_grid:
            ents = self.grid.get(bucket, set())
            proc = set()
            for ent1 in ents:
                for ent2 in ents:
                    if ent1 not in proc and ent1 != ent2:
                        i += 1
                        if pygame.sprite.collide_rect(ent1, ent2):
                            #print 'col between', ent1, 'and', ent2
                            if self._stateObject.GAME is None:
                                return
                            ent1.notify(('COLLIDE', ent1, ent2))
                            if self._stateObject.GAME is None:
                                return
                            ent2.notify(('COLLIDE', ent2, ent1))
                proc.add(ent1)
        #print 'Processed', i, 'distinct possible collisions'

    def update_buckets(self, ent, newbuckets):
        for old in ent.buckets:
            if old not in newbuckets:
                #print 'removing old', old, 'from', ent
                self.grid[old].remove(ent)
            else:
                newbuckets.remove(old)
        for new in newbuckets:
            if new not in self.grid:
                self.grid[new] = set()
            self.grid[new].add(ent)
