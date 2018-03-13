#!/usr/bin/python3
# coding utf-8
from queue import Queue
from threading import Thread, Event
"""
The "actor model" is one of the oldest and most simple approaches to concurrency and distributed computing. In fact, it's
underlying simplicity is part of its appeal.
Actors are straightforward to define using a combination of a thread and a queue
"""
# sentinel used for shutdown
class ActorExit(Exception):
    pass


class Actor:
    def __init__(self):
        self._mailbox = Queue()

    def send(self, msg):
        # send a message to the actor
        self._mailbox.put(msg)

    def recv(self):
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()

    def close(self):
        self.send(ActorExit)

    def start(self):
        # start concurrent execution
        self._terminated = Event()
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._terminated.set()

    def join(self):
        self._terminated.wait()

    def run(self):
        while True:
            msg = self.recv()


# sample actorTack
class PringActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print('got:', msg)


# sample use
p = PringActor()
p.start()
p.send('Hello')
p.send('World')
p.close()
p.join()