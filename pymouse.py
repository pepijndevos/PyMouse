# -*- coding: iso-8859-1 -*-
import sys
from abc import ABCMeta, abstractmethod

class PyMouseMeta:
	__metaclass__ = ABCMeta

	@abstractmethod
	def press(self, x, y, button = 0):
		"""Press the mouse on a givven x, y and button.
		Button is defined as 0 = left, 1 = middle, 2 = right."""
		pass

	@abstractmethod
	def release(self, x, y):
		"""Release all mouse buttons"""
		pass

	def click(self, x, y, button = 0):
		"""Click the mouse on a givven x, y and button.
		Button is defined as 0 = left, 1 = middle, 2 = right."""
		self.press(x, y, button)
		self.release(x, y, button)

	@abstractmethod
	def move(self, x, y):
		"""Move the mouse to a givven x and y"""
		pass

	@abstractmethod
	def position(self):
		"""Get the current mouse position in pixels.
		Returns a tuple of 2 integers"""
		pass

	@abstractmethod
	def screen_size(self):
		"""Get the current screen size in pixels.
		Returns a tuple of 2 integers"""
		pass

if sys.platform == 'darwin':
	from mac import PyMouse

elif sys.platform == 'win32':
	from windows import PyMouse

else:
	from unix import PyMouse
