__author__ = 'schaef'

import time
import curses

import grovepi
from grove_rgb_lcd import *


class Widget:

    def __init__(self, max_w=15):
        self.max_w = max_w
        self.line1 = "line 1 .... and some other text."
        self.line2 = "line 2"
        self.last_refresh = time.time()
        self.roll_offset = 0
        self.dirty = False

    def is_dirty(self):
        return self.dirty

    def refresh(self):
        self.dirty = False
        #self.debug_draw(self.line1, self.line2)
        self.draw(self.line1, self.line2)
        pass

    def click(self):
        self.line2 = "CLICK!"
        pass

    def dial(self, value):
        self.line2 = "dial {0}".format(value)
        pass

    def draw(self, line1, line2):
        setText("{0}\n{1}".format(self.roll_line(line1), line2[:self.max_w]))
        pass

    def roll_line(self, line):
        if len(line) < self.max_w:
            return line
        #self.dirty = True
        # add a padding of the length of the display to the right of the string.
        padding = ' '*self.max_w
        padded_line = line + padding
        # update the offset of the rolling string
        #self.roll_offset += (time.time()-self.last_refresh)
        #self.roll_offset %= len(padded_line)
        return padded_line[int(self.roll_offset):(self.max_w+int(self.roll_offset))]

    def debug_draw(self, line1, line2):
        screen = curses.initscr()

        screen.clear()
        screen.border(0)
        screen.addstr(2, 2, "UI Demo.")
        screen.addstr(3, 4, "Press Up/Down to turn the dial left or right. Press Right to simulate a click.")

        self.last_refresh = time.time()
        screen.addstr(9, 2, self.roll_line(line1))
        screen.addstr(10, 2, line2[:self.max_w])

        screen.refresh()


