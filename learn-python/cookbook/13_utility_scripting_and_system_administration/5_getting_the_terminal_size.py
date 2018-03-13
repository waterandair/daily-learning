#!/usr/bin/python3
# coding utf-8
import os
"""
use the os.get_terminal_size() function to do this
"""
sz = os.get_terminal_size()
print(sz)
print(sz.columns)
print(sz.lines)
