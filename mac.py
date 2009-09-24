# -*- coding: iso-8859-1 -*-
import objc

class PyMouse(object):

	def click(self, x, y, button = 0):
		bndl = objc.loadBundle('CoreGraphics', globals(), \
								'/System/Library/Frameworks/ApplicationServices.framework')
		objc.loadBundleFunctions(bndl, globals(), [('CGPostMouseEvent', \
								'v{CGPoint=ff}IIIII')])
		button_list = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
		CGPostMouseEvent((float(x), float(y)), 1, 3, *button_list[button])
		CGPostMouseEvent((float(x), float(y)), 1, 3, 0, 0, 0)

	def move(self, x, y):
		bndl = objc.loadBundle('CoreGraphics', globals(), '/System/Library/Frameworks/ApplicationServices.framework')
		objc.loadBundleFunctions(bndl, globals(), [('CGWarpMouseCursorPosition', 'v{CGPoint=ff}')])
		CGWarpMouseCursorPosition((float(x), float(y)))

	def whereis(self):
		raise NotImplementedError

	def screen_size(self):
		raise NotImplementedError