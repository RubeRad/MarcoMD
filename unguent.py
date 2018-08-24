#! /usr/bin/python3

import pygame
from pygame.sprite import Sprite

class Unguent(Sprite):
    def __init__(s, settings, screen):
        super().__init__()
        s.sc = screen   # short names for often-used data members
        s.se = settings
        s.nblocks = s.se.unguent_blocks

        # SIZE: make a Rect that is nblocks full spacings wide
        # we will draw individual unguent blocks inside it
        rectw = s.se.spacing*s.nblocks # one spacing per block
        recth = s.se.spacing+s.se.blockborder+1 # extra pixel to detect adjacent collision
        s.rect = pygame.Rect(0,0, rectw, recth)

        # POSITION: 'centered' at the top of the screen
        if s.nblocks%2: # odd  nblocks start lesser half left of center
           half = s.nblocks // 2
           ctrx = s.se.scw // 2
           s.rect.left = ctrx - half*s.se.spacing
        else:              # even nblocks start split by screen center
           s.rect.centerx = screen.get_rect().centerx

        # assign random colors per block from colors in settings
        s.colors = []
        for i in range(s.nblocks):
            s.colors.append(s.se.random_color())

        # start out moving down
        s.moving_down = True
        s.topy = 0.0
        s.move = ''


    def render(s):
        bb = s.se.blockborder
        bs = s.se.blocksize
        lx = s.rect.left # left of whole bounding rectangle
        if s.se.unguent_smooth:  # move every pixel
            s.rect.top = int(s.topy)
        else:  # move only in discrete jumps
            # use truncating integer division
            rows = int(s.topy)//s.se.spacing
            s.rect.top = rows * s.se.spacing
        ty = s.rect.top

        for c in s.colors: # draw each box its own color
            r = pygame.Rect(0,0, bs, bs)
            r.left = lx + bb
            r.top  = ty + bb
            pygame.draw.rect(s.sc, c, r)
            lx += s.se.spacing # scoot right for next box

    def update(s, bacteria):
        # DOWNWARD movement is automatic
        # stop moving at the bottom of the screen
        if s.topy+s.se.spacing >= s.se.screenh:
           s.moving_down = False
        # if we are still moving, apply fractional distance
        if s.moving_down:
           s.topy += s.se.unguent_speed

        if s.move == '': # if no action from user
            return       # we're done

        # HORIZONTAL movement is by user keypress
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






