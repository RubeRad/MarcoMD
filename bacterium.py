#! /usr/bin/python3
import pygame
from   pygame.sprite import Sprite
import random

class Bacterium(Sprite):
    def __init__(s, settings, screen, others):
        super().__init__()
        s.sc = screen
        s.rect = pygame.Rect(0, 0, settings.blocksize, settings.blocksize)
        s.rect.centerx = screen.get_rect().centerx
        s.rect.centery = screen.get_rect().centery
        s.color = settings.random_color()
        s.random_position(settings, others)

    def random_position(s, settings, others):
        half = settings.spacing//2
        while True:
            row = random.randint(0, settings.blockrows-1)
            col = random.randint(0, settings.cols-1)
            s.rect.centerx = half + col * settings.spacing
            s.rect.centery = half + row * settings.spacing
            s.rect.centery = settings.screenh - s.rect.centery
            if pygame.sprite.spritecollide(s, others, False):
                print("Bang!")
                continue # collision! go try again
            # if we make it here, s does not collide with others
            break

    def render(s):
        pygame.draw.rect(s.sc, s.color, s.rect)