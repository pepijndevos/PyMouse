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
        from xtest import XTest
    except ImportError:
        print "Your system is not supported, make sure you have XTest enabled"
    
class PyMouse(object):
    
    def click(self, x, y, button = LEFT):
        if sys.platform == 'darwin':
            bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
            objc.loadBundleFunctions(bndl, globals(), [('CGPostMouseEvent', 'v{CGPoint=ff}IIIII')])
            button_list = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
            CGPostMouseEvent((float(x), float(y)), 1, 3, *button_list[button])
            CGPostMouseEvent((float(x), float(y)), 1, 3, 0, 0, 0)
        elif sys.platform == 'win32':
            windll.user32.SetCursorPos(x, y)
            blob[0].ii.mi.dwFlags = clicks[button]
            blob[1].ii.mi.dwFlags = releases[button]
            windll.user32.SendInput(2,pointer(blob),sizeof(blob[0]))
        else:
            X = XTest()
            X.fakeMotionEvent(x, y)
            X.fakeButtonEvent(button, True)
            X.fakeButtonEvent(button, False)
    
    def move(self, x, y):
        if sys.platform == 'darwin':
            bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
            objc.loadBundleFunctions(bndl, globals(), [('CGWarpMouseCursorPosition', 'v{CGPoint=ff}')])
            CGWarpMouseCursorPosition((float(x), float(y)))
        elif sys.platform == 'win32':
            windll.user32.SetCursorPos(x, y)
        else:
            X = XTest()
            X.fakeMotionEvent(x, y)

if __name__ == "__main__":
    import random, time
    m = PyMouse()
    print 'move'
    m.move(random.randint(0, 500), random.randint(0, 500))
    time.sleep(5)
    print 'click'
    m.click(400, 500, LEFT)
    time.sleep(5)
    print 'click'
    m.click(random.randint(0, 500), random.randint(0, 500), RIGHT)
    time.sleep(5)
    print 'click'
    m.click(random.randint(0, 500), random.randint(0, 500), MIDDLE)
    time.sleep(5)
    print 'move'
    m.move(random.randint(0, 500), random.randint(0, 500))