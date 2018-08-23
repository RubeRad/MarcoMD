#! /usr/bin/python3

class Settings:
    def __init__(self):
        self.screenw = 400
        self.screenh = 700
        self.blockw  = 16
        self.blockh  = 16
        self.spacing = 20
        self.cols = self.screenw // self.spacing
        self.rows = 20
        self.n_bacteria = 10
        self.colors  = [(255,0,0),   # red
                        (0,0,255),   # blue
                        (255,255,0)] # yellow