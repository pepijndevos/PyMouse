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

from ctypes import *
import win32api,win32con
from pymouse.base import PyMouseMeta, PyMouseEventMeta

class POINT(Structure):
    _fields_ = [("x", c_ulong),
                ("y", c_ulong)]

class PyMouse(PyMouseMeta):
    """MOUSEEVENTF_(button and action) constants
    are defined at win32con, buttonAction is that value"""
    def press(self, x, y, button = 1):
        buttonAction = 2**((2*button)-1)
        self.move(x,y)
        win32api.mouse_event(buttonAction, x, y)

    def release(self, x, y, button = 1):
        buttonAction = 2**((2*button))
        self.move(x,y)
        win32api.mouse_event(buttonAction, x, y)

    def move(self, x, y):
        windll.user32.SetCursorPos(x, y)

    def position(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt.x, pt.y

    def screen_size(self):
        width = windll.user32.GetSystemMetrics(0)
        height = windll.user32.GetSystemMetrics(1)
        return width, height
