#!/usr/bin/python3
# -*- coding utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl

# 设置中文和"-"负号显示问题
mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['axes.unicode_minus'] = False

# 获取 figure 对象
fig = plt.figure(figsize=(8, 6))
#  在 figure 对象上创建 axes 对象
ax1 = fig.add_subplot(2, 2, 1)
ax2 = fig.add_subplot(2, 2, 2)
ax3 = fig.add_subplot(2, 2, 3)
# 在当前 axes 上回执曲线图
plt.plot(np.random.randn(50).cumsum(), 'k--')
# 在 ax1 上绘制柱状图
ax1.hist(np.random.randn(300), bins=20, color='k', alpha=0.3)
# 在 ax2 上绘制散点图
ax2.scatter(np.arange(30), np.arange(30), + 3 * np.random.randn(30))
plt.show()