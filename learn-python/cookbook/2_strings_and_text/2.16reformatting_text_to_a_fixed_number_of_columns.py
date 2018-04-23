#!/usr/bin/python3
# -*- coding utf-8 -*-
import textwrap
import os
s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."
res = textwrap.fill(s, 70)
print(res)
"""
Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
not around the eyes, don't look around the eyes, look into my eyes,
you're under.
"""

res = textwrap.fill(s, 40)
print(res)
"""
Look into my eyes, look into my eyes,
the eyes, the eyes, the eyes, not around
the eyes, don't look around the eyes,
look into my eyes, you're under.
"""

res = textwrap.fill(s, 40, initial_indent='    ')
print(res)
"""
    Look into my eyes, look into my
eyes, the eyes, the eyes, the eyes, not
around the eyes, don't look around the
eyes, look into my eyes, you're under.

"""

res = textwrap.fill(s, 40, subsequent_indent='    ')
print(res)
"""
Look into my eyes, look into my eyes,
    the eyes, the eyes, the eyes, not
    around the eyes, don't look around
    the eyes, look into my eyes, you're
    under.
"""

# output terminal size
terminal_size = os.get_terminal_size().columns
print(terminal_size)