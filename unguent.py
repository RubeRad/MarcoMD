#! /usr/bin/python3

import pygame
from pygame.sprite import Sprite

class Unguent(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.nblocks = settings.unguent_blocks

        # SIZE: make a Rect that is nblocks full spacings wide
        # we will draw individual unguent blocks inside it
        rectw = settings.spacing*self.nblocks # one spacing per block
        recth = settings.spacing+settings.blockborder+1 # extra pixel to detect adjacent collision
        self.rect = pygame.Rect(0,0, rectw, recth)

        # POSITION: 'centered' at the top of the screen
        if self.nblocks%2: # odd  nblocks start lesser half left of center
           half = self.nblocks // 2
           ctrx = settings.screenw // 2
           self.rect.left = ctrx - half*settings.spacing
        else:              # even nblocks start split by screen center
           self.rect.centerx = screen.get_rect().centerx

        # assign random colors per block from colors in settings
        self.colors = []
        for i in range(self.nblocks):
            self.colors.append(settings.random_color())

        # start out moving down
        self.moving_down = True
        self.topy = 0.0


    def render(self):
        bb = self.settings.blockborder
        bs = self.settings.blocksize
        lx = self.rect.left # left of whole bounding rectangle
        if self.settings.unguent_smooth:  # move every pixel
            self.rect.top = int(self.topy)
        else:  # move only in discrete jumps
            # use truncating integer division
            rows = int(self.topy)//self.settings.spacing
            self.rect.top = rows * self.settings.spacing
        ty = self.rect.top

        for c in self.colors: # draw each box its own color
            r = pygame.Rect(0,0, bs, bs)
            r.left = lx + bb
            r.top  = ty + bb
            pygame.draw.rect(self.screen, c, r)
            lx += self.settings.spacing # scoot right for next box

    def update(self):
        # stop moving at the bottom of the screen
        if self.topy+self.settings.spacing >= self.settings.screenh:
           self.moving_down = False
        # if we are still moving, apply fractional distance
        if self.moving_down:
           self.topy += self.settings.unguent_speed





