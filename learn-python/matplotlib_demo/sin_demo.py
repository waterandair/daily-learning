#!/usr/bin/python3
# -*- coding utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False

x = np.arange(-5, 5)
y = np.sin(np.arange(-5, 5))