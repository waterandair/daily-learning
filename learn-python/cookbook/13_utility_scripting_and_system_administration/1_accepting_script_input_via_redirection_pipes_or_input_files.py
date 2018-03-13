#!/usr/bin/python3
# coding utf-8
import fileinput

with fileinput.input() as f_input:
    for line in f_input:
        print(line, end='')

"""
$ ls | ./filein.py          # Prints a directory listing to stdout.
$ ./filein.py /etc/passwd   # Reads /etc/passwd to stdout.
$ ./filein.py < /etc/passwd # Reads /etc/passwd to stdout.
"""