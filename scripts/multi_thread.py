import time
from threading import Thread
import datetime

def long_io(cb):
    def func(callback):
        print("开始耗时操作io", datetime.datetime.now())
        time.sleep(1)
        print("io耗时操作完成", datetime.datetime.now())
        res = "io res"
        callback(res)

    print("初始化线程时间戳", datetime.datetime.now())
    t1 = Thread(target=func, args=(cb,))
    t1.start()


def receive_msg(res):
    print("获取结果回调结果")
    print("io 结果:", res)


def req_a():
    print("开始处理请求a---")
    long_io(receive_msg)
    print("离开请求a---")


def req_b():
    print("开始处理请求b---")
    time.sleep(2)
    print("处理完请求b---")


def main():
    req_a()
    req_b()


if __name__ == '__main__':
    main()
