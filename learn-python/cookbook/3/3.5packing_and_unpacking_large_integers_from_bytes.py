#!/usr/bin/python3
# -*- coding utf-8 -*-

# Suppose your program needs to work with a 16-element byte string that holds a 128-bit integer value.
data = b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'

# To interpret the bytes as an integer,use int.from_bytes(),and specify the byte ordering like this
print(len(data))  # 16
print(int.from_bytes(data, 'little'))  # 69120565665751139577663547927094891008
print(int.from_bytes(data, 'big'))     # 94522842520747284487117727783387188

# To convert a large integer value back into a byte string, use the int.to_bytes() method, specifying the number of
# bytes and the byte order

x = 94522842520747284487117727783387188
print(x.to_bytes(16, 'big'))     # b'\x00\x124V\x00x\x90\xab\x00\xcd\xef\x01\x00#\x004'
print(x.to_bytes(16, 'little'))  # b'4\x00#\x00\x01\xef\xcd\x00\xab\x90x\x00V4\x12\x00'