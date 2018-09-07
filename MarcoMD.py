#! /usr/bin/python3

import time
import pygame
from   pygame.sprite import Group
from bacterium import Bacterium
from unguent   import Unguent
from settings  import Settings
import events



settings = Settings()
pygame.init()
screen = pygame.display.set_mode((settings.screenw, settings.screenh))
statics = Group()
for i in range(settings.n_bacteria):
    statics.add(Bacterium(settings, screen, statics))
u = Unguent(settings, screen)

tsum=tnum=0
t0 = time.perf_counter()
while events.has_bacteria(statics):
    # take care of bidnis
    events.handle(settings, u)
    if settings.paused:
        continue

    u.update(statics)
    if not u.moving_down: # done moving! time for a new one
        statics.add(u)
        u = Unguent(settings, screen)
        # is the new unguent blocked from entering the screen?
        if pygame.sprite.spritecollide(u, statics, False):
            print("Kablooey")
            break; # game over

    # detect inarows and execute erasure
    # movers are the broken pieces of unguents that need to fall down
    movers = events.clear(settings, statics)

    # temporarily let extra pieces fall at same speed as accelerated keypresses
    save_speed = settings.s_fall
    settings.s_fall = settings.s_move
    while len(movers):
        # inner loop makes user wait for pieces to fall
        for m in movers.copy():
            if not m.moving_down:
                statics.add(m)
                movers.remove(m)
        screen.fill(settings.bg_color)
        for b in statics.sprites():
            b.render()
        for m in movers:
            m.update(statics)
            m.render()
        pygame.display.flip()
    settings.s_fall = save_speed

    # redraw everything
    screen.fill(settings.bg_color)
    for b in statics.sprites():
        b.render()
    u.render()
    pygame.display.flip()
    t1 = time.perf_counter()
    dt = t1-t0
    t0 = t1
    tsum += dt
    tnum += 1

avg = tsum / tnum
print(tnum, "cycles, avg", avg, "sec")





