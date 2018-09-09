# MarcoMD
A video game in python

Use the dropping Unguents to eliminate all the Bacteria. Use keys a,d,s for
left,right,drop and j,k for ccw/cw rotation. 4-in a row of the same color
(vertical or horizontal) disappears.

Take a look in settings.py to see all the game elements that can be controlled
(board size, number of bacteria, available colors, number of blocks per Unguent,
keyset).

Take a look at the history of Commits to see what kind of incremental steps got
the game to the current state.

The three most important parts of the code are probably:

* unguent.update() which decides when/where to move a falling Unguent, based on
  user keypresses

* events.detect_inarows(): is there a 4-inarow that needs erasing?

* events.clear(): erase any blocks inarow, break up any partially-erased
  Unguents so they are free to fall

Take a look at the Issues board for tasks I have in mind for future development.




