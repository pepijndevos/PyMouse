# coding=utf8
#   Copyright 2014 Christopher H. Casebeer
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

'''
Tests that import time for pymouse is not unreasonably long. 

This catches the slow-import-of-Quartz on Mac OS X due to pyobjc's slow 
behavior when import via from ... import *. 
'''

import contextlib
import time

from nose import SkipTest

@contextlib.contextmanager
def check_execution_time(description, max_seconds):
	start_time = time.time()
	yield
	end_time = time.time()
	execution_time = end_time - start_time
	if execution_time > max_seconds:
		raise Exception("Took too long to complete %s" % description)

def test_pymouse_import_time():
	# skip this test by default – call nosetests with --no-skip to enable
	raise SkipTest()
	with check_execution_time("importing pymouse", max_seconds=3):
		import pymouse

