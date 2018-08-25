#! /usr/bin/python3

import pygame
import sys

def handle(se, u):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            c=chr(e.key) # convert number to character
            if   c == 'q':
                 sys.exit()
            elif c in se.keyset:
                 u.move = c
        elif e.type == pygame.KEYUP:
            u.move = '' # turn off key_down
