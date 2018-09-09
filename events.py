#! /usr/bin/python3

import time
import pygame
import sys
from bacterium import Bacterium
from unguent   import Unguent

def handle(se, u):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            c=chr(e.key) # convert number to character
            if   c == 'q':
                 sys.exit()
            elif c == se.key_pause:
                 se.paused = not se.paused
            elif c in se.keyset:
                 u.move = c
                 u.time_move = time.perf_counter()
                 u.key_just_pressed = True
        elif e.type == pygame.KEYUP:
            u.move = '' # turn off key_down
            u.time_move = time.perf_counter()
            u.key_just_pressed = False




def detect_inarows(settings, statics):
    # populate a grid with all the colors
    onerow = [(0,0,0)]*settings.cols
    colors = []
    for i in range(settings.rows):
        colors.append(onerow.copy())
    #colors = [[(0,0,0)] * settings.cols] * settings.rows
    for s in statics:
        if isinstance(s, Bacterium):
            c,r = s.block_index()
            colors[r][c] = s.color
        elif isinstance(s, Unguent):
            c,r = s.first_block_col_row()
            dc,dr = s.orientation_dc_dr()
            for i in range(s.nblocks):
                colors[r][c] = s.colors[i]
                c += dc
                r += dr
    # now look for inarows
    inarows = []
    for     r in range(settings.rows):
        for c in range(settings.cols):
            color = colors[r][c] # see if inarow from here is the same color
            if color == settings.bg_color: # no color here
                continue

            # how many inarow down from here?
            inarow = [ (r,c) ]
            for i in range(1,settings.inarow):
                if r + i >= settings.rows:
                    break  # ran off the board
                thiscolor = colors[r+i][c]
                if thiscolor != color:
                    break # this color doesn't match
                # if we get here then thiscolor does match color
                inarow.append( (r+i,c) )
            if len(inarow) >= settings.inarow: # we found enough!
                inarows.append(inarow)

            # how many inarow across right from here?
            inarow = [ (r,c) ]
            for i in range(1, settings.inarow):
                if c + i >= settings.cols:
                    break  # ran off the board
                thiscolor = colors[r][c+i]
                if thiscolor != color:
                    break # this color doesn't match
                # if we get here then thiscolor does match color
                inarow.append( (r,c+i) )
            if len(inarow) >= settings.inarow: # we found enough!
                inarows.append(inarow)

    if len(inarows):
        return inarows
    # else
    return None


def erase_inarows(settings, statics):
    inarows = detect_inarows(settings, statics)
    if not inarows:
        return []

    allrcs = []
    for inarow in inarows:
        for rc in inarow:
            allrcs.append(rc)

    movers = []
    for s in statics.copy():
        if isinstance(s, Bacterium):
            c,r = s.block_index()
            if (r,c) in allrcs:
                statics.remove(s)
        elif isinstance(s, Unguent):
            c,r = s.first_block_col_row()
            dc,dr = s.orientation_dc_dr()
            eraseindices = []
            for eraser,erasec in allrcs:
                i = s.index_of(eraser,erasec)
                if i!=-1:
                    eraseindices.append(i)
            if len(eraseindices):
                # break Unguent up into smaller Unguents
                pieces = s.denature(allrcs)
                if pieces:
                    movers.extend(pieces)
                statics.remove(s)


    # static Unguents might have broken free, look for them
    found_sumpn = True # just to get the loop started
    while (found_sumpn):
        found_sumpn = False
        for s in statics.copy():
            if not isinstance(s, Unguent): # bacteria never fall
                continue
            # check if unguent has no statics in its way
            statics.remove(s) # don't let it collide with itself
            if s.free_to_move(statics):
                found_sumpn = True
                movers.append(s)
                break
            else: # put it back
                statics.add(s)

    # issue #15: make sure these movers are sorted bottom-up
    # (decreasing row number). Whenever one fragment a is right
    # on top of fragment b, we need b to update before a so if it
    # stops moving and gets transferred from movers to statics,
    # then a can update and see it as a static and not move down into it
    movers.sort(key=lambda m : -m.bottom_row())

    return movers


def has_bacteria(statics):
    for s in statics:
        if isinstance(s, Bacterium):
            return True
    return False


#######################
##### UNIT TESTS ######
#######################
# if you run MarcoMD.py __name__=='events' and this is all skipped
# but if you run events.py then __name__=='__main__' and these tests are run
import unittest
from   pygame.sprite import Group
from settings import Settings

if __name__ == '__main__':
    class EventsTester(unittest.TestCase):
        def testInarows(s):
            se = Settings() # defaults: inarows=4
            red = (255,0,0)

            # set up 3 bacteria like this:       *
            #                                   **
            statics = Group()
            b1=Bacterium(se, None, statics); b1.color=red; b1.set_position(3,7)
            b2=Bacterium(se, None, statics); b2.color=red; b2.set_position(3,8)
            b3=Bacterium(se, None, statics); b3.color=red; b3.set_position(2,8)
            statics.add(b1)
            statics.add(b2)
            statics.add(b3)

            # verify we can detect 4 vertical blocks inarow
            u = Unguent(se,None,clist=(red,red))
            u.set_rect(3,6,3) # right above and going up
            statics.add(u)
            rcs = detect_inarows(se, statics)
            s.assertEqual(1, len(rcs))
            should_be_four = rcs[0]
            s.assertEqual(4, len(should_be_four))
            s.assertTrue((5,3) in should_be_four)
            s.assertTrue((8,3) in should_be_four)

            u.set_rect(3,9,1) # right below and going down
            rcs = detect_inarows(se, statics)
            s.assertEqual(1, len(rcs))
            should_be_four = rcs[0]
            s.assertEqual(4, len(should_be_four))
            s.assertTrue((7, 3) in should_be_four)
            s.assertTrue((10,3) in should_be_four)



    unittest.main()


