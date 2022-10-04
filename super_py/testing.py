import traceback
import time
from typing import Type

from . import string



class test:
	"""
		A decorator that runs tests automatically when running a file.
		Provide a setup function, and it will run before the test.
		Provide a teardown function, and it will run after the test,
		even if an exception occurs.
	"""
	def __init__(self, setup: callable = lambda: None, teardown: callable = lambda: None, raise_assertion_errors: bool = False):
		self.setup = setup
		self.teardown = teardown
		self.raise_assertion_errors = raise_assertion_errors


	def __call__(self, method):
		self.setup()
		try:
			t1 = time.time()
			method()
			t2 = time.time()
			ms = f"{((t2 - t1) * 1000):.1f}ms"
			print(string.colored(f"Test {method.__name__}() finished in {ms}", "bright_green"))
		except AssertionError:
			print(string.colored(f"Test {method.__name__}() failed!", "bright_red"))
			print(string.colored(traceback.format_exc(), "bright_red"))
			if self.raise_assertion_errors:
				raise
		except BaseException:
			raise
		finally:
			self.teardown()



class test_class:
	"""
		A decorator that runs all tests of a class automatically whose function names
		start with "test_".
		The class_setup runs before all tests, and the class_teardown runs after all tests.
		each_setup and each_teardown runs before and after each test.
	"""
	def __init__(self, class_setup: callable = lambda: None, class_teardown: callable = lambda: None, each_setup: callable = lambda: None, each_teardown: callable = lambda: None):
		self.class_setup = class_setup
		self.class_teardown = class_teardown
		self.each_setup = each_setup
		self.each_teardown = each_teardown


	def do_test(self, method):
		self.each_setup()
		try:
			t1 = time.time()
			method()
			t2 = time.time()
			ms = f"{((t2 - t1) * 1000):.1f}ms"
			print("--> " + string.colored(f"Test {method.__name__}() finished in {ms}", "bright_green"))
		except AssertionError:
			print("--> " + string.colored(f"Test {method.__name__}() failed!", "bright_red"))
			print(string.colored(traceback.format_exc(), "bright_red"))
		except BaseException:
			self.class_teardown()
			raise
		finally:
			self.each_teardown()


	def __call__(self, method):
		print(f"Run test class {method.__name__}:")
		self.class_setup()
		obj = method()
		for test_method_name in [m for m in dir(obj) if m.startswith("test_")]:
			self.do_test(getattr(obj, test_method_name))
		self.class_teardown()



class test_must_except():
	"""
		Use a with statement to run a block of code that must raise an exception.
		The exception must be of the specified type.9

	"""

	def __init__(self, exception_type: Type[Exception]):
		self.exception_type = exception_type

	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_value, traceback):
		if not exc_type:
			raise TypeError(f"Expected an exception of type {self.exception_type}")
		if not issubclass(exc_type, self.exception_type):
			raise TypeError(f"Expected an exception of type {self.exception_type}, got {exc_type}")
		# Return True to surpress the exception
		return True
