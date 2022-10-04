# SuperPy

[![Downloads](https://pepy.tech/badge/super-py)](https://pepy.tech/project/super-py)
[![Downloads](https://pepy.tech/badge/super-py/month)](https://pepy.tech/project/super-py)
[![Downloads](https://pepy.tech/badge/super-py/week)](https://pepy.tech/project/super-py)

There are 5 sub modules:
- sp.logging
- sp.testing
- sp.concurrency
- sp.dicts
- sp.disk
- sp.string


## sp.logging

SuperPy's logging system is a simple abstraction from the standard library logging module.
It also provides some nice extra functionalities.
Here are some examples:

### Logging messages

``` python
import super_py as sp

log = sp.logging.Logger("info",
    ts_color="bright_green",
    terminal=True,
    files=["info.log", "combined.log"],
)

log("This is a simple log!")
```

This will write the following log line to the terminal, and the files `info.log` and `comnined.log`:
```
[info        ] 2022-10-04 15:53:09            This is a simple log!
```
where the name and timestamp will be colored in `bright_green`.

### Logging function benchmarks

You can also use the provided decorator to log benchmarks of your functions:

``` python
import super_py as sp

log = sp.logging.Logger("benchmark",
    ts_color="bright_green",
    terminal=True,
)

@log.benchmark(with_args=[0])
def wait(seconds):
    time.sleep(seconds)

for i in range(10):
    wait(i / 10)
```

This will write the following log lines:
```
[benchmark   ] 2022-10-04 16:03:39     0.0ms  wait((0.0))
[benchmark   ] 2022-10-04 16:03:39   105.1ms  wait((0.1))
[benchmark   ] 2022-10-04 16:03:39   205.1ms  wait((0.2))
[benchmark   ] 2022-10-04 16:03:40   308.3ms  wait((0.3))
[benchmark   ] 2022-10-04 16:03:40   403.5ms  wait((0.4))
[benchmark   ] 2022-10-04 16:03:40   505.1ms  wait((0.5))
[benchmark   ] 2022-10-04 16:03:41   605.1ms  wait((0.6))
[benchmark   ] 2022-10-04 16:03:42   705.1ms  wait((0.7))
[benchmark   ] 2022-10-04 16:03:43   804.1ms  wait((0.8))
[benchmark   ] 2022-10-04 16:03:43   903.3ms  wait((0.9))
```

You can use benchmark without calling the decorator, it will still work:
``` python
@log.benchmark
def wait(seconds):
    time.sleep(seconds)
```

The benchmark decorator takes the following keyword arguments:
- `with_args: list[int]`: The list of indices of function arguments which should be logged.
- `with_kwargs: list[str]`: The list of keyword argument names of the function which should be logged.
