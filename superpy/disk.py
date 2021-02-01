import os
import time
import random

from superpy import log



def _generate_bytes(size_bytes: int, times: int = 1):
	"""
		Generates a list of {times} random bytes objects,
		each the size of {size_bytes}.
	"""
	return [os.urandom(size_bytes) for _ in range(times)]



def _write_bytes(bytes_to_write_list: list, file_names: list):
	"""
		Write each item of the {bytes_to_write_list} to its own file,
		specified in {file_names}.
		The writing duration is measured, and prined at the end.
	"""
	sec = 0.0
	for file_name, bytes_to_write in zip(file_names, bytes_to_write_list):
		start_time = time.time()
		with open(file_name, "wb") as f:
			f.write(bytes_to_write)
		end_time = time.time()
		sec += end_time - start_time

	mb = (len(bytes_to_write) * len(file_names)) / 1_000_000.0
	print(f"Write {mb:.2f}mb over {len(file_names)} files took {1000 * sec:.1f}ms at {mb / sec:.2f}mb/s")



def _read_bytes(file_names: list):
	"""
		Read each file specified in {file_names}.
		The reading duration is measured, and prined at the end.
	"""
	sec, size = 0.0, 0
	for file_name in file_names:
		start_time = time.time()
		with open(file_name, "rb") as f:
			read_bytes = f.read()
		end_time = time.time()
		sec += end_time - start_time
		size += len(read_bytes)

	mb = size / 1_000_000.0
	print(f"Read {mb:.2f}mb over {len(file_names)} files took {1000 * sec:.1f}ms at {mb / sec:.2f}mb/s")



@log(with_args=[0, 1])
def test_write_read_speed(size_bytes: int, times: int = 1):
	"""
		Generates a list of {times} random bytes objects,
		each the size of {size_bytes}, and then writes and reads them
		sequentially, while printing the results.
	"""
	try:
		os.makedirs(".sp_test_write_read_speed/")
		file_names = [f".sp_test_write_read_speed/{random.randint(0, 99999999999999)}" for _ in range(times)]
		bytes_to_write_list = _generate_bytes(size_bytes, times=times)
		_write_bytes(bytes_to_write_list, file_names)
		_read_bytes(file_names)
	finally:
		for file_name in file_names:
			os.remove(file_name)
		os.rmdir(".sp_test_write_read_speed/")