import time
import logging
import functools
from logging.handlers import RotatingFileHandler

from . import string


class _ColoredLoggingFormatter(logging.Formatter):
	def __init__(self, ts_color: str = None):
		self.ts_color = ts_color
		super().__init__(fmt="$levelno: $msg", datefmt="%Y.%m.%d %H:%M:%S", style="$")

	def format(self, record):
		base = string.colored("[$name]    $asctime  ", self.ts_color) + "$msg"
		# formats = {
		# 	logging.CRITICAL: f"{base}{string.colored('$msg', 'bright_magenta')}",
		# 	logging.ERROR: f"{base}{string.colored('$msg', 'bright_red')}",
		# 	logging.WARNING: f"{base}{string.colored('$msg', 'bright_orange')}",
		# 	logging.INFO: f"{base}{string.colored('$msg', 'bright_white')}",
		# 	logging.DEBUG: f"{base}{string.colored('$msg', 'white')}",
		# }
		formatter = logging.Formatter(
			fmt=string.colored("[%(name)-12s] %(asctime)s", self.ts_color) + " %(msg)s",
			datefmt="%Y-%m-%d %H:%M:%S",
			style="%",
		)
		return formatter.format(record)



class Logger():
	def __init__(
		self,
		name: str,
		ts_color: str = "bright_orange",
		terminal: bool = True,
		files: list[str] | str | None = None,
	):
		"""
		:param name: Name of the logger
		:param ts_color: Color of the timestamp and logger name in the log
		:param terminal: Whether to log to terminal
		:param files: List of files to log to, or a single file name as a string
		"""
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.DEBUG)
		formatter = _ColoredLoggingFormatter(ts_color=ts_color)

		# Setup terminal logger
		if terminal:
			console_handler = logging.StreamHandler()
			console_handler.setFormatter(formatter)
			self.logger.addHandler(console_handler)

		# Setup file logging
		for file in ([files] if isinstance(files, str) else (files or [])):
			file_handler = logging.FileHandler(file)
			file_handler.setFormatter(formatter)
			self.logger.addHandler(file_handler)


	def __call__(self, message):
		self.logger.debug((" " * 11) + message)


	def benchmark(
		self,
		_func=None,
		*,
		with_args: list[int] = [],
		with_kwargs: list[str] = []
	):
		"""
		A function decorator for the logger that logs the time it takes to execute a function

		Example usage:

			log = Logger("my_logger")

			@log.benchmark
			def my_func():
				...

			@log.benchmark(with_args=[0, 1], with_kwargs=["c", "d"])
			def my_func(a, b, c=None, d=None):
				...

		:param with_args: a list of indices of the arguments to be logged
		:param with_kwargs: a list of keyword arguments to include in the log
		:return: A decorator.
		"""
		# The decorator is called or returned at the end depending on whether
		# self.benchmark is called with () or not.
		def decorator(func):
			@functools.wraps(func)
			# The wrapper receives all args and kwagrs of the decorated function
			def wrapper(*args, **kwargs):

				# Execute and time the decorated function
				t1 = time.time()
				res = func(*args, **kwargs)
				t2 = time.time()

				# Create log message
				ms = f"{(t2 - t1) * 1000:.1f}ms".rjust(9)
				arglist = [f"{a}" for i, a in enumerate(args) if i in with_args]
				kwarglist = [f"{k}={a}" for k, a in kwargs.items() if k in with_kwargs]
				arg_str = ", ".join(arglist + kwarglist)

				self.logger.debug(f"{ms}  {func.__name__}({arg_str})")
				return res
			return wrapper
		return decorator if _func is None else decorator(_func)
