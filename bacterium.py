#! /usr/bin/python3
import pygame
from   pygame.sprite import Sprite
import random

class Bacterium(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, settings.blockw, settings.blockh)
        self.rect.centerx = screen.get_rect().centerx
        self.rect.centery = screen.get_rect().centery
        self.random_color(settings)

    def random_color(self, settings):
        ncolors = len(settings.colors)
        index = random.randint(0, ncolors)
        self.color = settings.colors[index]

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)