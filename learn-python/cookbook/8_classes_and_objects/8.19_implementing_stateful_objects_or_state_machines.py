#!/usr/bin/python3
# -*- coding utf-8 -*-

"""
In certain applications, you might have objects that operate differently according to some kind of internal state.
"""
class Connection:
    def __init__(self):
        self.state = 'closed'

    def read(self):
        if self.state != 'open':
            raise RuntimeError('not open')
        print('reading')

    def write(self, data):
        if self.state != 'open':
            raise RuntimeError('not open')
        print('writing')

    def open(self):
        if self.state == 'open':
            raise RuntimeError('already open')
        self.state = 'open'

    def close(self):
        if self.state == 'closed':
            raise RuntimeError('already closed')
        self.state = 'closed'


"""
A more elegant approach is to encode each operational state as a separate class and arrange for the Connection class to 
delegate to the state class
"""
class Connection1:
    """为每个状态定义一个类"""

    def __init__(self):
        self.new_state(ClosedConnectionState)

    def new_state(self, newstate):
        self._state = newstate
        # Delegate to the state class

    def read(self):
        return self._state.read(self)

    def write(self, data):
        return self._state.write(self, data)

    def open(self):
        return self._state.open(self)

    def close(self):
        return self._state.close(self)


class ConnectionState:
    @staticmethod
    def read(conn):
        raise NotImplementedError()

    @staticmethod
    def write(conn, data):
        raise NotImplementedError()

    @staticmethod
    def open(conn):
        raise NotImplementedError()

    @staticmethod
    def close(conn):
        raise NotImplementedError()


# Implementation of different states
class ClosedConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        raise RuntimeError('Not open')

    @staticmethod
    def write(conn, data):
        raise RuntimeError('Not open')

    @staticmethod
    def open(conn):
        conn.new_state(OpenConnectionState)

    @staticmethod
    def close(conn):
        raise RuntimeError('Already closed')


class OpenConnectionState(ConnectionState):
    @staticmethod
    def read(conn):
        print('reading')

    @staticmethod
    def write(conn, data):
        print('writing')

    @staticmethod
    def open(conn):
        raise RuntimeError('Already open')

    @staticmethod
    def close(conn):
        conn.new_state(ClosedConnectionState)
