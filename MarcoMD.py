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

while True:
    screen.fill(settings.bg_color)
    for b in bacteria.sprites():
        b.render()
    u.update()
    u.render()
    if pygame.sprite.spritecollide(u, bacteria, False):
        break

    pygame.display.flip()

stophere=1





