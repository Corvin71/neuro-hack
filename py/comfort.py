# -*- coding: UTF-8 -*-
import numpy as np

# Инициализация сети
def init(n):
    return np.zeros(shape=(2*n, 2*n + 1))

# Одна итерация обучения
def learn_iter(x, y, net):
    return 0.0 # Возврат ошибки

# Одна эпоха обучения (день)
def learn_epoch(X, Y, net):
    return [] # возврат обученной сети

# Расчёт по нейронной сети
def calc(datapiece, net):
    return []
