import pygame.image as PI
import pygame


def load_frames(filename, numframes, sprite_start_x, sprite_start_y,
                sprite_width, sprite_height, colorkey=None):
    image = PI.load(filename)
    if colorkey is not None:
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    frames = []
    for i in xrange(numframes):
        frames.append(image.subsurface(pygame.Rect(sprite_start_x + i *
                                                   sprite_width,
                                                   sprite_start_y,
                                                   sprite_width,
                                                   sprite_height)))
    return frames
