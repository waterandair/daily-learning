#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

if __name__ == '__main__':
    path = "../data/advertising.csv"
    data = pd.read_csv(path)
    x = data[['TV', 'Radio', 'Newspaper']]
    y = data['Sales']

    plt.figure(figsize=(4, 6))
    # 子图, 子图规格, 三位[1, 3]的整数,
    # 第一个数表示共有几个子图,
    # 第二个数表示每行显示几个子图,
    # 第三个数表示现在绘制的是第几个子图
    plt.subplot(311)

    plt.plot(data['TV'], y, 'ro')
    plt.title('TV')
    plt.grid()
    plt.subplot(312)
    plt.plot(data['Radio'], y, 'g^')
    plt.title('Radio')
    plt.grid()
    plt.subplot(313)
    plt.plot(data['Newspaper'], y, 'b*')
    plt.title('Newspaper')
    plt.grid()
    plt.tight_layout()  # 自动调整子图参数
    plt.show()

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=1)
    linearReg = LinearRegression()
    model = linearReg.fit(x_train, y_train)
    print(model)
    print(linearReg.coef_)  # 估计系数
    print(linearReg.intercept_)  # 独立项/截距

    y_hat = linearReg.predict(x_test)
    mse = np.average((y_hat - np.array(y_test)) ** 2)  # 均方误差
    rmse = np.sqrt(mse)  # 均方根误差
    print(mse, rmse)

    t = np.arange(len(x_test))
    plt.plot(t, y_test, 'r-', linewidth=2, label='Test')  # 红色折线图
    plt.plot(t, y_hat, 'g-', linewidth=2, label='Predict')  # 绿色折线图
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()
