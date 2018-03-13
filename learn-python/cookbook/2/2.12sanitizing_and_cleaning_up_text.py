#!/usr/bin/python3
# -*- coding utf-8 -*-
import unicodedata
import sys

s = 'pýtĥöñ\fis\tawesome\r\n'
print(s)
# pýtĥöñ
#       is	awesome

# the first step is to clean up the whitespace.To do  this , make a small translation table and use translate()
remap = {
    ord('\t'): ' ',
    ord('\f'): ' ',
    ord('\r'): None  # deleted
}

a = s.translate(remap)
print(a)  # pýtĥöñ is awesome\n

# you can take this remapping idea a step further and build much bigger tables.
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
print(cmb_chrs)

b = unicodedata.normalize('NFD', a)
print(b)  # pýtĥöñ is awesome

print(b.translate(cmb_chrs))  # python is awesome