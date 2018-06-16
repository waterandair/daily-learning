#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as colors
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


def iris_type(s):
    iris = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
    return iris[s]


# 花萼长度、花萼宽度，花瓣长度，花瓣宽度
# iris_feature = 'sepal length', 'sepal width', 'petal length', 'petal width'
iris_feature = '花萼长度', '花萼宽度', '花瓣长度', '花瓣宽度'

if __name__ == '__main__':
    # matplotlib 中文
    mpl.rcParams[u'font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

    path = "../data/iris.data"
    data = np.loadtxt(path, dtype=float, delimiter=",", converters={4: iris_type}, encoding='utf-8')
    x, y = np.split(data, (4, ), axis=1)
    # 为了可视化, 仅使用前两列特征
    x = x[:, :2]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

    model = Pipeline([
        ("ss", StandardScaler()),
        # min_samples_split ：如果该结点包含的样本数目大于10，则(有可能)对其分支
        # min_samples_leaf ：若将某结点分支后，得到的每个子结点样本数目都大于10，则完成分支；否则，不进行分支
        ("DTC", DecisionTreeClassifier(criterion="entropy", max_depth=3)),  # 计算信息增益, 树的最大深度3
    ])
    model = model.fit(x_train, y_train)
    # 预测测试数据
    y_test_hat = model.predict(x_test)

    # 以 dot 格式输出决策树
    f = open('iris_tree.dot', 'w')
    tree.export_graphviz(model.get_params('DTC')['DTC'], out_file=f)

    # # 画图
    # N, M = 100, 100  # 横纵各 100 个采样
    # x1_min, x1_max = x[:, 0].min(), x[:, 0].max()  # 第 0 列的范围
    # x2_min, x2_max = x[:, 1].min(), x[:, 1].max()  # 第 1 列的范围
    # t1 = np.linspace(x1_min, x1_max, N)
    # t2 = np.linspace(x2_min, x2_max, M)
    # x1, x2 = np.meshgrid(t1, t2)  # 生成网格采样点
    #
    # x_show = np.stack((x1.flat, x2.flat), axis=1)  # 测试点
    # y_show_hat = model.predict(x_show).reshape(x1.shape)  # 预测值
    #
    # cm_light = colors.ListedColormap(['#77E0A0', '#FF8080', '#A0A0FF'])
    # cm_dark = colors.ListedColormap(['g', 'r', 'b'])
    # plt.pcolormesh(x1, x2, y_show_hat, cmap=cm_light)  # 画出预的结果的范围
    # plt.scatter(x_test[:, 0], x_test[:, 1], c=y_test.ravel(), edgecolors='k', s=20, cmap=cm_dark)  # 画出样本点
    # plt.xlabel(iris_feature[0], fontsize=15)
    # plt.ylabel(iris_feature[1], fontsize=15)
    # plt.xlim(x1_min, x1_max)
    # plt.ylim(x2_min, x2_max)
    # plt.grid(True)
    # plt.title(u'鸢尾花数据的决策树分类', fontsize=17)
    # plt.show()

    # 计算准确度
    y_test = y_test.reshape(-1)
    result = (y_test_hat == y_test)
    acc = np.mean(result)
    print("准确度: {}%".format(acc * 100))

    # 使用不同的树的深度限制生成决策树,选择效果最好的那个
    depth = np.arange(1, 15)
    err_list = []  # 错误率
    for d in depth:
        clf = DecisionTreeClassifier(criterion='entropy', max_depth=d)
        clf = clf.fit(x_train, y_train)
        y_test_hat = clf.predict(x_test)
        res = (y_test_hat == y_test)
        err = 1 - np.mean(res)
        err_list.append(err)
        print("深度: {} 错误率: {}%".format(d, err * 100))

    plt.figure(facecolor='w')
    plt.plot(depth, err_list, 'ro-', lw=2)
    plt.xlabel(u'决策树深度', fontsize=15)
    plt.ylabel(u'错误率', fontsize=15)
    plt.title(u'决策树深度与过拟合', fontsize=17)
    plt.grid(True)
    plt.show()





























