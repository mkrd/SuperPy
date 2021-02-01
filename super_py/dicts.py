def deep_update(base_dict: dict, update_dict: dict):
	"""
		Works like update, but recursively on each level
	"""
	res = base_dict.copy()
	for key, val in update_dict.items():
		c = isinstance(res.get(key), dict) and isinstance(val, dict)
		res[key] = deep_update(res[key], val) if c else val
	return res