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
answer = '/smartHack/Server/answer.php'
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
    request = u2.Request(address + answer, postData)
    response = u2.urlopen(request)
    return

''' Обучение и эксплуатация нейронок '''
# Вызывается, когда нужно обучить сеть.
# Возвращает количество дней, оставшихся для обучения
def learning(datablock, c_net, e_net, days_left):
    Xc, Yc = to_c_blocks(datablock)
    Xe, Ye = to_e_blocks(datablock)
    c_net = c.learn_epoch(Xc, Yc, c_net)
    e_net = e.learn_epoch(Xe, Ye, e_net)
    # Расчёт оптимизатора ВЫКИНУТЬ ИЗ РЕЛИЗА!
    print 'Optimization before learning (for middle): '
    temps = [Xc[30][i] for i in range(2, len(Xc[0]), 2)]
    params = [Xc[30][0]] + [Xc[30][i] for i in range(3, len(Xc[0]), 2)]
    print e.optimize(temps, count_of_rooms(datablock[0]), e_net, c_net, params)
    # Расчёт ошибок
    c_err, e_err = 0, 0
    for i in range(len(Xc)):
        c_err += c.error(c.calc(Xc[i], c_net), Yc[i])
        e_err += e.error(e.calc(Xe[i], e_net), Ye[i])
    c_err /= len(Xc)
    e_err /= len(Xe)
    days_left -= 1
    # Логгирование и сохранение
    log('Epoch complete. Errors: comfort: ' + str(c_err) + '; econom: ' + str(e_err) + '. Left (days): ' + str(days_left))
    save_net(c_net, e_net, days_left) # Сохранение данных каждый день
    if days_left != 0:
        await()
    return c_net, e_net, days_left

# Возвращает вектор крутилок при поддержании режима "Комфорт"
def comfort(datapiece, c_net):
    log('Task for comfort-mode')
    x, y = to_c_block(datapiece)
    return c.calc(x, c_net)

# Возвращает вектор крутилок при поддержании режима "Эконом"
def econom(datapiece, c_net, e_net):
    log('Task for econom-mode')
    temps = [datapiece[i] for i in range(2, len(datapiece), 2)]
    params = [datapiece[0]] + [datapiece[i] for i in range(3, len(datapiece), 2)]
    e_res = e.optimize(temps, count_of_rooms(datapiece), e_net, c_net, params)
    return e_res

''' Запись и загрузка нейронок '''
# Сохраняет сети и количество дней (в файл или на сервер)
def save_net(c_net, e_net, days_left):
    with open('neuronet.npy', 'wb') as f:
        np.save(f, np.array([c_net, e_net, days_left]))
    log('Saved')
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
        temp_x = [datapiece[0], datapiece[2]] # Прикручиваем время суток и крутилку газа
        for i in range(3, len(datapiece), 5):
            temp_x.append(datapiece[i])       # Докидываем температуру
            temp_x.append(datapiece[i + 1])   # и присутствие
        x.append(temp_x)
        temp_y = []
        for i in range(5, len(datapiece), 5):
            temp_y.append(datapiece[i])       # Присобачиваем крутилку кондиционера
            temp_y.append(datapiece[i + 1])   # и крутилку радиатора
        y.append(temp_y)
    return x, y

# Генерация обучающей выборки для "Эконома"
def to_e_blocks(datablock):
    x = []
    y = []
    for datapiece in datablock:
        temp_x = []
        for i in range(3, len(datapiece), 5):
            temp_x.append(datapiece[i + 3]) # Привинчиваем крутилку радиатора
            temp_x.append(datapiece[i + 2]) # Присасываем крутилку кондиционера
            temp_x.append(datapiece[i])     # Присобачиваем температуру
        temp_x.append(datapiece[2])         # Докидываем крутилку газа
        x.append(temp_x)
        s = 0
        for i in range(7, len(datapiece), 5):
            s += datapiece[i]               # Находим сумму энергий
        temp_y = [datapiece[1], s]          # и докидываем расходы
        y.append(temp_y)
    return x, y

''' Служебное '''
# Получить количество комнат по выборке
def count_of_rooms(datablock):
    return int(len(datablock[3:]) / 5)

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
    return

''' Параметры командной строки '''
# Инициализация системы
def initialization():
    n = int(u.urlopen(address + path + rooms).read()[3:]) # Всегда считываются 3 левых символа - убираем
    c_net, e_net = c.init(n), e.init(n) # Создаём сети
    days_left = 7 # Неделя на обучение
    return c_net, e_net, days_left

# Режим продолжения прерванного обучения
def continue_mode():
    log('Started in continue-mode')
    c_net, e_net, days_left = load_net('neuronet.npy') # Загружаем сети и количество дней
    while days_left > 0:
        datablock = get_data(learning=True)
        c_net, e_net, days_left = learning(datablock, c_net, e_net, days_left)
    log('Successfully learned')
    return

# Режим обучения
def learn_only_mode():
    log('Started in learn-only-mode')
    c_net, e_net, days_left = initialization()
    while days_left > 0:
        datablock = get_data(learning=True)
        c_net, e_net, days_left = learning(datablock, c_net, e_net, days_left)
    log('Successfully learned')
    return

# Рабочий режим
def work_mode(em=False):
    log('Started in work-mode')
    c_net, e_net, days_left = load_net('neuronet.npy') # Загружаем сети и количество дней
    data = get_data()
    if days_left > 0:
        mode = 'econom-mode' if em else 'comfort-mode'
        log('Failure! Trying to use non-trained net in ' + mode)
        post_data(['Сбой! Попытка использовать необученную сеть.'])
        return
    result = econom(data, c_net, e_net) if em else comfort(data, c_net, e_net)
    post_data(result)
    return

# Режим отладки
def debug_mode():
    log('Started in debug-mode')
    c_net, e_net, days_left = initialization()
    while days_left > 0:
        day = d.date(2017, 10, 11)
        datablock = get_data(learning=True, day=day)
        day += timedelta(days=1)
        c_net, e_net, days_left = learning(datablock, c_net, e_net, days_left)
    log('Successfully learned')
    post_data([1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 0])
    return

# Выбор паттерна введённых параметров
def pattern(param):
    return {
        param == '--econom' or param == '-e': lambda: work_mode(True),
        param == '--comfort' or param == '-c': lambda: work_mode(),
        param == '--continue' or param == '-cm': continue_mode,
        param == '--learn-only' or param == '-lo': learn_only_mode,
        param == '--debug' or param == '-d': debug_mode,
        param == '--help' or param == '-h': help_mode
    }[True]

# Справка
def help_mode():
    print "9 HE CyMEJI IIO4uHuTb KOguPOBKy, TAK 4TO COCHuTE XEP - CIIPABKu HE 6ygET!"
    return
