import sys

if sys.platform == 'darwin':
    import objc
elif sys.platform == 'win32':
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
    try:
        from xtest import XTest
    except ImportError:
        print "Your system is not supported, make sure you have XTest enabled"
    
class PyMouse(object):
    
    def click(self, x, y, button):
        if sys.platform == 'darwin':
            bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
            objc.loadBundleFunctions(bndl, globals(), [('CGPostMouseEvent', 'v{CGPoint=ff}III')])
            CGPostMouseEvent((x, y), 1, button, 1)
            CGPostMouseEvent((x, y), 1, button, 0)
        elif sys.platform == 'win32':
            windll.user32.SetCursorPos(x, y)
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
            CGWarpMouseCursorPosition((x, y))
        elif sys.platform == 'win32':
            windll.user32.SetCursorPos(x, y)
        else:
            X = XTest()
            X.fakeMotionEvent(x, y)

if __name__ == "__main__":
    import random, time
    m = PyMouse()
    m.clickMouse(random.randint(0, 500), random.randint(0, 500), 1)
    time.sleep(5)
    m.clickMouse(random.randint(0, 500), random.randint(0, 500), 2)
    time.sleep(5)
    m.clickMouse(random.randint(0, 500), random.randint(0, 500), 2)
    time.sleep(5)
    m.moveMouse(random.randint(0, 500), random.randint(0, 500))