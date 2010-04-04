from pymouse import PyMouse
import random, time
try:
    from pymouse import PyMouseEvent

    class event(PyMouseEvent):
        def move(self, x, y):
            print "Mouse moved to", x, y

        def click(self, x, y, button, press):
            if press:
                print "Mouse pressed at", x, y, "with button", button
            else:
                print "Mouse released at", x, y, "with button", button

    e = event()
    e.start()

except ImportError:
    print "Mouse events are not yet supported on your platform"

m = PyMouse()
try:
	size = m.screen_size()
	print "size: %s" % (str(size))

	pos = (random.randint(0, size[0]), random.randint(0, size[1]))
except:
	pos = (random.randint(0, 250), random.randint(0, 250))

print "Position: %s" % (str(pos))

m.move(pos[0], pos[1])

time.sleep(2)

m.click(pos[0], pos[1], 1)

time.sleep(2)

m.click(pos[0], pos[1], 2)

time.sleep(2)

m.click(pos[0], pos[1], 3)

try:
    e.stop()
except:
    pass
