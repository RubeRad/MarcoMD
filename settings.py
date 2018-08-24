#! /usr/bin/python3

class Settings:
    def __init__(self):
        self.cols = 8
        self.rows = 15
        self.blockrows = 8
        self.blockw  = 16
        self.blockh  = 16
        self.spacing = 20
        self.screenw = self.spacing*self.cols
        self.screenh = self.spacing*self.rows
        self.n_bacteria = 4
        self.colors  = [(255,0,0),   # red
                        (0,0,255),   # blue
                        (255,255,0)] # yellow