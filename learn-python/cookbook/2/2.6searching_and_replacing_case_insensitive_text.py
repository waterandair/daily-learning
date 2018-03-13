#!/usr/bin/python3
# -*- coding utf-8 -*-
import re

text = 'UPPER PYTHON, lower python, Mixed Python'
res = re.findall('python', text, flags=re.IGNORECASE)
print(res)  # ['PYTHON', 'python', 'Python']

res = re.sub('python', 'snake', text, flags=re.IGNORECASE)
print(res)  # UPPER snake, lower snake, Mixed snake

# The last example reveals a limitation that replacing text won't match the case of the matched text.
# If you need to fix this, you might have to use a support function, as in the following
def matchcase(word):
    def replace(m):
        """
        :param m: argument only can be a match object
        """
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace


res = re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)
print(res)  # UPPER SNAKE, lower snake, Mixed Snake
