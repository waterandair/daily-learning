#!/usr/bin/python3
# coding utf-8
import gzip
import io
import glob
from concurrent import futures
"""
The concurrent.futures library provides a ProcessPoolExecutor class that can be used to execute computationally
intensive functions in a separately running instance of the Python interpreter.
However, in order to use it, you first need to have some computationally intensive work
"""


def find_robots(filename):
    """
    find all of the hosts that access robots.txt
    :param filename:
    :return:
    """
    robots = set()
    with gzip.open(filename) as f:
        for line in io.TextIOWrapper(f, encoding='utf-8'):
            fields = line.split()
            if fields[6] == '/robots.txt':
                robots.add(fields[0])
    return robots


def find_all_robots(logdir):
    """
    find all hosts across and entire sequence of files
    :param logdir:
    :return:
    """
    files = glob.glob(logdir + '/*.log.gz')
    all_robots = set()
    for robots in map(find_robots, files):
        all_robots.update(robots)
    return all_robots


"""
Now, suppose you want to modify this program to use multiple CPUs.
"""


def find_robots2(filename):
    robots = set()
    with gzip.open(filename) as f:
        for line in io.TextIOWrapper(f, encoding='utf-8'):
            fields = line.split()
            if fields[6] == '/robots.txt':
                robots.add(fields[0])
    return robots


def find_all_robots2(logdir):
    files = glob.glob(logdir + '/*.log.gz')
    all_robots = set()
    with futures.ProcessPoolExecutor() as pool:
        for robots in pool.map(find_robots2, files):
            all_robots.update(robots)
    return all_robots


if __name__ == '__main__':
    robots = find_all_robots2('test')
    for ip in robots:
        print(ip)

"""
with this modification, the script produces the same result but runs about 3_num_date_time.5 times faster on quad-core machine.
The actual performance will vary according to the number of CPUs available on your machine.
"""



