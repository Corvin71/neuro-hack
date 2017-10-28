# -*- coding: UTF-8 -*-
import numpy as np
import random as rnd

def f(x):
    return 1/(1+np.exp(-x))

def layer1Ans(W, x):
    return W.dot(x)

def layer2Ans(V, x):
    return V.dot(x)

# Инициализация сети
def init(N):
    W = np.zeros(shape=(N, 3*N+1))
    for i in range(N):
        for k in range(3):
            W[i, 3*i+k] = rnd.random()
    W[i, 3*(N-1)+3] = rnd.random()
    V = np.random.rand(2,N)
    return [W, V]

# Одна итерация обучения
def learn_iter(x, y, net):
    ans = calc(x, net) # ans = {a1, a2} - выход сети. a1 - расход газа, a2 - электричества
    u = layer1Ans(net[0], x) # u - выход 1 слоя БЕЗ ФУНКЦИИ АКТИВАЦИИ
    # dV
    dV = (2*(ans-y)*(((np.ones(net[1].shape).T * np.power(ans, 2)).T * f(u)).T * np.exp(-net[1].dot(f(u))))).T
    # dW
    Vs = np.average(net[1], axis=0) # матрица (вектор) V'
    dW = np.power(f(Vs.dot(f(u))), 2)*np.exp(-Vs.dot(f(u)))*Vs*np.power(f(u), 2)*np.exp(-u)
    dW = (2*np.average(ans-y)*np.ones(net[0].shape).T * dW).T * x
    mW = (net[0]!=0) + np.zeros(net[0].shape) # маска элементов матрицы W
    dW *= mW
    
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
    return f(layer2Ans(net[1], f(layer1Ans(net[0], np.array(datapiece)))))
