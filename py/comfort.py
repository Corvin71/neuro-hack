# -*- coding: UTF-8 -*-
import numpy as np
import random as rnd

# Функция активации
def f(x):
    return 1.0 / (1.0 + np.exp(-x))

# Функция ошибки
def mse(y_actual, y_ideal):
    return [np.power(y_a - y_i, 2) for y_a, y_i in zip(y_actual, y_ideal)] / len(y_actual)

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
    
    return 0.0 # Возврат ошибки

# Одна эпоха обучения (день)
def learn_epoch(X, Y, net):
    return [] # возврат обученной сети

# Расчёт по нейронной сети
def calc(datapiece, net):
    return f(net.dot(datapiece))
