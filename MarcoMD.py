#! /usr/bin/python3

import pygame
from   pygame.sprite import Group
from bacterium import Bacterium
from unguent   import Unguent
from settings  import Settings
import events


settings = Settings()
pygame.init()
screen = pygame.display.set_mode((settings.screenw, settings.screenh))
bacteria = Group()
for i in range(settings.n_bacteria):
    bacteria.add(Bacterium(settings, screen, bacteria))
u = Unguent(settings, screen)

while True:
    # take care of bidnis
    events.handle(settings, u)
    if pygame.sprite.spritecollide(u, bacteria, False):
        u.moving_down = False
    u.update()

    # redraw everything
    screen.fill(settings.bg_color)
    for b in bacteria.sprites():
        b.render()
    u.render()
    pygame.display.flip()

    if not u.moving_down:
        break

stophere=1





