# -*- coding: iso-8859-1 -*-
import sys

LEFT = 0
RIGHT = 1
MIDDLE = 2

if sys.platform == 'darwin':
    import objc
elif sys.platform == 'win32':
    clicks = [2, 8, 32]
    releases = [4, 16, 64]

    from ctypes import *
    from win32api import GetSystemMetrics
    
    PUL = POINTER(c_ulong)
    class MouseInput(Structure):
        _fields_ = [("dx", c_long),
                 ("dy", c_long),
                 ("mouseData", c_ulong),
                 ("dwFlags", c_ulong),
                 ("time",c_ulong),
                 ("dwExtraInfo", PUL)]

    class Input_I(Union):
        _fields_ = [("mi", MouseInput)]

    class Input(Structure):
        _fields_ = [("type", c_ulong), ("ii", Input_I)]

    FInputs = Input * 2
    extra = c_ulong(0)

    click = Input_I()
    click.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
    release = Input_I()
    release.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))

    blob = FInputs( (0, click), (0, release) )
else:
    LEFT = 1
    RIGHT = 2
    MIDDLE = 3
    try:
        #from xtest import XTest
        from Xlib.display import Display
		from Xlib import X
		from Xlib.protocol import event
        import Xlib.ext.xtest
    except ImportError:
        print "Your system is not supported"

class PyMouse(object):

    def click(self, x, y, button = LEFT):
        if sys.platform == 'darwin':
            bndl = objc.loadBundle('CoreGraphics', globals(), \
                                    '/System/Library/Frameworks/ApplicationServices.framework')
            objc.loadBundleFunctions(bndl, globals(), [('CGPostMouseEvent', \
                                    'v{CGPoint=ff}IIIII')])
            button_list = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            CGPostMouseEvent((float(x), float(y)), 1, 3, *button_list[button])
            CGPostMouseEvent((float(x), float(y)), 1, 3, 0, 0, 0)

        elif sys.platform == 'win32':
            windll.user32.SetCursorPos(x, y)
            blob[0].ii.mi.dwFlags = clicks[button]
            blob[1].ii.mi.dwFlags = releases[button]
            windll.user32.SendInput(2,pointer(blob),sizeof(blob[0]))

        else:
            display = Display(':0') #Default display fails on Mac
            focus = display.get_input_focus().focus
			root = display.screen().root
			rel = focus.translate_coords(root, x, y)
			button_list = [X.Button1, X.Button2, X.Button3]
			
            try:
				mousePress = event.ButtonPress(
				    time=X.CurrentTime,
				    root=root,
				    window=focus,
				    same_screen=1,
				    child=X.NONE,
				    root_x=x,
				    root_y=y,
				    event_x=rel.x,
				    event_y=rel.y,
				    state=0,
				    detail=button_list[button]
				    )
				
				mouseRealease = event.ButtonRelease(
				    time=X.CurrentTime,
				    root=root,
				    window=focus,
				    same_screen=1,
				    child=X.NONE,
				    root_x=x,
				    root_y=y,
				    event_x=rel.x,
				    event_y=rel.y,
				    state=1,
				    detail=button_list[button]
				    )
				 
				focus.send_event(mousePress)
				focus.send_event(mouseRealease)
            except:
                ##Using xlib-xtest fake input
                display.screen().root.warp_pointer(x, y) # I believe you where not setting the position
                Xlib.ext.xtest.fake_input (d, X.ButtonPress, button)
            display.sync()

    def move(self, x, y):
        if sys.platform == 'darwin':
            bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
            objc.loadBundleFunctions(bndl, globals(), [('CGWarpMouseCursorPosition', 'v{CGPoint=ff}')])
            CGWarpMouseCursorPosition((float(x), float(y)))
        elif sys.platform == 'win32':
            windll.user32.SetCursorPos(x, y)
        else:
            display = Display(':0')
            display.screen().root.warp_pointer(x, y)
            display.sync()

    def whereis(self):
        if sys.platform == 'darwin':
            #need to know how
            return 0, 0
        elif sys.platform == 'win32':
            #need to know how
            return 0, 0
        else:
            display = display.Display()
            coord = display.screen().root.query_pointer()._data
            return coord["root_x"], coord["root_y"]

    def screen_size(self):
        if sys.platform == 'darwin':
            #need to know how
            width, height= 0, 0
        elif sys.platform == 'win32':
        	#untested
            width = GetSystemMetrics(0)
            height = GetSystemMetrics(1)
        else:
            display = display.Display()
            width = display.screen().width_in_pixels
            height = display.screen().height_in_pixels
        return (width, height)

if __name__ == "__main__":
    import random, time
    m = PyMouse()
    try:
        size= m.screen_size()
        print "size: %s" % (str(size))

        pos= (random.randint(0, size[0]), random.randint(0, size[1]))
    except:
        pos= (random.randint(0, 250), random.randint(0, 250))
    print "Position: %s" % (str(pos))

    print 'move'
    m.move(pos[0], pos[1])

    time.sleep(5)

    print 'click'
    m.click(pos[0], pos[1], LEFT)
