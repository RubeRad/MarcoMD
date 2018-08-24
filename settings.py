#! /usr/bin/python3

import random

class Settings:
    def __init__(self):
        self.bg_color = (0,0,0) # black
        self.cols = 8  # should be even
        self.rows = 15
        self.blockrows = 8
        self.blocksize = 16 # pixels
        self.blockborder = 2 # pixels all around
        self.spacing = self.blocksize + self.blockborder*2
        self.screenw = self.spacing*self.cols
        self.screenh = self.spacing*self.rows

        self.n_bacteria = 4
        self.colors  = [(255,0,0),   # red
                        (0,0,255),   # blue
                        (255,255,0)] # yellow

        self.unguent_blocks = 2
        self.unguent_speed = 0.1
        self.unguent_smooth = False

    def random_color(self):
        ncolors = len(self.colors)
        index = random.randint(0, ncolors-1)
        return self.colors[index]