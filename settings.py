#! /usr/bin/python3

import random

class Settings:
    def __init__(s):
        s.bg_color = (0,0,0) # black
        s.cols = 8  # should be even
        s.rows = 15
        s.blockrows = 8
        s.blocksize = 16 # pixels
        s.blockborder = 2 # pixels all around
        s.spacing = s.blocksize + s.blockborder*2
        s.screenw = s.spacing*s.cols
        s.screenh = s.spacing*s.rows

        s.n_bacteria = 4
        s.colors  = [(255,0,0),   # red
                        (0,0,255),   # blue
                        (255,255,0)] # yellow

        s.unguent_blocks = 2
        s.unguent_speed = 0.05
        s.unguent_smooth = False

        s.key_left = 'a'
        s.key_rght = 'd'
        s.key_down = 's'
        s.keyset = (s.key_left, s.key_rght, s.key_down)

    def random_color(s):
        ncolors = len(s.colors)
        index = random.randint(0, ncolors-1)
        return s.colors[index]