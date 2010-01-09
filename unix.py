# -*- coding: iso-8859-1 -*-
from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input

from pymouse import PyMouseMeta

display = Display()

class PyMouse(PyMouseMeta):

    def press(self, x, y, button = 1):
    	self.move(x, y)
	fake_input(display, X.ButtonPress, [None, 1, 3, 2][button])
        display.sync()

    def release(self, x, y, button = 1):
    	self.move(x, y)
	fake_input(display, X.ButtonRelease, [None, 1, 3, 2][button])
        display.sync()

    def move(self, x, y):
	fake_input(display, X.MotionNotify, x=x, y=y)
        display.sync()

    def position(self):
        coord = display.screen().root.query_pointer()._data
        return coord["root_x"], coord["root_y"]

    def screen_size(self):
        width = display.screen().width_in_pixels
        height = display.screen().height_in_pixels
        return width, height
