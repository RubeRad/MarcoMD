#! /usr/bin/python3

import time
import pygame
from pygame.sprite import Sprite
from settings import Settings

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
        s.set_rect(c,r,o)

        # start out moving down
        s.moving_down = True
        #s.topy = s.rect.top
        s.move = ''
        s.key_just_pressed = False
        s.time_move = time.perf_counter()
        s.time_fall = s.time_move

    def set_rect(s, c, r, o):
        s.c0 = c
        s.r0 = r
        s.orientation = o

        # first set the size
        if s.orientation in (0,2): # horizontal
            s.rect.width  = s.se.spacing * s.nblocks
            s.rect.height = s.se.spacing
        else:                      # vertical
            s.rect.width  = s.se.spacing
            s.rect.height = s.se.spacing * s.nblocks

        # then place that size by setting position
        if s.orientation in (0,1): # l->r, t->b
            s.rect.left   = s.se.spacing * c
            s.rect.top    = s.se.spacing * r
        else:
            s.rect.right  = s.se.spacing * (c+1)
            s.rect.bottom = s.se.spacing * (r+1)

    def first_block_col_row(s): # col,row index of only 'first' block
        #if s.orientation in (0, 1):  # l->r/t->b: grab top/left block
        #    row = (s.rect.top    + s.se.blockborder) // s.se.spacing
        #    col = (s.rect.left   + s.se.blockborder) // s.se.spacing
        #else:  # r->l/b->t: grab bottom/right blocks
        #    row = (s.rect.bottom - s.se.blocksize)   // s.se.spacing
        #    col = (s.rect.right  - s.se.blocksize)   // s.se.spacing
        #if col != s.c0 or row != s.r0:
        #    stophere=1
        #return (col,row)
        return (s.c0, s.r0)

    def orientation_dc_dr(s):
        if s.orientation == 0: return (1, 0)
        if s.orientation == 1: return (0, 1)
        if s.orientation == 2: return (-1, 0)
        if s.orientation == 3: return (0, -1)

    def block_col_row(s, i):
        c0,r0 = s.first_block_col_row()
        dc,dr = s.orientation_dc_dr()
        return (c0+i*dc, r0+i*dr)

    # if this unguent doesn't include r,c, return -1
    # if it does, return 0 for 'first' block, etc.
    def index_of(s, r, c):
        c0,r0 = s.first_block_col_row()
        dc,dr = s.orientation_dc_dr()
        cN = c0 + dc*(s.nblocks-1)
        rN = r0 + dr*(s.nblocks-1)
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

    def bottom_cols_rows(s):
        dc,dr = s.orientation_dc_dr()
        crs = []
        if s.orientation in (0,2):
            for i in range(s.nblocks):
                crs.append( (s.c0+i*dc, s.r0) )
        elif s.orientation == 3: # c0,r0 is bottom
            crs.append( (s.c0, s.r0) )
        else: # orientation 1, c0, r0 is top
            crs.append( (s.c0, s.r0 - s.nblocks + 1) )

    def free_to_move(s, statics):
        s.set_rect(s.c0, s.r0+1, s.orientation)
        if s.rect.bottom > s.se.screenh or pygame.sprite.spritecollideany(s, statics, False):
            s.set_rect(s.c0, s.r0-1, s.orientation)
            s.moving_down = False
        else:
            s.moving_down = True
        return s.moving_down

    def render(s):
        bb = s.se.blockborder
        bs = s.se.blocksize
        sp = s.se.spacing
        col,row = s.first_block_col_row()
        dcol,drow = s.orientation_dc_dr()

        for c in s.colors: # draw each box its own color
            r = pygame.Rect(col*sp+bb, row*sp+bb, bs, bs)
            pygame.draw.rect(s.sc, c, r)
            col += dcol # scoot for next block
            row += drow

    def update(s, bacteria):
        if not s.moving_down: # shouldn't happen much
            return

        curt = time.perf_counter()
        dt_move = curt - s.time_move
        dt_fall = curt - s.time_fall
        if not s.move and dt_fall < s.se.s_fall:
            # no user key, not time for automatic drop yet
            return
        if s.move and not s.key_just_pressed and dt_move < s.se.s_move:
            # key held down, not time to move again yet
            return

        # so either we need to act on user keypress, or do an
        # automatic drop i.e. a movement is definitely happening

        # ROTATION is by user keypress
        if s.move in (s.se.key_cw, s.se.key_ccw):
            # save time of rotation for proper delay to next one
            s.time_move = curt
            # save current state in case rotation collides
            csav,rsav,osav = s.c0, s.r0, s.orientation
            if s.move == s.se.key_cw: dori=+1
            else:                     dori=-1
            onew = (s.orientation+dori)%4
            s.set_rect(s.c0, s.r0, onew)

            # if new orientation collides, undo it
            if pygame.sprite.spritecollideany(s, bacteria, False):
                s.set_rect(csav, rsav, osav)
                s.move = ''
            else: # check if rotation goes off screen right or left, bump it
                if s.rect.left  < 0:
                    s.set_rect(s.c0+1, s.r0, s.orientation)
                if s.rect.right > s.se.screenw:
                    s.set_rect(s.c0-1, s.r0, s.orientation)
            # check again (the bump might have caused a collision)
            if pygame.sprite.spritecollideany(s, bacteria, False):
                s.set_rect(csave, rsav, osav)
                s.move = ''

        # HORIZONTAL movement is by user keypress
        elif s.move in (s.se.key_left, s.se.key_rght):
            s.time_move = curt # for proper delay to next move
            csav = s.c0        # to restore in case of collision
            if   s.move == s.se.key_left: s.set_rect(s.c0-1, s.r0, s.orientation)
            elif s.move == s.se.key_rght: s.set_rect(s.c0+1, s.r0, s.orientation)
            # test if we go off the screen or collide with any bacteria
            undo = False
            if s.rect.left  <  0:           undo = True
            if s.rect.right > s.se.screenw: undo = True
            if pygame.sprite.spritecollide(s, bacteria, False):
                                            undo = True
            if undo:
                s.set_rect(csav, s.r0, s.orientation)
                s.move = ''

        # DOWNWARD movement is automatic (or keypress-accelerated)
        # Even if we did keypress movements above, it might be
        # time for a one-row drop as well
        like_its_hot=False
        if dt_fall > s.se.s_fall:
            like_its_hot = True
        if s.move == s.se.key_down:
            if dt_move > s.se.s_move or s.key_just_pressed:
                like_its_hot = True
                s.time_move = curt
        if like_its_hot: # drop it
            s.set_rect(s.c0, s.r0+1, s.orientation) # try it
            s.time_fall = curt

        # stop moving at the bottom of the screen, or hitting a static
        if s.rect.bottom > s.se.screenh or pygame.sprite.spritecollide(s, bacteria, False):
           # too far!
           s.set_rect(s.c0, s.r0-1, s.orientation) # undo it
           s.moving_down = False
           s.move = ''

        s.key_just_pressed = False # not any more

    # rcs are (row,col) tuples of blocks currently being erased
    # split this unguent apart at erased blocks and return new
    # unguents for the segments that are not erased
    # if none of these blocks are erased, do nothing and return None
    # if entire Unguent is erased return empty list []
    def denature(s, rcs):
        indices = []
        for r,c in rcs:
            i = s.index_of(r,c)
            if i!=-1:
                indices.append(i)
        if len(indices) == 0: # no blocks erased
            return None       # return None
        # Otherwise some blocks are erased. What's left?

        indices.sort()
        i = indices.pop() # the last index

        # what is after that last index?
        aft_len = s.nblocks-(i+1)
        if aft_len == 0:
            aft = None
        else:
            col,row = s.block_col_row(i+1)
            aft = Unguent(s.se, s.sc, r=row, c=col, o=s.orientation, clist=s.colors[i+1:])

        # make an Unguent before i and recursively denature it
        bef_len = i-0
        if bef_len == 0:
            befs = None
        else:
            col,row = s.first_block_col_row()
            bef = Unguent(s.se, s.sc, r=row, c=col, o=s.orientation, clist=s.colors[0:i])
            befs = bef.denature(rcs)
            if befs==None: # bef not hit by rcs, it is a whole piece
                befs = [bef]

        returns = []
        if befs: returns.extend(befs)
        if aft:  returns.append(aft)
        return returns


