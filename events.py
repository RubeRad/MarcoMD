#! /usr/bin/python3

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
        elif e.type == pygame.KEYUP:
            u.move = '' # turn off key_down


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
            color = colors[r][c]
            if color == (0,0,0):
                continue
            down_same = True # so far
            inarow = [ (r,c) ]
            for i in range(1,settings.inarow):
                if r+i>=settings.rows or  colors[r+i][c] != color:
                    down_same = False
                    break
                inarow.append( (r+i,c) )
            if down_same:
                inarows.append(inarow)

            acrs_same = True
            inarow = [ (r,c) ]
            for i in range(1, settings.inarow):
                if c+i>=settings.cols or colors[r][c+i] != color:
                    acrs_same = False
                    break
                inarow.append( (r,c+i) )
            if acrs_same:
                inarows.append(inarow)

    if len(inarows):
        return inarows
    # else
    return None


def clear(settings, statics):
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
            statics.remove(s)
            if isinstance(s,Unguent) and s.free_to_move(statics):
                found_sump = True
                movers.append(s)
                break
            else: # put it back
                statics.add(s)

    return movers


def has_bacteria(statics):
    for s in statics:
        if isinstance(s, Bacterium):
            return True
    return False