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
import win32api, win32con
from base import PyMouseMeta, PyMouseEventMeta, MouseButtons
import pythoncom, pyHook
from time import sleep


def get_button_code(event_message):
    """ Platform specific ! """
    
    try:
        if event_message == pyHook.HookConstants.WM_LBUTTONDOWN:
           code = (MouseButtons.BUTTON_LEFT, True)
        elif event_message == pyHook.HookConstants.WM_LBUTTONUP:
           code = (MouseButtons.BUTTON_LEFT, False)
        elif event_message == pyHook.HookConstants.WM_RBUTTONDOWN:
           code = (MouseButtons.BUTTON_RIGHT, True)
        elif event_message == pyHook.HookConstants.WM_RBUTTONUP:
           code = (MouseButtons.BUTTON_RIGHT, False)
        elif event_message == pyHook.HookConstants.WM_MBUTTONDOWN:
           code = (MouseButtons.BUTTON_MIDDLE, True)
        elif event_message == pyHook.HookConstants.WM_MBUTTONUP:
           code = (MouseButtons.BUTTON_MIDDLE, False)
                
    except IndexError:
        code = (None, False)
        
    return code


def get_event_code(button_code, state):
    """ Platform specific ! """
    
    # Windows only supports Left, Middle and Right buttons
    if button_code not in (1, 2, 3):
        raise ValueError("Button not supported")
    
    # swap button 2 and 3, because Windows uses 3 for middle button and 2 for right button
    if button_code == 2:
        button_code = 3
    elif button_code == 3:
        button_code = 2
    
    if state:
        code = 2 ** ((2 * button_code) - 1)
    else:
        code = 2 ** ((2 * button_code))
        
    
    return code
    
    
    

class POINT(Structure):
    _fields_ = [("x", c_ulong),
                ("y", c_ulong)]

class PyMouse(PyMouseMeta):
    """MOUSEEVENTF_(button and action) constants 
    are defined at win32con, buttonAction is that value"""
    def press(self, x, y, button=1):
        buttonAction = get_event_code(button, True)
        self.move(x, y)
        win32api.mouse_event(buttonAction, x, y)
     
    def release(self, x, y, button=1):
        buttonAction = get_event_code(button, False)
        self.move(x, y)
        win32api.mouse_event(buttonAction, x, y)

    def move(self, x, y):
        windll.user32.SetCursorPos(x, y)

    def position(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt.x, pt.y

    def screen_size(self):
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        return width, height

class PyMouseEvent(PyMouseEventMeta):
    def __init__(self):
        PyMouseEventMeta.__init__(self)
        self.hm = pyHook.HookManager()

    def run(self):
        self.hm.MouseAllButtons = self._click
        self.hm.MouseMove = self._move
        self.hm.HookMouse()
        while self.state:
            sleep(0.01)
            pythoncom.PumpWaitingMessages()

    def stop(self):
        self.hm.UnhookMouse()
        self.state = False

    def _click(self, event):
        x, y = event.Position

        (button, state) = get_button_code(event.Message)
        
        if button is not None:
            self.click(x, y, button, state)
            
        return not self.capture

    def _move(self, event):
        x, y = event.Position
        self.move(x, y)
        return not self.captureMove
