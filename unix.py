# -*- coding: iso-8859-1 -*-
from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
from Xlib.ext import record
from Xlib.protocol import rq

from pymouse import PyMouseMeta, PyMouseEventMeta

display = Display(':0')

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

class PyMouseEvent(PyMouseEventMeta):
    ctx = display.record_create_context(
        0,
        [record.AllClients],
        [{
                'core_requests': (0, 0),
                'core_replies': (0, 0),
                'ext_requests': (0, 0, 0, 0),
                'ext_replies': (0, 0, 0, 0),
                'delivered_events': (0, 0),
                'device_events': (X.ButtonPressMask, X.ButtonReleaseMask),
                'errors': (0, 0),
                'client_started': False,
                'client_died': False,
        }])

    def run(self):
        if self.capture:
            display.screen().root.grab_pointer(True, X.ButtonPressMask | X.ButtonReleaseMask | X.MotionNotify, X.GrabModeAsync, X.GrabModeAsync, 0, 0, X.CurrentTime)

        display.record_enable_context(self.ctx, self.handler)
        display.record_free_context(self.ctx)
    
    def stop(self):
        # This stuff should tear things down, but it does not work.
        display.record_disable_context(self.ctx)
        display.ungrab_pointer(X.CurrentTime)
        display.flush()

        # That is why I simply set the handler functions to empty ones
        def empty(*args):
            pass

        self.click = empty
        self.move = empty

    def handler(self, reply):
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, display.display, None, None)
            
            if event.type == X.ButtonPress:
                self.click(event.root_x, event.root_y, (None, 1, 3, 2)[event.detail], True)
            elif event.type == X.ButtonRelease:
                self.click(event.root_x, event.root_y, (None, 1, 3, 2)[event.detail], False)
            else:
                self.move(event.root_x, event.root_y)
            

