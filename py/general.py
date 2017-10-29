# -*- coding: UTF-8 -*-
import sys
import numpy as np
import json as j
import time as t
import datetime as d
import urllib as u
import urllib2 as u2
import comfort as c
import econom as e
address = 'http://corvin71.ddns.net'
path = '/smartHack/Server/data_collection.php'
is_learning = '?is_learning='
rooms = '?how_rooms=1'
save = ''
load = ''

''' Отладка!!! '''
from datetime import timedelta

''' Работа с удалённым сервером '''
# Получает данные с сервера уже в виде вектора.
# Если is_learning == True, то получает данные для обучения
# (вместе со всеми крутилками).
def get_data(learning=False, day=d.datetime.today().date()):
    if learning:
        response = u.urlopen(address + path + is_learning + d.datetime.strftime(day, "%d.%m.%Y"))
    else:
        log('Listening to sever')
        response = u.urlopen(address + path)
        log('Answer received')
    return j.loads(response.read()[3:])

# Загружает полученную информацию на сервер
def post_data(result):
    postData = "ans=" + str(result)
    request = u2.Request(address + path, postData)
    response = u2.urlopen(request)

''' Обучение и эксплуатация нейронок '''
# Вызывается, когда нужно обучить сеть.
# Возвращает количество дней, оставшихся для обучения
def learning(datablock, c_net, e_net, days_left):
    Xc, Yc = to_c_blocks(datablock)
    Xe, Ye = to_e_blocks(datablock)
    c_net = c.learn_epoch(Xc, Yc, c_net)
    e_net = e.learn_epoch(Xe, Ye, e_net)
    days_left -= 1
    save_net(c_net, e_net, days_left) # Сохранение данных каждый день
    if days_left != 0:
        await()
    return c_net, e_net, days_left

# Возвращает вектор крутилок при поддержании режима "Комфорт"
def comfort(datapiece, c_net):
    x, y = to_c_block(datapiece)
    return c.calc(x, c_net)

# Возвращает вектор крутилок при поддержании режима "Эконом"
def econom(datapiece, c_net, e_net):
    x_c = to_work_c_block(datapiece)
    c_res = c.calc(x_c, c_net)
    x_e = to_work_e_block(datapiece, c_res)
    e_res = e.calc(c_res, e_net)
    return c_res + e_res

''' Запись и загрузка нейронок '''
# Сохраняет сети и количество дней (в файл или на сервер)
def save_net(c_net, e_net, days_left):
    with open('neuronet.npy', 'wb') as f:
        np.save(f, np.array([c_net, e_net, days_left]))
    log('Epoch complete. Left (days): ' + str(days_left))
    return

# Загружает сети и количество (из файла или с сервера)
def load_net(path):
    with open(path, 'rb') as f:
        obj = np.load(f)
    log('Loading complete. Days for learning left: ' + str(obj[2]))
    return obj[0], obj[1], obj[2]

''' Генераторы выборок '''
# Генерация рабочей выборки для "Комфорта"
def to_work_c_block(datapiece):
    x = [datapiece[0]]
    for i in range(3, len(datapiece), 4):
        x.append(datapiece[i])
        x.append(datapiece[i + 1])
    return x

# Генерация рабочей выборки для "Эконома"
def to_work_e_block(datapiece, twisters):
    x = []
    j = 0
    for i in range(len(twisters) - 1):
        x.append(twisters[i + 1])
        x.append(twisters[i])
        x.append(datapiece[i + 2*j])
        j += 1
    return x

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

''' Служебное '''
# Определяет, включен ли режим "Эконом"
def econom_mode_on(datapiece):
    return datapiece[0] == 0

# Ожидание данных
def await():
    tm = 5
    while tm > 0:
        log('I am alive')
        tm -= 1
        t.sleep(1) # Отладка!!!

# Ведение логов
def log(message):
    message = str(d.datetime.today()) + ': ' + message
    print message
    with open('logs.log', 'a') as log:
        log.write(message + '\n')

# Завершение работы
def halt():
    log('Halt')
    raise SystemExit

''' Параметры командной строки '''
# Инициализация системы
def initialization():
    n = int(u.urlopen(address + path + rooms).read()[3:]) # Всегда считываются 3 левых символа - убираем
    c_net, e_net = c.init(n), e.init(n) # Создаём сети
    days_left = 7 # Неделя на обучение
    return c_net, e_net, days_left

# Режим продолжения
def continue_mode():
    log('Started in continue-mode')
    c_net, e_net, days_left = load_net('neuronet.npy') # Загружаем сети и количество дней
    combine_mode(c_net, e_net, days_left)

# Режим обучения
def learn_only_mode():
    log('Started in learn-only-mode')
    c_net, e_net, days_left = initialization()
    while days_left > 0:
        datablock = get_data(learning=True)
        c_net, e_net, days_left = learning(datablock, c_net, e_net, days_left)
    log('Successfully learned')
    return

# Комбинированный режим (обучение и продолжение)
def combine_mode(c_net, e_net, days_left):
    # Если сеть ещё не обучилась
    while days_left > 0:
        datablock = get_data(learning=True)
        c_net, e_net, days_left = learning(datablock, c_net, e_net, days_left)
    # Сеть уже обучилась
    data = get_data()
    if econom_mode_on(data):
        result = econom(data, c_net, e_net)
    else:
        result = comfort(data, c_net)
    ''' Отладка!!! '''
    post_data([1,1,1])
    #post_data(result)
    return

def debug_mode():
    post_data([1,1,1,1,1])
    return

# Выбор паттерна введённых параметров
def pattern(param):
    return {
        param == '--continue-mode' or param == '-cm': continue_mode,
        param == '--learn-only-mode' or param == '-lom': learn_only_mode,
        param == '--debug' or param == '-d': debug_mode,
        param == '--help' or param == '-h': help_mode
    }[True]

# Справка
def help_mode():
    print "9 HE CyMEJI IIO4uHuTb KOguPOBKy, TAK 4TO COCHuTE XEP - CIIPABKu HE 6ygET!"
    return

''' Главная функция '''
def debug():
    if __name__ == "__main__":

        # ЭТОТ КОД НЕ ВЫПОЛНЯЕТСЯ! ЭТА ФУНКЦИЯ ПОДЛЕЖИТ УДАЛЕНИЮ!
        if len(sys.argv) > 1:
            pattern(sys.argv[1])()
        else:
            c_net, e_net, days_left = initialization()
            combine_mode()
            
    else:
        ''' ОТЛАДКА!!! '''
        c_net, e_net, days_left = initialization()
        while True:
            # Основной цикл программы
            if days_left == 0:
                halt() # Отладка!!!
                data = get_data(False)
                if data == []:
                    return
                if econom_mode_on(d):
                    result = econom(data, c_net, e_net)
                else:
                    result = comfort(data, c_net)
                post_data(result)
            else:
                # Обучение
                day = d.date(2017, 10, 11) # Отладка!!!
                data = get_data(True, day)
                day += timedelta(days=1) # Отладка!!!
                if data == []:
                    return
                c_net, e_net, days_left = learning(data, c_net, e_net, days_left)
    return
