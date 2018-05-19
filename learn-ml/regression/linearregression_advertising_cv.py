#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, Ridge
from sklearn.model_selection import GridSearchCV


if __name__ == "__main__":
    data = pd.read_csv('../data/advertising.csv')
    x = data[['TV', 'Radio', 'Newspaper']]
    # x = data[['TV', 'Radio']]
    y = data['Sales']

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1)
    # model = Lasso()
    model = Ridge()

    alpha = np.logspace(-3, 2, 10)  # 取一个等差数列, 数列中的数作为超参数
    liner_model = GridSearchCV(model, param_grid={'alpha': alpha}, cv=5)  # 训练数据分成5份做交叉验证
    liner_model.fit(x_train, y_train)
    print("超参数:", liner_model.best_params_)

    y_hat = liner_model.predict(np.array(x_test))
    mse = np.average((y_hat - np.array(y_test)) ** 2)
    rmse = np.sqrt(mse)
    print("均方误差", mse, "均方根误差", rmse)
    print("分数", liner_model.score(x_test, y_test))
    print(liner_model.best_score_)

    t = np.arange(len(x_test))
    plt.plot(t, y_test, 'r-', linewidth=2, label='Test')
    plt.plot(t, y_hat, 'g-', linewidth=2, label='Predict')
    plt.legend(loc='upper right')
    plt.grid()
    plt.show()


