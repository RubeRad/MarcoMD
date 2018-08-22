#! /usr/bin/python3

class Settings:
    def __init__(self):
        self.screenw = 400
        self.screenh = 700
        self.blockw  = 8
        self.blockh  = 8
        self.spacing = 10
        self.colors  = [(255,0,0), # red
                        (0,255,0), # green
                        (0,0,255)] # blue