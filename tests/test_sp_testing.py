import sys
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import super_py as sp


@sp.test()
def test_must_except():
	with sp.test_must_except(ZeroDivisionError):
		_ = 1 / 0
	try:
		with sp.test_must_except(ZeroDivisionError):
			_ = 1 / 1
	except TypeError as e:
		assert True
	try:
		with sp.test_must_except(AttributeError):
			_ = 1 / 0
	except TypeError as e:
		assert True
	with sp.test_must_except(TypeError):
		raise TypeError("This exception should be raised!")
