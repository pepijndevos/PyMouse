# -*- coding: iso-8859-1 -*-

from Xlib.display import Display
from Xlib import X
from Xlib.protocol import event
import Xlib.ext.xtest

class PyMouse(object):

	def click(self, x, y, button = 0):
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
		display = Display(':0')
		display.screen().root.warp_pointer(x, y)
		display.sync()

	def whereis(self):
		display = display.Display()
		coord = display.screen().root.query_pointer()._data
		return coord["root_x"], coord["root_y"]

	def screen_size(self):
		display = display.Display()
		width = display.screen().width_in_pixels
		height = display.screen().height_in_pixels
		return (width, height)
