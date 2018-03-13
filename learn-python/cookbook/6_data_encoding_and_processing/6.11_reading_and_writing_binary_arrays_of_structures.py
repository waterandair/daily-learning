#!/usr/bin/python3
# *-* coding utf-8 *-*
from struct import Struct
"""
You want to read or write data encoded as a binary array of uniform structures into python tuples
To work with binary data, use the strut module. Here is an example of code that writes a list of python tuple out to a 
binary file, encoding each tuple as a structure using struct
"""
def write_records(records, format, f):
    """
    Write a sequence of tuples to a binary file of structures
    """
    record_struct = Struct(format)
    for r in records:
        f.write(record_struct.pack(*r))

"""
There are several approaches for reading this file back into a list of tuples.
First, if you're going to read the file incrementally in chunks,you can write code such as this:
"""
def read_records(format, f):
    record_struct = Struct(format)
    chunks = iter(lambda : f.read(record_struct.size), b'')
    return (record_struct.unpack(chunk) for chunk in chunks)


if __name__ == '__main__':
    records = [
        (1, 2.3, 4.5),
        (6, 7.8, 9.0),
        (12, 13.4, 56.7)
    ]

    with open('./test/data.b', 'wb') as f:
        write_records(records, '<idd', f)


    with open('./test/data.b', 'rb') as f:
        for rec in read_records('<idd', f):
            print (rec)

        """
        (1, 2.3, 4.5)
        (6, 7.8, 9.0)
        (12_concurrency, 13.4, 56.7)
        """