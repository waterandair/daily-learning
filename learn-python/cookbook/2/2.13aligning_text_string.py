#!/usr/bin/python3
# -*- coding utf-8 -*-

# For basic alignment of strings, the ljust(), rjust(), and center() methods of strings can be used
text = 'Hello World'
res = text.ljust(20)
print(res)  # ‘Hello World         ’

res = text.rjust(20)
print(res)  # '         Hello World'

res = text.center(20)
print(res)  # '    Hello World     '

res = text.rjust(20, '=')
print(res)  # '=========Hello World'

res = text.center(20, '*')
print(res)  # ****Hello World*****


# the format() function can also be used to easily align things.All you need to do is use the <,>,or ^ characters along
# with a desired width.
res = format(text, '>20')
print(res)  # '         Hello World'

res = format(text, '<20')
print(res)  # 'Hello World         '

# If you want to include a fill character other than a space, specify it before the alignment character
res = format(text, '=>20')
print(res)  # '=========Hello World'

res = format(text, '*^20s')
print(res)  # '****Hello World*****'

# The format codes can also be used in the format() method when formatting multiple values
res = '{:>10s} {:>10s}'.format('hello', 'world')
print(res)  # '     hello      world'

# One benefit of format() is that it is not specific to strings.It works with any value,making it more general purpose
x = 1.2345
res = format(x, '>10')
print(res)  # '    1.2345'

res = format(x, '^10.2f')
print(res)  # '   1.23   '


# In older code, you will also see the % operator used to format text.
res = '%-20s' % text
print(res)  # 'Hello World         '

res = '%20s' % text
print(res)  # '         Hello World'
# However, in new code, you should probably prefer the use of the format() function or method .format is a lot
# more powerful than what is provided with the % operator.Moreover, format() is more general purpose than using the
# ljust(), rjust(), or center() method of strings in that it works with any kind of object
