# -*- coding: iso-8859-1 -*-

#   Copyright 2010 Pepijn de Vos
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""The goal of PyMouse is to have a cross-platform way to control the mouse.
PyMouse should work on Windows, Mac and any Unix that has xlib.

See http://github.com/pepijndevos/PyMouse for more information.
"""

import sys

if sys.platform.startswith('java'):
    from pymouse.java_ import PyMouse

elif sys.platform == 'darwin':
    from pymouse.mac import PyMouse
    try:
        from pymouse.events.mac import PyMouseEvent
    except ImportError:
        from pymouse.base import PyMouseEventMeta as PyMouseEvent

elif sys.platform == 'win32':
    from pymouse.windows import PyMouse
    try:
        from pymouse.events.windows import PyMouseEvent
    except ImportError:
        from pymouse.base import PyMouseEventMeta as PyMouseEvent

else:
    from pymouse.unix import PyMouse
    try:
        from pymouse.events.unix import PyMouseEvent
    except ImportError:
        from pymouse.base import PyMouseEventMeta as PyMouseEvent
