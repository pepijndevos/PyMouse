# -*- coding: iso-8859-1 -*-
import objc

from unix import PyMouse as UnixPyMouse

bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
objc.loadBundleFunctions(bndl, globals(), [('CGPostMouseEvent', 'v{CGPoint=ff}IIIII')])
objc.loadBundleFunctions(bndl, globals(), [('CGWarpMouseCursorPosition', 'v{CGPoint=ff}')])

class PyMouse(UnixPyMouse):
	def press(self, x, y, button = 0):
		button_list = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]
		CGPostMouseEvent((float(x), float(y)), 1, 3, *button_list[button])

	def release(self, x, y, button = 0):
		CGPostMouseEvent((float(x), float(y)), 1, 3, 0, 0, 0)

	def move(self, x, y):
		CGWarpMouseCursorPosition((float(x), float(y)))