#!/usr/bin/python3
# *-* coding utf-8 *-*
import base64
"""
You need to decode or encode binary data using Base64
The base64 module has two functions b64encode() and b64decode(), that do exactly what you want
"""
# some byte data
s = b'hello'
# encode as base64
a = base64.b64encode(s)
print (a)  # b'aGVsbG8='
# decode from base64
s = base64.b64decode(a)
print(s)  # b'hello'

"""
Base64 encoding is only meant to be used on byte-oriented data such as byte strings and byte arrays. Moreover, the 
output of the encoding process is always a byte string. If you are mixing Base64-encoded data with Unicode text, you may
have to perform an extra decoding step;
When decoding Base64, both byte strings and Unicode text strings can be supplied. However, Unicode strings can only 
contain ASCII characters
"""
a = base64.b64encode(s).decode('ascii')
print (a)  # aGVsbG8=