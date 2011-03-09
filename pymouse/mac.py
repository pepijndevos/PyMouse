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
from base import PyMouseMeta, PyMouseEventMeta

pressID = [None, kCGEventLeftMouseDown, kCGEventRightMouseDown, kCGEventOtherMouseDown]
releaseID = [None, kCGEventLeftMouseUp, kCGEventRightMouseUp, kCGEventOtherMouseUp]



def get_button_code(event_message):
    """ Platform specific ! """
    
    if type in pressID:
        code = pressID.index(type)
        state = True
    elif type in releaseID:
        code = releaseID.index(type)
        state = False
    else:
        code = None
        state = False
            
    return (code, state)


def get_event_code(button_code, state):
    """ Platform specific ! """
    
    if state:
        code = pressID[button_code]
        
    else:
        code = releaseID[button_code]
        
    return code



class PyMouse(PyMouseMeta):
    def press(self, x, y, button=1):
        event = CGEventCreateMouseEvent(None, get_event_code(button, True), (x, y), button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def release(self, x, y, button=1):
        event = CGEventCreateMouseEvent(None, get_event_code(button, False), (x, y), button - 1)
        CGEventPost(kCGHIDEventTap, event)

    def move(self, x, y):
        move = CGEventCreateMouseEvent(None, kCGEventMouseMoved, (x, y), 0)
        CGEventPost(kCGHIDEventTap, move)
        

    def position(self):
        loc = NSEvent.mouseLocation()
        return loc.x, CGDisplayPixelsHigh(0) - loc.y

    def screen_size(self):
        return CGDisplayPixelsWide(0), CGDisplayPixelsHigh(0)

class PyMouseEvent(PyMouseEventMeta):
    def run(self):
        tap = CGEventTapCreate(
            kCGSessionEventTap,
            kCGHeadInsertEventTap,
            kCGEventTapOptionDefault,
            CGEventMaskBit(kCGEventMouseMoved) | 
            CGEventMaskBit(kCGEventLeftMouseDown) | 
            CGEventMaskBit(kCGEventLeftMouseUp) | 
            CGEventMaskBit(kCGEventRightMouseDown) | 
            CGEventMaskBit(kCGEventRightMouseUp) | 
            CGEventMaskBit(kCGEventOtherMouseDown) | 
            CGEventMaskBit(kCGEventOtherMouseUp),
            self.handler,
            None)

        loopsource = CFMachPortCreateRunLoopSource(None, tap, 0)
        loop = CFRunLoopGetCurrent()
        CFRunLoopAddSource(loop, loopsource, kCFRunLoopDefaultMode)
        CGEventTapEnable(tap, True)

        while self.state:
            CFRunLoopRunInMode(kCFRunLoopDefaultMode, 5, False)

    def handler(self, proxy, type, event, refcon):
        (x, y) = CGEventGetLocation(event)
        
        (code, state) = get_button_code(type)
        
        if code is not None:
            self.click(x, y, code, state)
        else:
            self.move(x, y)
        
        if self.capture:
            CGEventSetType(event, kCGEventNull)

        return event
