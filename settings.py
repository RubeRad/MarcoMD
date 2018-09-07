#! /usr/bin/python3

import random
import argparse

class Settings:
    def __init__(s):
        s.bg_color = (0,0,0) # black
        s.cols = 8  # should be even
        s.rows = 15
        s.blockrows = int(s.rows*0.55) # i.e. default 8
        s.blocksize = 16 # pixels
        s.blockborder = 2 # pixels all around
        s.spacing = s.blocksize + s.blockborder*2

        s.n_bacteria = 4
        s.colors  = [(255,0,0),   # red
                        (0,0,255),   # blue
                        (255,255,0)] # yellow

        s.speed  = 1.0  # this is what default speed 1.0 means:
        s.s_fall = 1    # seconds per automatic row drop
        s.s_move = 0.2  # seconds per keyed movement

        s.key_left = 'a'
        s.key_rght = 'd'
        s.key_down = 's'
        s.key_cw   = 'k'
        s.key_ccw  = 'j'
        s.key_pause = 'p'
        s.keyset = (s.key_left, s.key_rght, s.key_down,
                    s.key_cw, s.key_ccw, s.key_pause)
        s.paused = False

        s.inarow = 4

        parser = argparse.ArgumentParser("Marco M.D.")
        parser.add_argument('--seed', type=int, default=-1,
                            help='Seed to control random number generation')
        parser.add_argument('--dims', type=str, default="8x15x4x8",
                            help='COLS[xROWS[xBLOCKS[xBLOCKROWS]]]')
        parser.add_argument('--speed', type=float, default=1.0,
                            help='Default 1.0')
        # this will go away after implementing Issue#3 (multiple unguent sizes)
        # or maybe stick around and only be able to specify a single 100% size
        parser.add_argument('--unguent_blocks', type=int, default=2)
        parser.add_argument('-v', '--verbose', action='store_true',
                            help='Print game state for later reproducibility')
        args = parser.parse_args()

        if args.seed == 0:
              s.seed = random.randint(1,1000000000) # still random but we know what it is
        else: s.seed = args.seed # specified by the user
        random.seed(s.seed)

        if args.speed < 0:
            print("Speed must be positive. 1.0=default, 2.0 is twice as fast, etc")
        s.speed   = args.speed
        s.s_fall /= args.speed
        s.s_move /= args.speed


        dims = args.dims.split('x')
        for d in dims:
            try:     i = int(d)
            except:  i = 0
            if i<=0:
                print("--dims must be positive integers separated by 'x'")
                exit(-1)
        if len(dims) >= 1: s.cols       = int(dims[0])
        if len(dims) >= 2: s.rows       = int(dims[1])
        if len(dims) >= 3: s.n_bacteria = int(dims[2])
        if len(dims) >= 4: s.blockrows  = int(dims[3])
        else:              s.blockrows  = int(s.rows*0.55)

        s.unguent_blocks = args.unguent_blocks  # default 2
        if s.unguent_blocks < 1 or s.unguent_blocks > s.cols:
            print("Invalid value for unguent_blocks")
            exit(-1)

        # now that we know how many rows/columns the screen is...
        s.screenw = s.spacing*s.cols
        s.screenh = s.spacing*s.rows

        if args.verbose:
            print('--dims '
                  + str(s.cols) + 'x'
                  + str(s.rows) + 'x'
                  + str(s.n_bacteria) + 'x'
                  + str(s.blockrows),
                  '--speed', s.speed,
                  '--unguent_blocks', s.unguent_blocks,
                  '--seed', s.seed)

    def random_color(s):
        ncolors = len(s.colors)
        index = random.randint(0, ncolors-1)
        return s.colors[index]
