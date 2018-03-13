#!/usr/bin/python3
# coding utf-8
from socket import AF_INET, SOCK_STREAM, socket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Queue
import urllib.request
"""
The concurrent.futures library has a ThreadPoolExecutor class that can be used for this purpose.
Here is an example of a simple TCP server that uses a thread-pool to serve clients
"""
def echo_client(sock, client_addr):
    """
    handle a client connection
    :param sock:
    :param client_addr:
    :return:
    """

    print('got connection from ', client_addr)
    while True:
        msg = sock.recv(65535)
        if not msg:
            break
        sock.sendall(msg)
    print('client closed connection')
    sock.close()


def echo_server(addr):
    pool = ThreadPoolExecutor(128)
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(10)  # params not useful on linux
    while True:
        client_sock, client_addr = sock.accept()  # block
        pool.submit(echo_client, client_sock, client_addr)


echo_server(('', 15000))


def echo_client2(q):
    """
    handle a client connection
    :param q:
    :return:
    """
    sock, client_addr = q.get()
    print('got connection from ', client_addr)
    while True:
        msg = sock.recv(65535)
        if not msg:
            break
        sock.sendall(msg)
    print('client closed connection')
    sock.close()


def echo_server2(addr, nworkers):
    # launch the client workers
    q = Queue()
    for n in range(nworkers):
        t = Thread(target=echo_client2, args=(q, ))
        t.start()

    # run the server
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(addr)
    sock.listen(5)
    while True:
        client_sock, client_addr = sock.accept()
        q.put((client_sock, client_addr))


echo_server2(('', 15000), 128)


"""
one advantage of using ThreadPoolExecutor over a manual implementation is that it makes it easier for the 
submitter to receive results from the called function.
"""
def fetch_url(url):
    u = urllib.request.urlopen(url)
    data = u.read()
    return data


pool = ThreadPoolExecutor(10)
# submit work to the pool
a = pool.submit(fetch_url, 'http://www.python.org')
b = pool.submit(fetch_url, 'http://www.pypy.org')

# get the result back
x = a.result()
y = b.result()
"""
The result objects in the example handle all of the blocking and coordination needed to get data back from the worker 
thread.
Specifically, the operation a.result() blocks until the corresponding function has been executed by the pool and 
returned a value
"""