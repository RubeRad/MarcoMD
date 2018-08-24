#! /usr/bin/python3
import pygame
from   pygame.sprite import Sprite
import random

class Bacterium(Sprite):
    def __init__(self, settings, screen, others):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, settings.blocksize, settings.blocksize)
        self.rect.centerx = screen.get_rect().centerx
        self.rect.centery = screen.get_rect().centery
        self.color = settings.random_color()
        self.random_position(settings, others)

    def random_position(self, settings, others):
        half = settings.spacing//2
        while True:
            row = random.randint(0, settings.blockrows-1)
            col = random.randint(0, settings.cols-1)
            self.rect.centerx = half + col * settings.spacing
            self.rect.centery = half + row * settings.spacing
            self.rect.centery = settings.screenh - self.rect.centery
            if pygame.sprite.spritecollide(self, others, False):
                print("Bang!")
                continue # collision! go try again
            # if we make it here, self does not collide with others
            break

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)