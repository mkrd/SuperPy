def _colored_by_color_code(text: str, color_code: int, bold: bool = False, underline: bool = False):
	"""
		Returns an ANSI colored string by its color code,
		and can also be bold and underlined.
	"""
	options = "\033["
	if bold:
		options += "1;"
	if underline:
		options += "4;"
	options += f"{color_code}m"
	return f"{options}{text}\033[0m"



def colored(text: str, color: str, bold: bool = False, underline: bool = False):
	"""
		Returns an ANSI colored string which can be bold and underlined.
		Allowed colors are: black, red, green, orange, blue, magenta,
		cyan, white, bright_black, bright_red, bright_green, bright_orange,
		bright_blue, bright_magenta, bright_cyan, bright_white.
	"""
	colors = {
		"black": 30,
		"red": 31,
		"green": 32,
		"orange": 33,
		"blue": 34,
		"magenta": 35,
		"cyan": 36,
		"white": 37,
		"bright_black": 90,
		"bright_red": 91,
		"bright_green": 92,
		"bright_orange": 93,
		"bright_blue": 94,
		"bright_magenta": 95,
		"bright_cyan": 96,
		"bright_white": 97,
	}
	if color not in colors:
		raise Exception(f"Color {color} does not exist")
	return _colored_by_color_code(text, colors[color], bold=bold, underline=underline)