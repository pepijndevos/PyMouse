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

import Quartz
from AppKit import NSEvent
from base import PyMouseMeta, PyMouseEventMeta

pressID = [None, Quartz.kCGEventLeftMouseDown, Quartz.kCGEventRightMouseDown, Quartz.kCGEventOtherMouseDown]
releaseID = [None, Quartz.kCGEventLeftMouseUp, Quartz.kCGEventRightMouseUp, Quartz.kCGEventOtherMouseUp]

class PyMouse(PyMouseMeta):
    def press(self, x, y, button = 1):
        event = Quartz.CGEventCreateMouseEvent(None, pressID[button], (x, y), button - 1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    def release(self, x, y, button = 1):
        event = Quartz.CGEventCreateMouseEvent(None, releaseID[button], (x, y), button - 1)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    def move(self, x, y):
        move = Quartz.CGEventCreateMouseEvent(None, Quartz.kCGEventMouseMoved, (x, y), 0)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, move)
        

    def position(self):
        loc = NSEvent.mouseLocation()
        return loc.x, Quartz.CGDisplayPixelsHigh(0) - loc.y

    def screen_size(self):
        return Quartz.CGDisplayPixelsWide(0), Quartz.CGDisplayPixelsHigh(0)

class PyMouseEvent(PyMouseEventMeta):
    def run(self):
        tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,
            Quartz.kCGHeadInsertEventTap,
            Quartz.kCGEventTapOptionDefault,
            Quartz.CGEventMaskBit(Quartz.kCGEventMouseMoved) |
            Quartz.CGEventMaskBit(Quartz.kCGEventLeftMouseDown) |
            Quartz.CGEventMaskBit(Quartz.kCGEventLeftMouseUp) |
            Quartz.CGEventMaskBit(Quartz.kCGEventRightMouseDown) |
            Quartz.CGEventMaskBit(Quartz.kCGEventRightMouseUp) |
            Quartz.CGEventMaskBit(Quartz.kCGEventOtherMouseDown) |
            Quartz.CGEventMaskBit(Quartz.kCGEventOtherMouseUp),
            self.handler,
            None)

        loopsource = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
        loop = Quartz.CFRunLoopGetCurrent()
        Quartz.CFRunLoopAddSource(loop, loopsource, Quartz.kCFRunLoopDefaultMode)
        Quartz.CGEventTapEnable(tap, True)

        while self.state:
            Quartz.CFRunLoopRunInMode(Quartz.kCFRunLoopDefaultMode, 5, False)

    def handler(self, proxy, type, event, refcon):
        (x, y) = Quartz.CGEventGetLocation(event)
        if type in pressID:
            self.click(x, y, pressID.index(type), True)
        elif type in releaseID:
            self.click(x, y, releaseID.index(type), False)
        else:
            self.move(x, y)
        
        if self.capture:
            Quartz.CGEventSetType(event, Quartz.kCGEventNull)

        return event
