import super_py as sp


logger = sp.make_logger("basic_logger", ts_color="bright_orange",)



@sp.test()
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



@sp.test()
def test_dis_write_read_speed():
    logger.debug("Hi I am a log")
    sp.disk.test_write_read_speed(1000_000, 100)