# -*- coding: UTF-8 -*-
import numpy as np
import random as rnd
from scipy.optimize import minimize

def f(x):
    return 1 / (1 + np.exp(-x))

def layer1Ans(W, x):
    return W.dot(x)

def layer2Ans(V, x):
    return V.dot(x)

# Функция ошибки
def error(y_train, y_test):
    return np.average(np.power(y_train - y_test, 2))

# Инициализация сети
def init(N):
    W = np.zeros(shape=(2*N, 3*N))
    for i in range(N):
        W[2*i, 3*i] = rnd.random()
        W[2*i, 3*i+2] = rnd.random()
        W[2*i+1, 3*i+1] = rnd.random()
        W[2*i+1, 3*i+2] = rnd.random()
    V = np.zeros((2, 2*N+1))
    for i in range(N):
        V[0, 2*i] = rnd.random()
        V[1, 2*i+1] = rnd.random()
    V[1, 2*N] = rnd.random()
    return [W, V]

# Вспомогательная функция для оптимизации. На вход получает массивы крутилок и температур
def g(twisters, temps, net):
    # twisters - массив показаний крутилок вида: [Р1 К1 Р2 К2 ... Рn Кn Г]
    # temps - массив температур вида: [Т1 Т2 ... Тn]
    x = np.zeros((np.array(twisters).size + np.array(temps).size,), dtype=twisters.dtype)
    x[0:-1:3] = twisters[0:-1:2]
    x[1:-1:3] = twisters[1:-1:2]
    x[2:-1:3] = temps
    x[-1] = twisters[-1]
    return calc(x, net).dot([0.5, 0.5])

# Функция оптимизации, возвращает показания крутилок в [0, 1].
# Формат выхода: [Р1 К1 Р2 К2 ... Рn Кn Г]
def optimize(temps, N, net, c_res):
    bounds = np.c_[np.zeros(2*N+1), np.ones(2*N+1)]
    con = {
        'type': 'ineq',
        'fun': lambda x: -np.max(abs(x - c_res)) + 0.04
        }
    res = minimize(g, np.zeros(2*N+1), args=(temps,net,), bounds=bounds, tol=1e-3, constraints=con)
    print res.success
    print res.message
    return res.x

# Одна итерация обучения
def learn_iter(x, y, net):
    ans = calc(x, net) # ans = {a1, a2} - выход сети. a1 - расход газа, a2 - электричества
    u = layer1Ans(net[0], x[:-1]) # u - выход 1 слоя
    p = layer2Ans(net[1], np.append(u, x[-1])) # p - выход 2 слоя
    
    mV = (net[1] != 0) + np.zeros(net[1].shape)
    mW = (net[0] != 0) + np.zeros(net[0].shape)
    # dV
    dV = (np.power(f(p), 2)*np.exp(-p) * (np.ones(net[1].shape)).T).T * np.append(u, x[-1]) * mV
    dV = (2*(ans-y)*dV.T).T
    # dW
    dW = np.sum((np.power(f(p), 2)*np.exp(-p) * net[1].T), axis=1)
    tmp = np.ones(net[0].shape) * x[:-1]
    dW = (dW[:-1] * tmp.T).T * mW
    df = np.zeros(net[0].shape[0])
    df[0::2] = 2*(ans-y)[0]
    df[1::2] = 2*(ans-y)[1]
    dW = (dW.T * df).T
    
    return [dW, dV]

# Одна эпоха обучения (день)
def learn_epoch(x, y, net):
    dW = np.zeros(net[0].shape)
    dV = np.zeros(net[1].shape)
    for i in range(len(x)):
        tmp = learn_iter(x[i], y[i], net)
        dW += tmp[0]
        dV += tmp[1]
    dW /= len(x)
    dV /= len(x)
    return [net[0]-dW, net[1]-dV]

# Расчёт по нейронной сети
def calc(datapiece, net):
    return f(layer2Ans(net[1], np.append(layer1Ans(net[0], datapiece[:-1]), datapiece[-1])))
