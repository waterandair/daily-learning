#!/usr/bin/python3
# -*- coding utf-8 -*-
import serial
"""
You want to read and write data over a serial port, typically to interact with some kind of hardware device
e.g. a robot or sensor

Although you can probably do this directly using Python's built-in I/O primitives, your best bet for serial
communication is to use the Pyserial package
"""

"""
ser = serial.Serial('/dev/tty.usbmodem641',  # Device name varies
                     baudrate=9600,
                     bytesize=8,
                     parity='N',
                     stopbits=1)
"""

