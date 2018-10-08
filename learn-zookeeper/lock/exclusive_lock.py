import sys
import time
from kazoo.client import KazooClient


def work(zk, path, sleep, is_lock, times):
    lock = zk.Lock("/lock", "incr lock")

    if is_lock == "yes":
        with lock:
            _work(zk, path, sleep, times)
    else:
        _work(zk, path, sleep, times)


def _work(zk, path, sleep, times):
    value = int(zk.get(path)[0])
    get_time = time.time()
    time.sleep(sleep)
    zk.set(path, str(value + 1).encode())
    set_time = time.time()
    print("time:{:<20} get:{:<5} time:{:<20} set:{:<5} loop_times:{:<5}"
          .format(get_time, value, set_time, value + 1, times))


if __name__ == '__main__':
    # 为了方便观察而设置的阻塞时间
    sleep = 1 if len(sys.argv) < 2 else int(sys.argv[1])
    # 是否使用锁 "yes"/"no"
    is_lock = "yes" if len(sys.argv) > 2 and sys.argv[2] == "yes" else "no"

    # zookeeper 地址
    hosts = "127.0.0.1:2181,127.0.0.1:2182,127.0.0.1:2183"
    # 在这个节点上做自增操作
    path = "/data"

    # 启动 kazoo
    zk = KazooClient(hosts=hosts)
    zk.start()

    # 初始化数据节点
    exists = zk.exists(path)
    if exists is None:
        zk.create(path, b"0")

    # 执行次数
    times = 0
    while True:
        times += 1
        work(zk, path, sleep, is_lock, times)

        if times > 10 // sleep:
            break

    print("该节点当前的值:", zk.get(path)[0])
    zk.stop()
