# -*- coding: iso-8859-1 -*-
from Quartz import *
from AppKit import NSEvent
from pymouse import PyMouseMeta

pressID = [None, kCGEventLeftMouseDown, kCGEventRightMouseDown, kCGEventOtherMouseDown]
releaseID = [None, kCGEventLeftMouseUp, kCGEventRightMouseUp, kCGEventOtherMouseUp]

class PyMouse(PyMouseMeta):
    def press(self, x, y, button = 1):
        event = CGEventCreateMouseEvent(None, pressID[button], (x, y), button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def release(self, x, y, button = 1):
        event = CGEventCreateMouseEvent(None, releaseID[button], (x, y), button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def move(self, x, y):
        move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
        CGEventPost(kCGHIDEventTap, move)
        

    def position(self):
        loc = NSEvent.mouseLocation()
        return int(loc.x), int(CGDisplayPixelsHigh(0) - loc.y)

    def screen_size(self):
        return CGDisplayPixelsWide(0), CGDisplayPixelsHigh(0)
