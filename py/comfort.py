# -*- coding: UTF-8 -*-
import numpy as np
import random as rnd

# Функция активации
def f(x):
    return 1.0 / (1.0 + np.exp(-x))

# Функция ошибки
def error(y_train, y_test):
    return np.average(np.power(y_train - y_test, 2))

# Инициализация сети
def init(N):
    W = np.zeros(shape=(2*N, 2*N + 1))
    for i in range(2*N):
        W[i][0] = rnd.random()
    for i in range(1, 2*N, 2):
        W[i - 1][i] = rnd.random()
        W[i][i] = rnd.random()
        W[i - 1][i + 1] = rnd.random()
        W[i][i + 1] = rnd.random()
    return W

# Одна итерация обучения
def learn_iter(x, y, net):
    y_act = calc(x, net)
    u = net.dot(x)
    dW = (2 * np.average(y_act - y) * np.power(f(u), 2) * np.exp(-u) * (np.ones(net.shape) * x).T).T
    dW *= (net != 0) + np.zeros(net.shape)
    return dW

# Одна эпоха обучения (день)
def learn_epoch(X, Y, net):
    dW = np.zeros(net.shape)
    for i in range(len(X)):
        dW += learn_iter(X[i], Y[i], net)
    dW /= len(X)
    return net - dW

# Расчёт по нейронной сети
def calc(datapiece, net):
    return f(net.dot(datapiece))
