#!/usr/bin/python3
# -*- coding utf-8 -*-
import sys
"""
Simply write the byte data to the files underlying buffer
"""
#sys.stdout.write(b'Hello\n')
# Traceback (most recent call last):
#   File "./5.17_writing_bytes_to_a_textfile.py", line 7, in <module>
#     sys.stdout.write(b'Hello\n')
# TypeError: write() argument must be str, not bytes
sys.stdout.buffer.write(b'Hello\n')  # Hello
"""
Similarly, binary data can be read from a text file by reading from its buffer attribute instead
"""


"""
The I/O system is built from layers.Text files are constructed by adding a Unicode encoding/decoding layer
on top of a buffered binary-mode file. The buffer attribute simply points at this underlying file.If you access
it, you'll bypass the text encoding/decoding layer.
"""

"""
The example involving sys.stdout might be viewed as a special case.By default, sys.stdout is always opened
in text mode.However,if you are writing a script that actually needs to dump binary data to standard output,
you can use the technique shown to bypass the text encoding.
"""