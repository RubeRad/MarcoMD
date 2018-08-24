#! /usr/bin/python3

import pygame
from   pygame.sprite import Group
from bacterium import Bacterium
from unguent   import Unguent
from settings  import Settings


settings = Settings()
pygame.init()
screen = pygame.display.set_mode((settings.screenw, settings.screenh))
bacteria = Group()
for i in range(settings.n_bacteria):
    bacteria.add(Bacterium(settings, screen, bacteria))
u = Unguent(settings, screen)

for b in bacteria.sprites():
    b.render()
u.render()

pygame.display.flip()

stophere=1





