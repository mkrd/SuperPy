from concurrent.futures import ThreadPoolExecutor, wait



def run_threaded(fns_args: [(callable, tuple)], max_threads=None):
	"""
		Run a list of tasks concurrently, and return their results as
		a list in the same order. A task is a 2-tuple of the function and an
		n-tuple of the function's n arguments.
		Remember: A 1-tuple needs a trailing comma, eg. (x,)
	"""
	if max_threads is None:
		max_threads = len(fns_args)
	results = []
	with ThreadPoolExecutor(max_threads) as pool:
		for fn, args in fns_args:
			future = pool.submit(fn, *args)
			results.append(future)
	wait(results)
	return [r.result() for r in results]