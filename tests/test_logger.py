

import super_py as sp
import time



log = sp.logging.Logger("main", files=["main.log"], ts_color="bright_green")
log_combined = sp.logging.Logger("combined", files=["combined.log"], ts_color="bright_orange")


log("hi")


@log_combined.benchmark(with_args=[0], with_kwargs=["a"])
@log.benchmark(with_args=[0, 1], with_kwargs=["three", "four"])
def wait_500ms(one, two, *, three, four):
    time.sleep(one)
    return "done"


print(wait_500ms(11.3, 20, three=30, four=40))
print(wait_500ms(0.01, 20, three=30, four=40))
