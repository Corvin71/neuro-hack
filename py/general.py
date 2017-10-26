# -*- coding: UTF-8 -*-
import sys
import time as t
import urllib as u
import comfort as c
import econom as e
address = 'http://corvin71.ddns.net'
path = '/smartHack/Server'
get = '/data_collection.php'
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
        response = u.urlopen(address + path + get + '?is_learning=1')
    else:
        response = u.urlopen(address + path + get)
    return []

def post_data(result):
    return # Возвращает результат работы нейронок result на сервер

''' Обучение и эксплуатация нейронок '''
# Вызывается, когда нужно обучить сеть.
# Возвращает количество дней, оставшихся для обучения
def learning(datablock, c_net, e_net, days_left):
    c.learn_epoch(datablock, c_net)
    e.learn_epoch(datablock, e_net)
    save_net(c_net, e_net, days_left - 1) # Сохранение данных каждый день
    return days_left - 1
    #return 0.0, 0.0 # Вызывается, когда нужно обучить сеть. Возвращает ошибки сетей "Комфорт" и "Эконом"

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
def econom_mode_on(datapiece):
    return True # Определяет, включен ли режим "Эконом"

''' Главная функция '''
def main():
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            # Проверка аргументов?
            c_net, e_net, days_left = load_net() # Загружаем сети и количество дней
        else:
            c_net, e_net = c.init(), e.init() # Создаём сети
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
                days_left = learning(d, c_net, e_net, days_left)
    return

main()
