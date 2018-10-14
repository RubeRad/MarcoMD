#!/usr/bin/env python3

import time
import pygame
from   pygame.sprite import Group
from bacterium import Bacterium
from unguent   import Unguent
from settings  import Settings
import events


# modularize some game logic into functions to make the main loop cleaner

def end_game(screen, msgs):
    rowpix = 0
    for msg in msgs:
        screen.blit(msg, (0, rowpix))
        rowpix += 20
    pygame.display.flip()
    time.sleep(3)

def drop_fragments(screen, fragments, statics):
    if len(fragments)==0:
        return # no fragments --> nothing to do

    # set all timers to the same so they fall in sync
    # set falling speed faster so they get out of the way quick
    common_time = time.perf_counter()
    for f in fragments:
        f.s_fall = f.s_move
        f.time_fall = common_time
        f.time_move = common_time

    # when we fall out of this while loop, all the fragments will be done falling
    while len(fragments):
        for f in fragments.copy():
            f.update(statics)     # immediately after updating
            if not f.moving_down:   # if update made f static
                statics.add(f)      # transfer f to statics
                fragments.remove(f) # so next frag knows it's static

        # redraw everything
        screen.fill(settings.bg_color)
        for b in statics.sprites():  b.render()
        for f in fragments:          f.render()
        pygame.display.flip()


def update_times(t0, tsum, tnum):
    t1 = time.perf_counter()
    dt = t1-t0
    new_t0 = t1
    return new_t0, tsum+dt, tnum+1



####################### MAIN PROGRAM STARTS HERE #######################
# get things ready
pygame.font.init()
myfont = pygame.font.SysFont('Ubuntu', 20)
txt_win1 = myfont.render('Congratulations!', False, (115, 115, 115))
txt_win2 = myfont.render('You Won!', False, (115, 115, 115))
winmsgs = [txt_win1, txt_win2]
txt_fail = myfont.render('Kablooey!', False, (115, 115, 115))
failmsgs = [txt_fail]

# create a Settings object, which also checks command line for options
settings = Settings()
# build empty screen
pygame.init()
screen = pygame.display.set_mode((settings.screenw, settings.screenh))
# populate with initial objects
statics = Group() # for now just bacteria, later also unguent fragments
for i in range(settings.n_bacteria):
    statics.add(Bacterium(settings, screen, statics))
# this is the game piece controlled by the user
u = Unguent(settings, screen)

tsum=tnum=0
t0 = time.perf_counter()

############################# MAIN LOOP HERE #############################
# just cycle around this really fast -- so fast most times nothing happens
# only when there's enough time elapsed does the unguent move
while True: # loop until game over
    # take care of bidnis
    events.handle(settings, u) # check for user keypress
    if settings.paused:     # if user pressed the pause key
        continue            # keep spinning around this loop until unpaused

    # check if enough time has elapsed to move the unguent
    # and check whether it has come to rest on a static or the bottom
    u.update(statics)

    if not u.moving_down: # done moving! time for a new one
        statics.add(u)    # add unguent to statics for future tracking
        u = Unguent(settings, screen) # make a new one top center
        # is the new unguent blocked from entering the screen?
        if pygame.sprite.spritecollide(u, statics, False):
            end_game(screen, failmsgs)
            break; # game over LOSE

    # detect inarows and execute erasure
    # compute the broken pieces of unguents that need to fall down
    fragments = events.erase_inarows(settings, statics)
    if events.has_bacteria(statics) == False:
        end_game(screen, winmsgs)
        break # game over WIN

    # if there are any fragments, block user action until they finish falling
    drop_fragments(screen, fragments, statics)

    # redraw everything
    screen.fill(settings.bg_color)
    for b in statics.sprites():
        b.render()
    u.render()
    pygame.display.flip()

    t0,tsum,tnum = update_times(t0,tsum,tnum)# track timing statistics


# report statistics of how many times around the main loop, and averge time per loop
avg = tsum / tnum
print(tnum, "cycles, avg", avg, "sec")





