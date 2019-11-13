import time


class Stopwatch:

    def __call__(self, param):
        def func_wrapper(func):
            avg_time = 0
            for _ in range(param):
                t0 = time.time()
                func()
                t1 = time.time()
                avg_time += (t1 - t0)
            avg_time /= param
            print("Среднее время выполнения %.5f секунд" % avg_time)

        return func_wrapper


stopwatch = Stopwatch()


@stopwatch(2)
def f():
    for j in range(1000000):
        if j % 100000 == 0:
            print(j)
