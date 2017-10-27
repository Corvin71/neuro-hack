# -*- coding: UTF-8 -*-
import sys
import json as j
import time as t
import urllib as u
import comfort as c
import econom as e
address = 'http://corvin71.ddns.net'
path = '/smartHack/Server/data_collection.php'
is_learning = '?is_learning='
rooms = '?how_rooms=1'
post = ''
save = ''
load = ''

''' Отладка!!! '''
from datetime import timedelta
import datetime

''' Работа с удалённым сервером '''
# Получает данные с сервера уже в виде вектора.
# Если is_learning == True, то получает данные для обучения
# (вместе со всеми крутилками).
def get_data(learning, day):
    if learning:
        #t.sleep(86400) # Ждём 24 часа
        t.sleep(1)
        #response = u.urlopen(address + path + is_learning + d.datetime.strftime(d.datetime.today().date(), "%d.%m.%Y")
        response = u.urlopen(address + path + is_learning + datetime.datetime.strftime(day, "%d.%m.%Y"))
    else:
        response = u.urlopen(address + path)
    return j.loads(response.read()[3:])

def post_data(result):
    return # Возвращает результат работы нейронок result на сервер

''' Обучение и эксплуатация нейронок '''
# Вызывается, когда нужно обучить сеть.
# Возвращает количество дней, оставшихся для обучения
def learning(datablock, c_net, e_net, days_left):
    Xc, Yc = to_c_blocks(datablock)
    Xe, Ye = to_e_blocks(datablock)
    c_net = c.learn_epoch(Xc, Yc, c_net)
    e_net = e.learn_epoch(Xe, Ye, e_net)
    save_net(c_net, e_net, days_left - 1) # Сохранение данных каждый день
    return c_net, e_net, days_left - 1

# Возвращает вектор крутилок при поддержании режима "Комфорт"
def comfort(datapiece, c_net):
    return c.calc(datapiece, c_net)

# Возвращает вектор крутилок при поддержании режима "Эконом"
def econom(datapiece, c_net, e_net):
    c_res = c.calc(datapiece, c_net)
    e_res = e.calc(c_res, e_net)
    return c_res + e_res

''' Запись и загрузка нейронок '''
def save_net(c_net, e_net, days_left):
    with open('neuronet', 'w') as f:
        f.write(str(c_net) + '\n')
        f.write(str(e_net) + '\n')
        f.write(str(days_left))
    return # Сохраняет сети и количество дней (в файл или на сервер)

def load_net():
    return [], [], 7 # Загружает сети и количество (из файла или с сервера)

''' Служебное '''
# Определяет, включен ли режим "Эконом"
def econom_mode_on(datapiece):
    return True

# Генерация обучающей выборки для "Комфорта"
def to_c_blocks(datablock):
    x = []
    y = []
    for datapiece in datablock:
        temp_x = [datapiece[0]]
        for i in range(3, len(datapiece), 5):
            temp_x.append(datapiece[i])
            temp_x.append(datapiece[i + 1])
        x.append(temp_x)
        temp_y = []
        for i in range(5, len(datapiece), 5):
            temp_y.append(datapiece[i])
            temp_y.append(datapiece[i + 1])
        y.append(temp_y)
    return x, y

# Генерация обучающей выборки для "Эконома"
def to_e_blocks(datablock):
    x = []
    y = []
    for datapiece in datablock:
        temp_x = []
        for i in range(3, len(datapiece), 5):
            temp_x.append(datapiece[i])
            temp_x.append(datapiece[i + 3])
            temp_x.append(datapiece[i + 2])
        temp_x.append(datapiece[2])
        x.append(temp_x)
        s = 0
        for i in range(7, len(datapiece), 5):
            s += datapiece[i]
        temp_y = [datapiece[1], s]
        y.append(temp_y)
    return x, y

''' Главная функция '''
def main():
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            # Проверка аргументов?
            c_net, e_net, days_left = load_net() # Загружаем сети и количество дней
        else:
            n = int(u.urlopen(address + path + rooms).read()[3:])
            c_net, e_net = c.init(n), e.init(n) # Создаём сети
            days_left = 7 # Неделя на обучение

        while True:
            # Основной цикл программы
            if days_left == 0:
                d = get_data(False)
                if d == []:
                    return
                if econom_mode_on(d):
                    result = econom(d, c_net, e_net)
                else:
                    result = comfort(d, c_net)
                post_data(result)
            else:
                # Обучение
                day = datetime.date(2017, 10, 11) # Отладка!!!
                d = get_data(True, day)
                day += timedelta(days=1) # Отладка!!!
                if d == []:
                    return
                c_net, e_net, days_left = learning(d, c_net, e_net, days_left)
    return

main()
