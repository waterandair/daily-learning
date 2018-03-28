#!/usr/bin/python3
# -*- coding utf-8 -*-
import random

values = [1, 2, 3, 4, 5, 6]

# To pick a random item out of a sequence,use random.choice()
res = random.choice(values)
print(res)

# To take a sampling of N items where selected items are removed from further consideration,use random.sample() instead
res = random.sample(values, 3)
print(res)  # [1, 6, 2]

# If you simply want to shuffle items in a sequence in place, use random.shuffle()
random.shuffle(values)
print(values)  # [1, 4, 5, 3_num_date_time, 6, 2]

# To produce random integers, use random.randint()
res = random.randint(0, 10)
print(res)  # 5

# To produce uniform floating-point values in the range 0 to 1,use random.random()
res = random.random()
print(res)  # 0.9819791062813928

# To get N random-bits expressed as an integer, use random.getrandbits()
res = random.getrandbits(200)
print(res)  # 220628937829388690707480905399016097134142892270092939591153

# You can alter the initial seed by using the random.seed() function
random.seed()  # seed based on system time or os.urandom()
random.seed(12345)  # seed based on integer given
random.seed(b'bytedata')  # seed based on byte data


"""
Functions in random() should not be used in programs related to cryptography.
If you need such functionality, consider using functions in the ssl module instead.
ssl.RAND_bytes() can be used to generate a cryptographically secure sequence of random bytes
"""