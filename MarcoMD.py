#! /usr/bin/python3

import pygame
from   pygame.sprite import Group
from bacterium import Bacterium
from settings  import Settings


settings = Settings()
pygame.init()
screen = pygame.display.set_mode((settings.screenw, settings.screenh))
b = Bacterium(settings, screen)
bacteria = Group()
bacteria.add(b)

for b in bacteria.sprites():
    b.render()

pygame.display.flip()

stophere=1