#######################
##### UNIT TESTS ######
#######################
import unittest
if __name__ == '__main__':
    class UnguentTester(unittest.TestCase):
        def testDenaturing(s):
            se = Settings()
            # this guy is r,c 5,6 and 5,7
            u = Unguent(se, None, r=5, c=6, o=0, clist=[1,2])

            # test erasing both
            ms = u.denature([(5,6), (5,7), (5,8)]) # 5,8 just for funsies
            s.assertEqual(len(ms), 0, 'should return 0 movers')

            # test erasing 5,6
            ms = u.denature([(5,6)])
            s.assertEqual(len(ms), 1, 'should return 1 mover')
            m = ms.pop()
            s.assertEqual(m.nblocks, 1, 'should be nblocks==1')
            s.assertTrue(len(m.colors)==1 and m.colors[0]==2, 'should be color 2')
            c,r = m.first_block_col_row()
            s.assertTrue(r==5 and c==7, 'should return r,c 5,7')

            # test erasing 5,7
            ms = u.denature([(5,7)])
            s.assertEqual(len(ms), 1, 'should return 1 mover')
            m = ms.pop()
            s.assertEqual(m.nblocks, 1, 'should be nblocks==1')
            s.assertTrue(len(m.colors)==1 and m.colors[0]==1, 'should be color 2')
            c,r = m.first_block_col_row()
            s.assertTrue(r==5 and c==6, 'should return r,c 5,6')

            # Issue #17 vertical 3-block erases wrong
            u = Unguent(se, None, c=4, r=0, o=1, clist=[0,0,0])
            should_be_empty = u.denature([(0,4), (1,4), (2,4)])
            s.assertEqual(0, len(should_be_empty), 'fully-erased 3-block should denature to nothing')

    unittest.main()


