# -*- coding: UTF-8 -*-
import numpy as np
import random as rnd

# Нейроная сеть режима "Комфорт"
# Входные параметры:
# [T, D, G, dt1, p1, dt2, p2, ... dtn, pn]
# T - время суток [0..1]
# D - рабочий/выходной день (0 или 1)
# dti - изменение температуры в i-й комнате [0..1]
# pi - датчик присутствия человека в i-й комнате (0 или 1)

# Функция активации
def f(x):
    return 1.0 / (1.0 + np.exp(-x))

# Функция ошибки
def error(y_train, y_test):
    return np.average(np.power(y_train - y_test, 2))

# Инициализация сети
def init(N):
    W = np.zeros(shape=(2*N, 2*N + 3))
    for i in range(2*N):
        W[i][0] = rnd.random()
        if i % 2 != 0:
            W[i][1] = rnd.random()
        W[i][2] = rnd.random()
    for i in range(3, 2*N, 2):
        W[i - 3][i] = rnd.random()
        W[i - 2][i] = rnd.random()
        W[i - 4][i + 1] = rnd.random()
        W[i - 3][i + 1] = rnd.random()
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
