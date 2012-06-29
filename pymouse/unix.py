# -*- coding: iso-8859-1 -*-

#   Copyright 2010 Pepijn de Vos
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input

from pymouse.base import PyMouseMeta


class PyMouse(PyMouseMeta):
    def __init__(self):
        PyMouseMeta.__init__(self)
        self.display = Display()
        self.display2 = Display()

    def press(self, x, y, button = 1):
        self.move(x, y)
        fake_input(self.display, X.ButtonPress, [None, 1, 3, 2, 4, 5][button])
        self.display.sync()

    def release(self, x, y, button = 1):
        self.move(x, y)
        fake_input(self.display, X.ButtonRelease, [None, 1, 3, 2, 4, 5][button])
        self.display.sync()

    def move(self, x, y):
        fake_input(self.display, X.MotionNotify, x=x, y=y)
        self.display.sync()

    def position(self):
        coord = self.display.screen().root.query_pointer()._data
        return coord["root_x"], coord["root_y"]

    def screen_size(self):
        width = self.display.screen().width_in_pixels
        height = self.display.screen().height_in_pixels
        return width, height
