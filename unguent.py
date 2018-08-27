#! /usr/bin/python3

import pygame
from pygame.sprite import Sprite

class Unguent(Sprite):
    def __init__(s, settings, screen,
                 r=-1, c=-1, # DEF: top, center
                 clist=[],   # DEF: settings.nblocks random colors
                 o=0):       # DEF: left-->right

        super().__init__()
        s.sc = screen   # short names for often-used data members
        s.se = settings

        if len(clist)>0: # assigned colors, known size
            s.colors  =     clist
            s.nblocks = len(clist)
        else:            # default size, random colors
            s.nblocks = s.se.unguent_blocks
            # assign random colors per block from colors in settings
            s.colors = []
            for i in range(s.nblocks):
                s.colors.append(s.se.random_color())

        # RECT: make a Rect that is nblocks full spacings wide/tall
        # we will draw individual unguent blocks inside it
        s.rect = pygame.Rect(0,0, 1, 1) # set all these numbers

        # POSITION row/column specifies index of 'first' block
        if r<0 or c<0: # position unassigned; center at top of screen
            r = 0
            c = s.se.cols//2 - s.nblocks//2

        # orientation 0=l->r, 1=t->b, 2=r->l, 3=b->t
        s.orientation = o
        if s.orientation in (0,1): # l->r, t->b
            s.rect.left   = s.se.spacing * c
            s.rect.top    = s.se.spacing * r
        else:
            s.rect.right  = s.se.spacing * (c+1)
            s.rect.bottom = s.se.spacing * (r+1) + 1

        if s.orientation in (0,2): # horizontal
            s.rect.width  = s.se.spacing * s.nblocks
            s.rect.height = s.se.spacing + 1
        else:                      # vertical
            s.rect.width  = s.se.spacing
            s.rect.height = s.se.spacing * s.nblocks + 1

        # start out moving down
        s.moving_down = True
        s.topy = s.rect.top
        s.move = ''


    def first_block_index(s): # col,row index of only 'first' block
        if s.orientation in (0, 1):  # l->r/t->b: grab top/left block
            row = (s.rect.top    + s.se.blockborder) // s.se.spacing
            col = (s.rect.left   + s.se.blockborder) // s.se.spacing
        else:  # r->l/b->t: grab bottom/right blocks
            row = (s.rect.bottom - s.se.blocksize)   // s.se.spacing
            col = (s.rect.right  - s.se.blocksize)   // s.se.spacing
        return (col,row)

    def last_block_index(s):
        if s.orientation in (0, 1):  # l->r/b->t: grab bot/right block
            row = (s.rect.bottom - s.se.blocksize) // s.se.spacing
            col = (s.rect.right  - s.se.blocksize) // s.se.spacing
        else:  # r->l/b->t: grab top/left blocks
            row = (s.rect.top    + s.se.blockborder) // s.se.spacing
            col = (s.rect.left   + s.se.blockborder) // s.se.spacing
        return (col,row)

    # if this unguent doesn't include r,c, return -1
    # if it does, return 0 for 'first' block, etc.
    def index_of(s, r, c):
        c0,r0 = s.first_block_index()
        cN,rN =  s.last_block_index()
        if s.orientation==0 and r==r0 and r==rN and c0<=c and c<=cN:
            return c-c0
        if s.orientation==1 and c==c0 and c==cN and r0<=r and r<=rN:
            return r-r0
        if s.orientation==2 and r==r0 and r==rN and cN<=c and c<=c0:
            return c0-c
        if s.orientation==3 and c==c0 and c==cN and rN<=r and r<=r0:
            return r0-r
        # else
        return -1



    def orientation_dc_dr(s):
        if s.orientation == 0: return (1,0)
        if s.orientation == 1: return (0,1)
        if s.orientation == 2: return (-1,0)
        if s.orientation == 3: return (0,-1)

    def render(s):
        bb = s.se.blockborder
        bs = s.se.blocksize
        sp = s.se.spacing
        if s.se.unguent_smooth:  # move every pixel
            s.rect.top = int(s.topy)
        else:  # move only in discrete jumps
            # use truncating integer division
            rows = int(s.topy)//s.se.spacing
            s.rect.top = rows * s.se.spacing
        ty = s.rect.top

        col,row = s.first_block_index()
        dcol,drow = s.orientation_dc_dr()

        for c in s.colors: # draw each box its own color
            r = pygame.Rect(col*sp+bb, row*sp+bb, bs, bs)
            pygame.draw.rect(s.sc, c, r)
            col += dcol # scoot for next block
            row += drow

    def update(s, bacteria):
        # DOWNWARD movement is automatic
        # stop moving at the bottom of the screen
        if s.rect.bottom >= s.se.screenh:
           s.moving_down = False
           s.move = ''
        # if we are still moving, apply fractional distance
        if s.moving_down:
           mvmty = s.se.unguent_speed
           if s.move == s.se.key_down: # move further/faster
               s.topy += mvmty * 10
               return # don't erase s.move until KEYUP
           # else no keypress for fast down, just regular mvmt
           s.topy += mvmty

        # ROTATION is by user keypress
        if s.move in (s.se.key_cw, s.se.key_ccw):
            # find the 'first' block
            bb = s.se.blockborder
            bs = s.se.blocksize
            sp = s.se.spacing

            col,row = s.first_block_index()
            # now build the bounding box for the new orientation
            s.orientation = (s.orientation + 1) % 4

            if s.orientation in (0,2):
                s.rect.width  = sp * s.nblocks
                s.rect.height = sp + bb + 1
            else:
                s.rect.width  = sp
                s.rect.height = sp * s.nblocks + bb + 1

            if s.orientation in (0,1):
                s.rect.top  = row * sp
                s.rect.left = col * sp
            else:
                s.rect.bottom = sp * (row+1) + bb + 1
                s.rect.right  = sp * (col+1)

            # check if rotation goes off screen right or left
            if s.rect.left  < 0:            s.rect.left  = 0
            if s.rect.right > s.se.screenw: s.rect.right = s.se.screenw

            # done processing CW/CCW keypress, erase it and return
            s.move = ''
            return

        # HORIZONTAL movement is by user keypress
        elif s.move in (s.se.key_left, s.se.key_rght):
            mvmtx = 0
            if s.move == s.se.key_left:
                mvmtx = -s.se.spacing
            elif s.move == s.se.key_rght:
                mvmtx =  s.se.spacing
            # test if we go off the screen or collide with any bacteria
            s.rect.centerx += mvmtx
            undo = False
            if s.rect.left  <  0:           undo = True
            if s.rect.right > s.se.screenw: undo = True
            if pygame.sprite.spritecollide(s, bacteria, False):
                                            undo = True
            if undo:
                s.rect.centerx -= mvmtx
            # move is executed so erase the keypress signal
            s.move = ''







