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

from Quartz import *
from AppKit import NSEvent
from pymouse.base import PyMouseMeta

pressID = [None, kCGEventLeftMouseDown, kCGEventRightMouseDown, kCGEventOtherMouseDown]
releaseID = [None, kCGEventLeftMouseUp, kCGEventRightMouseUp, kCGEventOtherMouseUp]

class PyMouse(PyMouseMeta):
    def _button_event(self, x, y, button_event, button, event_series_num):
        event = CGEventCreateMouseEvent(None, button_event, (x, y), button - 1)
        CGEventSetIntegerValueField(event, kCGMouseEventClickState, event_series_num)
        CGEventPost(kCGHIDEventTap, event)

    def press(self, x, y, button = 1):
        self._button_event(x, y, pressID[button], button, 1)

    def release(self, x, y, button = 1):
        self._button_event(x, y, releaseID[button], button, 1)

    def doubleclick(self, x, y, button=1):
        self._button_event(x, y, pressID[button], button, 1)
        self._button_event(x, y, releaseID[button], button, 1)
        self._button_event(x, y, pressID[button], button, 2)
        self._button_event(x, y, releaseID[button], button, 2)

    def move(self, x, y):
        move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
        CGEventPost(kCGHIDEventTap, move)

    def position(self):
        loc = NSEvent.mouseLocation()
        return loc.x, CGDisplayPixelsHigh(0) - loc.y

    def screen_size(self):
        return CGDisplayPixelsWide(0), CGDisplayPixelsHigh(0)
