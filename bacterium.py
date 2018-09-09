#! /usr/bin/python3
import pygame
from   pygame.sprite import Sprite
import random

class Bacterium(Sprite):
    def __init__(s, settings, screen, others):
        super().__init__()
        s.se = settings
        s.sc = screen # is this actually necessary?
        s.rect = pygame.Rect(0, 0, s.se.blocksize, s.se.blocksize)
        s.random_position(others) # this sets rect position
        s.color = s.se.random_color()

    def random_position(s, others):
        # try random positions until we find one that doesn't collide
        while True:
            row = random.randint(s.se.rows-s.se.blockrows, s.se.rows-1)
            col = random.randint(0, s.se.cols-1)
            s.set_position(col, row)
            if pygame.sprite.spritecollide(s, others, False):
                print("Bang!")
                continue # collision! go try again
            # if we make it here, s does not collide with others
            break

    def set_position(s, col, row):
        half = s.se.spacing//2
        s.rect.centerx = half + col * s.se.spacing
        s.rect.centery = half + row * s.se.spacing

    def render(s):
        pygame.draw.circle(s.sc, s.color, s.rect.center, s.se.blocksize//2)

    def block_index(s):
        row = s.rect.top  // s.se.spacing
        col = s.rect.left // s.se.spacing
        return (col,row)