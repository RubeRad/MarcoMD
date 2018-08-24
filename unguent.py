#! /usr/bin/python3

import pygame
from pygame.sprite import Sprite

class Unguent(Sprite):
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.nblocks = settings.unguent_blocks
        # make a Rect that is nblocks full spacings wide
        # we will draw individual unguent blocks inside it
        self.rect = pygame.Rect(0,0, settings.spacing*self.nblocks, settings.blocksize)
        if self.nblocks%2: # odd  nblocks start lesser half left of center
            self.rect.left = (settings.cols//2-self.nblocks//2) * settings.spacing
        else:              # even nblocks start split by screen center
            self.rect.centerx = screen.get_rect().centerx
        self.rect.top = screen.get_rect().top
        self.colors = []
        for i in range(self.nblocks):
            self.colors.append(settings.random_color())

        # start out moving down
        self.moving_down = True
        self.topx = 0.0


    def render(self):
        bb = self.settings.blockborder
        bs = self.settings.blocksize
        lx = self.rect.left + bb
        ty = int(self.topx) + bb
        for c in self.colors:
            r = pygame.Rect(0,0, bs, bs)
            r.left = lx
            r.top  = ty
            pygame.draw.rect(self.screen, c, r)
            lx += self.settings.spacing

    def update(self):
        if self.moving_down and self.topx+self.settings.blocksize < self.screen.get_rect().bottom:
            self.topx += self.settings.unguent_speed
        self.rect.top = int(self.topx)




