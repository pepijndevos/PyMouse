'''
Tested on linux.

install:  Xvfb, Xephyr, PyVirtualDisplay, nose

on Ubuntu:

    sudo apt-get install python-nose
    sudo apt-get install xvfb 
    sudo apt-get install xserver-xephyr
    sudo apt-get install python-setuptools
    sudo easy_install PyVirtualDisplay

'''

from nose.tools import eq_
from pymouse import PyMouse, PyMouseEvent
from pyvirtualdisplay import Display
from unittest import TestCase
import time

# 0 -> Xvfb
# 1 -> Xephyr
VISIBLE = 0

screen_sizes = [
              (10, 20),
              (100, 200),
              (765, 666),
              ]
positions = [
              (0, 5),
              (0, 0),
              (10, 20),
              (-10, -20),
              (5, 0),
              (2222, 2222),
              (9, 19),
              ]


class Event(PyMouseEvent):
    def move(self, x, y):
        print "Mouse moved to", x, y
        self.pos = (x, y)

    def click(self, x, y, button, press):
        if press:
            print "Mouse pressed at", x, y, "with button", button
        else:
            print "Mouse released at", x, y, "with button", button

def expect_pos(pos, size):
    def expect(x, m):
        x = max(0, x)
        x = min(m - 1, x)
        return x
    expected_pos = (expect(pos[0], size[0]), expect(pos[1], size[1]))
    return expected_pos

class Test(TestCase):
    def test_size(self):
        for size in screen_sizes:
            try:
                disp = Display(visible=VISIBLE, size=size).start()
                mouse = PyMouse()
                eq_(size, mouse.screen_size())
            finally:
                disp.stop()

    def test_move(self):
        for size in screen_sizes:
            try:
                disp = Display(visible=VISIBLE, size=size).start()
                mouse = PyMouse()
                for p in positions:
                    mouse.move(*p)
                    eq_(expect_pos(p, size), mouse.position())
            finally:
                disp.stop()

    def test_event(self):
        '''this fails with current version'''
        for size in screen_sizes:
            try:
                disp = Display(visible=VISIBLE, size=size).start()
                mouse = PyMouse()
                event = Event()
                event.start()
                for p in positions:
                    event.pos = None
                    mouse.move(*p)
                    eq_(expect_pos(p, size), event.pos)
                event.stop()                
            finally:
                disp.stop()
        
        
