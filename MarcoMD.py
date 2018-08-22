#! /usr/bin/python3

import pygame
from   pygame.sprite import Sprite
from   pygame.sprite import Group

class Bacterium(Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0,10,10)
        self.rect.centerx = screen.get_rect().centerx
        self.rect.centery = screen.get_rect().centery
        self.color = (255,0,0)

    def render(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

pygame.init()
screen = pygame.display.set_mode((400,800))
b = Bacterium(screen)
bacteria = Group()
bacteria.add(b)

for b in bacteria.sprites():
    b.render()

pygame.display.flip()

stophere=1





