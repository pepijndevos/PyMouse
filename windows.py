# -*- coding: iso-8859-1 -*-

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

class PyMouse(object):

	def click(self, x, y, button = 0):
		windll.user32.SetCursorPos(x, y)
		blob[0].ii.mi.dwFlags = clicks[button]
		blob[1].ii.mi.dwFlags = releases[button]
		windll.user32.SendInput(2,pointer(blob),sizeof(blob[0]))

	def move(self, x, y):
		windll.user32.SetCursorPos(x, y)
	
	def whereis(self):
		raise NotImplementedError

	def screen_size(self):
		#untested
		width = GetSystemMetrics(0)
		height = GetSystemMetrics(1)