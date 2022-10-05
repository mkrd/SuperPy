

from curses.ascii import US
import imp
import super_py as sp
import time


class User:
    def __init__(self, name):
        self.name = name


log = sp.logging.Logger("main", files=["main.log"], ts_color="bright_green")
log_combined = sp.logging.Logger("combined", files=["combined.log"], ts_color="bright_orange")


user = User("John Doe")


@log.benchmark(with_args=[0, 1], with_kwargs=["three", "four"], extra_info=[lambda: user.name, lambda: time.time()])
def wait_500ms(one, two, *, three, four):
    time.sleep(one)
    return "done"


print(wait_500ms(1.3, 20, three=30, four=40))
user.name = "Jane Doe"
print(wait_500ms(0.01, 20, three=30, four=40))
