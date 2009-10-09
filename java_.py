# -*- coding: iso-8859-1 -*-
from java.awt import Robot, Toolkit
from java.awt.event import InputEvent
from java.awt.MouseInfo import getPointerInfo
from pymouse import PyMouseMeta

r = Robot()

class PyMouse(PyMouseMeta):
    def press(self, x, y, button = 1):
        button_list = [None, InputEvent.BUTTON1_MASK, InputEvent.BUTTON3_MASK, InputEvent.BUTTON2_MASK]
        self.move(x, y)
        r.mousePress(button_list[button])

    def release(self, x, y, button = 1):
        button_list = [None, InputEvent.BUTTON1_MASK, InputEvent.BUTTON3_MASK, InputEvent.BUTTON2_MASK]
        self.move(x, y)
        r.mouseRelease(button_list[button])
    
    def move(self, x, y):
        r.mouseMove(x, y)

    def position(self):
        loc = getPointerInfo().getLocation()
        return loc.getX, loc.getY

    def screen_size(self):
        dim = Toolkit.getDefaultToolkit().getScreenSize()
        return dim.getWidth(), dim.getHeight()
