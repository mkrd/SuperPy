from time import sleep, time
import super_py as sp
import os
import sys

logger = sp.make_logger("basic_logger", ts_color="bright_orange",)



# @sp.test()
@sp.log(color="bright_magenta")
def test_concurrency():
    def compute():
        i = 1
        for j in range(1, 10000):
            i *= j
        return i
    results = sp.concurrency.run_threaded([
        (compute, ()) for _ in range(100)
    ])
    print(f"Results returned: {len(results)}")



# @sp.test()
def test_dis_write_read_speed():
    logger.debug("Hi I am a log")
    sp.disk.test_write_read_speed(1000_000, 100)


@sp.test()
def test_crashing_thread():
    def waiter(x):
        sleep(0.1)
        return True

    def crasher(x):
        sleep(1)
        d = 7 / 0
        return True

    try:
        r = sp.concurrency.run_threaded([
            (waiter, (0,)),
            (waiter, (1,)),
            (crasher, (0,)),
        ])
        print(f"{r=}")
    except ZeroDivisionError:
        assert True




@sp.test()
def test_if_concurrent():
    def waiter(x):
        sleep(x)
        return True

    t1 = time()

    results = sp.concurrency.run_threaded([
        (waiter, (1,)),
        (waiter, (1,)),
        (waiter, (1,)),
    ])

    t2 = time()

    assert results == [True, True, True]
    assert t2 - t1 < 1.1
