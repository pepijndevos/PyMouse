from pymouse import PyMouse
import random, time

m = PyMouse()
try:
	size = m.screen_size()
	print "size: %s" % (str(size))

	pos = (random.randint(0, size[0]), random.randint(0, size[1]))
except:
	pos = (random.randint(0, 250), random.randint(0, 250))

print "Position: %s" % (str(pos))

print 'move'
m.move(pos[0], pos[1])

time.sleep(2)

print 'click left'
m.click(pos[0], pos[1], 1)

time.sleep(2)

print 'click middle'
m.click(pos[0], pos[1], 2)

time.sleep(2)

print 'click right'
m.click(pos[0], pos[1], 3)
