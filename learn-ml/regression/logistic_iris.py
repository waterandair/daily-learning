#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


def iris_type(s):
    iris = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    return iris[s]


if __name__ == '__main__':
    """
    逻辑回归分类鸢尾花
    """
    path = "../data/iris.data"
    data = np.loadtxt(path, dtype=float, delimiter=",", converters={4: iris_type}, encoding='utf-8')

    # 将数据 0 到 3 的 4 列组成 x, 最后一列组成 y
    x, y = np.split(data, (4,), axis=1)

    # 使用 pipeline 形式组织模型
    lr = Pipeline([
        ('sc', StandardScaler()),  # 对数据进行标准化处理
        ('clf', LogisticRegression())]  # 逻辑回归模型
    )

    lr.fit(x, y.ravel())

    x = x[:, :2]
    # 画图查看结果, 构建一个由250000个点组成的平面
    N, M = 500, 500  # 横纵各采样多少个值
    x1_min, x1_max = x[:, 0].min(), x[:, 0].max()  # 第0列的范围
    x2_min, x2_max = x[:, 1].min(), x[:, 1].max()  # 第1列的范围
    t1 = np.linspace(x1_min, x1_max, N)
    t2 = np.linspace(x2_min, x2_max, M)
    x1, x2 = np.meshgrid(t1, t2)  # 生成网格采样点

    x_test = np.stack((x1.flat, x2.flat), axis=1)  # 250000个测试点

    cm_light = colors.ListedColormap(['#77E0A0', '#FF8080', '#A0A0FF'])
    cm_dark = colors.ListedColormap(['g', 'r', 'b'])
    y_hat = lr.predict(x_test)  # 预测值
    y_hat = y_hat.reshape(x1.shape)  # 使之与输入的形状相同
    plt.pcolormesh(x1, x2, y_hat, cmap=cm_light)  # 预测值的显示
    plt.scatter(x[:, 0], x[:, 1], s=10, c=y.ravel(), cmap=cm_dark)  # 样本点的显示
    plt.xlabel('petal length')
    plt.ylabel('petal width')
    plt.xlim(x1_min, x1_max)  # 设置轴的最大最小值
    plt.ylim(x2_min, x2_max)
    # plt.grid()
    plt.show()

    # 测试训练集上的预测结果
    y_hat = lr.predict(x)
    y = y.reshape(-1)
    result = y_hat == y
    acc = np.mean(result)
    print('准确度: {}'.format(100 * acc))



