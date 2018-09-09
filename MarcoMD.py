#! /usr/bin/python3

import time
import pygame
from   pygame.sprite import Group
from bacterium import Bacterium
from unguent   import Unguent
from settings  import Settings
import events

pygame.font.init()
myfont = pygame.font.SysFont('Ubuntu', 20)
textsurface_win1 = myfont.render('Congratulations!', False, (115, 115, 115))
textsurface_win2 = myfont.render('You Won!', False, (115, 115, 115))
textsurface_fail = myfont.render('Kablooey!', False, (115, 115, 115))

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
            screen.blit(textsurface_fail, (0,0))
            pygame.display.flip()
            time.sleep(3)
            break; # game over

    # detect inarows and execute erasure
    # compute the broken pieces of unguents that need to fall down
    fragments = events.erase_inarows(settings, statics)
    if events.has_bacteria(statics) == False:
        screen.blit(textsurface_win1, (0, 0))
        screen.blit(textsurface_win2, (0, 20))
        pygame.display.flip()
        time.sleep(3)
        break

    # temporarily let extra pieces fall at same speed as accelerated keypresses
    for f in fragments:
        f.s_fall = f.s_move
    while len(fragments):
        # inner loop makes user wait for pieces to fall
        for f in fragments.copy():
            if not f.moving_down:
                statics.add(f)
                fragments.remove(f)
        screen.fill(settings.bg_color)
        for b in statics.sprites():
            b.render()
        for f in fragments:
            f.update(statics)
            f.render()
        pygame.display.flip()

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





