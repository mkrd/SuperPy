import time
import logging
import functools
from datetime import datetime

from . import string



class _ColoredLoggingFormatter(logging.Formatter):
	def __init__(self, ts_color: str = None):
		self.ts_color = ts_color
		super().__init__(fmt="$levelno: $msg", datefmt="%Y.%m.%d %H:%M:%S", style="$")


	def format(self, record):
		base = string.colored("[$name]\t$asctime\t", self.ts_color)
		formats = {
			logging.CRITICAL: f"{base}{string.colored('$msg', 'bright_magenta')}",
			logging.ERROR: f"{base}{string.colored('$msg', 'bright_red')}",
			logging.WARNING: f"{base}{string.colored('$msg', 'bright_orange')}",
			logging.INFO: f"{base}{string.colored('$msg', 'bright_white')}",
			logging.DEBUG: f"{base}{string.colored('$msg', 'white')}",
		}
		formatter = logging.Formatter(
			fmt=formats.get(record.levelno, self._fmt),
			datefmt="%Y-%m-%d %H:%M:%S",
			style="$",
		)
		return formatter.format(record)



def make_logger(name: str, ts_color: str = "bright_orange", terminal: bool = True, files=[], level=logging.DEBUG):
	"""
		Create a styled logger with nice formating that writes to
		the terminal and/or a set of files.
	"""
	logger = logging.getLogger(name)
	logger.setLevel(level)
	if terminal:
		console_handler = logging.StreamHandler()
		console_handler.setFormatter(_ColoredLoggingFormatter(ts_color=ts_color))
		logger.addHandler(console_handler)
	for file in files:
		file_handler = logging.FileHandler(file)
		file_handler.setFormatter(_ColoredLoggingFormatter(ts_color=ts_color))
		logger.addHandler(file_handler)
	return logger



class log:
	"""
		decorator for logging.
		filepath: write to file
		with_args: list of indices of args that should apppear in the log
		with_kwargs: list of kwarg names that should appear in the log
	"""
	def __init__(self, filepath=None, with_args=[], with_kwargs=[], color="white"):
		# there is no need to make a class for a decorator if there are no parameters
		self.filepath = filepath
		self.with_args = with_args
		self.with_kwargs = with_kwargs
		self.color = color

	def __call__(self, method):
		# returns the decorator itself, which accepts a function and returns another function
		# wraps ensures that the name and docstring of 'method' is preserved in 'wrapper'
		@functools.wraps(method)
		def wrapper(*args, **kwargs):
			# the wrapper passes all parameters to the function being decorated
			timestamp = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
			t1 = time.time()
			res = method(*args, **kwargs)
			t2 = time.time()

			ms = f"{((t2 - t1) * 1000):.1f}ms"
			if len(ms) < 10:
				ms = (" " * (10 - len(ms))) + ms

			log = f"{timestamp}{ms}    {method.__name__}"
			arglist = [f"{a}" for i, a in enumerate(args) if i in self.with_args]
			kwarglist = [f"{k}={a}" for k, a in kwargs.items() if k in self.with_kwargs]
			log += "(" + ", ".join(arglist + kwarglist) + ")"

			log = string.colored(log, color=self.color)

			if self.filepath is None:
				print(log)
			else:
				with open(self.filepath, "a") as f:
					f.write(f"\n{log}")
			return res
		return wrapper