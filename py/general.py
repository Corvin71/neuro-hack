# -*- coding: UTF-8 -*-
# ДОБАВИТЬ И ИСПРАВИТЬ ГЕНЕРАЦИЮ ДАННЫХ ДЛЯ КАЖДОЙ НЕЙРОСЕТИ!
import sys
import time as t
import urllib as u
import comfort as c
import econom as e
address = 'http://corvin71.ddns.net'
path = '/smartHack/Server/data_collection.php'
learning = '?is_learning=1'
rooms = '?how_rooms=1'
post = ''
save = ''
load = ''

''' Работа с удалённым сервером '''
# Получает данные с сервера уже в виде вектора.
# Если is_learning == True, то получает данные для обучения
# (вместе со всеми крутилками).
def get_data(is_learning):
    if is_learning:
        #t.sleep(86400) # Ждём 24 часа
        response = u.urlopen(address + path + learning)
    else:
        response = u.urlopen(address + path)
    return []

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
    return # Сохраняет сети и количество дней (в файл или на сервер)

def load_net():
    return [], [], 0 # Загружает сети и количество (из файла или с сервера)

''' Служебное '''
# Определяет, включен ли режим "Эконом"
def econom_mode_on(datapiece):
    return True

# Генерация обучающей выборки для "Комфорта"
def to_c_blocks(datablock):
    x = []
    y = []
    for datapiece in datablock:
        temp_x = [datapiece[1]]
        for i in range(2, len(datapiece), 4):
            temp_x.append(datapiece[i])
            temp_x.append(datapiece[i + 1])
        x.append(temp_x)
        temp_y = []
        for i in range(4, len(datapiece), 4):
            temp_y.append(datapiece[i])
            temp_y.append(datapiece[i + 1])
        y.append(temp_y)
    return x, y

# Генерация обучающей выборки для "Эконома"
def to_e_blocks(datablock):
    x = []
    y = []
    for datapiece in datablock:
        
    return x, y

''' Главная функция '''
def main():
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            # Проверка аргументов?
            c_net, e_net, days_left = load_net() # Загружаем сети и количество дней
        else:
            n = int(u.urlopen(address + path + rooms).read())
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
                d = get_data(True)
                if d == []:
                    return
                c_net, e_net, days_left = learning(d, c_net, e_net, days_left)
    return

#main()

q = [['T', 'G', 'g', 't1', 'p1', 'C1', 'R1', 'E1', 't2', 'p2', 'C2', 'R2', 'E2'],['T', 'G', 'g', 'T', 't1', 'p1', 'C1', 'R1', 'E1', 't2', 'p2', 'C2', 'R2', 'E2']]
x, y = to_c_blocks(q)
print x, y
