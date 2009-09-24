# -*- coding: iso-8859-1 -*-
import sys

if sys.platform == 'darwin':
	from mac import PyMouse

if sys.platform == 'win32':
	from windows import PyMouse

if sys.platform != 'win32' and sys.platform != 'darwin':
	from unix import PyMouse