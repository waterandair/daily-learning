#!/usr/bin/python
# -*- coding utf-8 -*-

"""
Your program received a directory listing, but when id tried to print the filenames, it crashed with a
UnicodeEncodeError exception and a cryptic message about "surrogates" not allowed.
"""

"""
When printing filenames of unknown origin, use this convention to avoid errors:
"""
def bad_filename(filename):
    return repr(filename)[1:-1]


# for name in files:
#     try:
#             print(name)
#     except UnicodeEncodeError:
#             print(bad_filename(name))


"""
This recipe will likely be ignored by most readers.However, if you're writing mission-critical scripts that
need to work reliably with filenames and filesystem, it's something to think about.
Otherwise, you might find yourself called back into the office over the weekend to debug a seemingly 
inscrutable error.
"""