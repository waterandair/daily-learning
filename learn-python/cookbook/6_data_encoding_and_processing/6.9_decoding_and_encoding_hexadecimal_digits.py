#!/usr/bin/python3
# *-* coding utf-8 *-*
import binascii
import base64
"""
You need to decode a string of hexadecimal digits into a byte string or encode a byte string as hex
use the binascii module
"""
# Initial byte string
s = b'Hello'
# Encode as hex
h = binascii.b2a_hex(s)
print (h)  # b'48656c6c6f'
# Decode back to bytes
b = binascii.a2b_hex(h)
print (b)  # b'Hello'

# Similar functionality can also be found in the base64 module.
h = base64.b16encode(s)
print(h)  # b'48656C6C6F'
b = base64.b16decode(h)
print (b)  # b'Hello'