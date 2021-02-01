# flake8: noqa
from .logging import make_logger, log
from .testing import test, test_class
from . import disk
from . import string
from . import concurrency
from . import dicts

################################################################################
######## How to make decorators ################################################
################################################################################

# # No arguments decorator: @decorator
# def decorator(function):
# 	# wraps ensures that the name and docstring of 'function' is preserved in 'wrapper'
# 	@functools.wraps(function)
# 	def wrapper(*args, **kwargs):
# 		return function(*args, **kwargs)
# 	return wrapper

# # Decorator with arguments: @decorator(arg1, arg2=1)
# class decorator:
# 	def __init__(self, arg1, arg2=1):
# 		# there is no need to make a class for a decorator if there are no parameters
# 		self.arg1 = arg1
# 		self.arg2 = arg2

# 	def __call__(self, function):
# 	# returns the decorator itself, which accepts a function and returns another function
# 	# wraps ensures that the name and docstring of 'function' is preserved in 'wrapper'
# 		@functools.wraps(function)
# 		def wrapper(*args, **kwargs):
# 			return function(*args, **kwargs)
# 		return wrapper
