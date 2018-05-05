#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import time
data_path = os.path.dirname(os.path.realpath(__file__)) + '/data/LogiReg_data.txt'
STOP_ITER = 0  # 根据迭代次数停止迭代
STOP_COST = 1  # 根据损失值的变化停止迭代,如果两次迭代损失值变化很小很小,就停止迭代
STOP_GRAD = 2  # 根据梯度,如果梯度变化很小很小,就停止迭代

# matplotlib 中文
mpl.rcParams[u'font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

def show_plt(data):
    """
    查看数据的散点图
    :param student_data:
    :return:
    """
    admitted = data[student_data['admitted'] == 1]
    not_admitted = data[student_data['admitted'] == 0]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(admitted['iq'], admitted['eq'], s=30, c='b', marker='o', label='admitted')
    ax.scatter(not_admitted['iq'], not_admitted['eq'], s=30, c='r', marker='x', label='not admitted')
    ax.legend()
    ax.set_xlabel('iq')
    ax.set_ylabel('eq')
    plt.show()


def sigmoid(z):
    """
    映射到概率的函数, 可以把一个值映射到从0到1的一个值
    :param z:
    :return:
    """
    return 1 / (1 + np.exp(-z))


def model(X, theta):
    """
    返回预测结果值
    :param X: 样本
    :param theta: 参数
    :return:
    """
    return sigmoid(np.dot(X, theta.T))


def cost(X, y, theta):
    """
    损失函数(代价函数) 根据参数计算损失,损失越小,拟合越好
    :param X: 样本
    :param y: 目标值
    :param theta: 参数
    :return:
    """
    left = np.multiply(-y, np.log(model(X, theta)))
    right = np.multiply(1 - y, np.log(1 - model(X, theta)))
    return np.sum(left - right) / (len(X))


def gradient(X, y, theta):
    """
    计算每个参数的梯度方向
    :param X:
    :param y:
    :param theta:
    :return:
    """
    grad = np.zeros(theta.shape)
    error = (model(X, theta) - y).ravel()
    for j in range(len(theta.ravel())):
        term = np.multiply(error, X[:, j])
        grad[0, j] = np.sum(term) / len(X)

    return grad


def stopCriterion(type, value, threshold):
    """
    设定三种不同的停止策略
    :param type:
    :param value:
    :param threshold:
    :return:
    """
    if type == STOP_ITER:
        return value > threshold
    elif type == STOP_COST:
        return abs(value[-1]-value[-2]) < threshold
    elif type == STOP_GRAD:
        return np.linalg.norm(value) < threshold


def shuffleData(data):
    """
    重组数据
    :param data:
    :return:
    """
    np.random.shuffle(data)
    cols = data.shape[1]
    X = data[:, 0:cols-1]
    y = data[:, cols-1:]
    return X, y


def descent(data, theta, batchSize, stopType, thresh, alpha, n):
    """
    梯度下降求解,计算参数更新
    :param data: 样本数据
    :param theta: 参数
    :param batchSize: 每次迭代计算的样本数量
    :param stopType: 停止策略
    :param thresh: 停止策略对应的阈值
    :param alpha: 学习率
    :param n: 样本总数量
    :return:
    """
    init_time = time.time()
    # 初始化
    i = 0  # 迭代次数
    k = 0  # 每次迭代计算的样本数量
    X, y = shuffleData(data)
    grad = np.zeros(theta.shape)  # 计算的梯度
    costs = [cost(X, y, theta)]  # 损失值

    while True:
        grad = gradient(X[k:k + batchSize], y[k:k + batchSize], theta)
        k += batchSize  # 取batch数量个数据
        if k >= n:
            k = 0
            X, y = shuffleData(data)  # 重新洗牌
        theta = theta - alpha * grad  # 参数更新
        costs.append(cost(X, y, theta))  # 计算新的损失
        i += 1

        if stopType == STOP_ITER:
            value = i
        elif stopType == STOP_COST:
            value = costs
        elif stopType == STOP_GRAD:
            value = grad
        if stopCriterion(stopType, value, thresh):
            break

    return theta, i - 1, costs, grad, time.time() - init_time


def predict(X,theta):
    return [1 if x > 0.5 else 0 for x in model(X, theta)]


def runExpe(data, theta, batchSize, stopType, thresh, alpha, n):
    theta, iter, costs, grad, dur = descent(data, theta, batchSize, stopType, thresh, alpha, n)

    title = "原始数据" if (data[:, 1] > 2).sum() > 1 else "标准化数据"
    if batchSize == n:
        strDescType = "批量梯度下降"
    elif batchSize == 1:
        strDescType = "随机梯度下降"
    else:
        strDescType = "小批量梯度下降 ({})".format(batchSize)

    title += strDescType + " 学习率: {} ".format(alpha)
    title += " 迭代停止策略: "
    if stopType == STOP_ITER:
        strStop = "迭代次数 = {}".format(thresh)
    elif stopType == STOP_COST:
        strStop = "损失变化 < {}".format(thresh)
    else:
        strStop = "梯度变化 < {}".format(thresh)
    title += strStop
    print("***{}\nTheta: {} - Iter: {} - Last cost: {:03.2f} - Duration: {:03.2f}s".format(
        title, theta, iter, costs[-1], dur))

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(np.arange(len(costs)), costs, 'r')
    ax.set_xlabel('迭代次数')
    ax.set_ylabel('损失')
    ax.set_title(title)
    plt.show()
    return theta


if __name__ == '__main__':
    student_data = pd.read_csv(data_path, header=None, names=['iq', 'eq', 'admitted'])
    # show_plt(student_data)
    # 添加一列偏置项系数, 设置为1
    student_data.insert(0, 'ones', 1)
    # 设置样本X和目标值y
    orig_data = student_data.as_matrix()  # 把DataFrame转为矩阵,方便计算
    cols = orig_data.shape[1]
    X = orig_data[:, 0:cols-1]
    y = orig_data[:, cols-1:]
    # 给参数设置一个初始值
    theta = np.zeros([1, 3])

    """
    批量梯度下降
    每次迭代要计算所有样本,速度慢,准确度高
    """
    # 根据迭代次数停止,设置阈值 5000, 迭代5000次
    # res = runExpe(orig_data, theta, 100, STOP_ITER, 5000, 0.000001, 100)
    # 根据损失值停止, 设置阈值 0.0000001, 迭代次数 508960 左右
    # res = runExpe(orig_data, theta, 100, STOP_COST, 0.0000001, 0.001, 100)
    # 根据梯度变化停止, 设置阈值 0.05, 迭代次数
    # res = runExpe(orig_data, theta, 100, STOP_GRAD, 0.05, 0.001, 100)

    """
    随机梯度下降
    每次迭代只计算一个样本,速度快,准确度低,需要调低学习率
    """
    # res = runExpe(orig_data, theta, 1, STOP_ITER, 5000, 0.000001, 100)

    """
    小批量梯度下降
    每次迭代计算一部分样本,兼顾速度和准确度,是常用的方法
    """
    # 根据迭代次数停止,设置阈值 5000, 迭代5000次
    # res = runExpe(orig_data, theta, 15, STOP_ITER, 5000, 0.001, 100)
    # 浮动仍然比较大,可以对数据先进行标准化(按列减去其均值,除以其方差), 这样,对每列来说素有数据都聚集在 0 附近,方差值为 1
    from sklearn import preprocessing as pp
    scaled_data = orig_data.copy()
    scaled_data[:, 1:3] = pp.scale(orig_data[:, 1:3])
    # 标准化数据 根据迭代次数停止
    # res = runExpe(scaled_data, theta, 15, STOP_ITER, 5000, 0.001, 100)
    # 标准化数据 根据损失值停止
    # res = runExpe(scaled_data, theta, 15, STOP_COST, 0.000001, 0.001, 100)
    # 标准化数据 根据梯度变化停止
    res = runExpe(scaled_data, theta, 15, STOP_GRAD, 0.001, 0.001, 100)
    print(res)

    """
    预测
    """
    # 要被预测的数据
    scaled_X = scaled_data[:, :3]
    # 目标值
    y = scaled_data[:, 3]
    # 传入上面梯度下降算法得出的参数
    predictions = predict(scaled_X, res)
    correct = [1 if a == b else 0 for (a, b) in zip(predictions, y)]
    accuracy = (sum(map(int, correct)) % len(correct))
    print('accuracy = {0}%'.format(accuracy))



