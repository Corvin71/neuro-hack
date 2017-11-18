# -*- coding: utf-8 -*-
import date
import random
import urllib2 as u2

address = 'http://localhost'
answer = '/smartHome/Server/answer.php'

'''
with open('131521850387409128.log', 'r') as f:
    s = [i for i in f]

s1 = [s[i] for i in range(0, len(s), 1200)]
'''

def generate(_date, startCelsius, nameFile, step):
    _air1 = [] #t
    _power1 = [] #R
    _cold1 = [] #C
    _move1 = [] #p

    _energy1 = [] #E
    '''_con_gas1 = [] #G
    _gas1 = [] #g'''

    # Генерация для одного датчика
    # Cтартовая температура
    startCelsiumSensor1 = startCelsius
    # До скольких градусов греем
    endCelsiumSensor1 = startCelsiumSensor1 + int(random.randint(5, 20))
    airTime = random.randint(25, 72)
    # На протяжении какого времени нужно греть температуру
    amountHour = random.randint(5, 12)
    # Время стационарного режима
    amountStableHour = random.randint(17, 25)
    _deltaTemperature = float(endCelsiumSensor1 - startCelsiumSensor1) / float(amountHour)

    for i in range(len(_date)):
        # Держим температуру...
        if (i < airTime):
            _air1.append(str(startCelsiumSensor1 + random.uniform(-0.4, 0.4)))
            _move1.append('0')
            _cold1.append('0')
            _power1.append('0')
            _energy1.append('0')
        # Греем ...
        elif (i >= airTime) and (i < airTime + amountHour):
            _move1.append('1')
            _power1.append(str(0.9 + random.uniform(-0.1, 0.1)))
            c = 0.5 + random.uniform(-0.1, 0.1)
            _cold1.append(str(c))
            _energy1.append(str(c * 1.1))
            startCelsiumSensor1 += _deltaTemperature + random.uniform(-0.2, 0.2)
            _air1.append(str(startCelsiumSensor1))
        # Держим стационарный режым...
        elif (i >= airTime + amountHour) and (i < airTime + amountHour + amountStableHour):
            _move1.append('1')
            _power1.append(str(0.3 + random.uniform(-0.1, 0.1)))
            _cold1.append(str(0.4 + random.uniform(-0.1, 0.1)))
            _energy1.append(str(c * 1.1))
            _air1.append(str(startCelsiumSensor1 + random.uniform(-1, 0.2)))
        # Человек уходит
        else:
            _move1.append('0')
            _cold1.append('0')
            _power1.append('0')
            _energy1.append('0')

            if (startCelsiumSensor1 >= startCelsius):
                startCelsiumSensor1 += random.uniform(-0.8, 0)
                _air1.append(str(startCelsiumSensor1))
            else:
                _air1.append(str(startCelsiumSensor1 + random.uniform(-0.2, 0.2)))

    '''for i in range(len(_date)):
        print(_date[i] + ' - ' + _air1[i] + ' - ' + _power1[i] + ' - ' + _cold1[i] + ' - ' + _move1[i])
'''
    #Запись в файлы.
    """with open(str('sql/'+nameFile + '.sql'), 'w') as f:
        for i in range(len(_air1)):
            line1 = "INSERT INTO public.status_sensors(sensor_id, celsium, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Температура"+ str(step) +"'::text), '" + str(
                _air1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            line2 = "INSERT INTO public.status_sensors(sensor_id, twister_radiator, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Радиатор"+ str(step) +"'::text), '" + str(
                _power1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            line3 = "INSERT INTO public.status_sensors(sensor_id, twister_cold, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Кондиционер"+ str(step) +"'::text), '" + str(
                _cold1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            line4 = "INSERT INTO public.status_sensors(sensor_id, energy, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Энергия"+ str(step) +"'::text), '" + str(
                _energy1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            line5 = "INSERT INTO public.status_sensors(sensor_id, smove, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Движение"+ str(step) +"'::text), '" + str(
                _move1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            f.write(line1 + '\n')
            f.write(line2 + '\n')
            f.write(line3 + '\n')
            f.write(line4 + '\n')
            f.write(line5 + '\n')
"""

    #Формирование запроса. Отправка post данных.
    line1 = ""
    for i in range(len(_air1)):
        line1 += "INSERT INTO public.status_sensors(sensor_id, celsium, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Температура" + str(
            step) + "'::text), '" + str(
            _air1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
        line1 += "INSERT INTO public.status_sensors(sensor_id, twister_radiator, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Радиатор" + str(
            step) + "'::text), '" + str(
            _power1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
        line1 += "INSERT INTO public.status_sensors(sensor_id, twister_cold, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Кондиционер" + str(
            step) + "'::text), '" + str(
            _cold1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
        line1 += "INSERT INTO public.status_sensors(sensor_id, energy, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Энергия" + str(
            step) + "'::text), '" + str(
            _energy1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
        line1 += "INSERT INTO public.status_sensors(sensor_id, smove, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Движение" + str(
            step) + "'::text), '" + str(
            _move1[i]) + "'::text, '" + str(_date[i]) + "'::text);"

    #line1 - строка, в которой лежат все INSERT'ы.
    return [float(item) for item in _power1], line1

line1 = ""
for j in range(7):
    _date = date.get_hours(11 + j) #T
    s = [0 for i in range(71)]
    for i in range(1,6):
        s1, line1 = generate(_date, 15 + random.uniform(-1.5, 1.5), "room" + str(i) + '_' + str(j), i)
        s = list(map(lambda x, y: x + y, s, s1))
    s = [1.0 / item if item > 1 else item for item in s]
    for k in range(len(s)):
        line1 += "INSERT INTO public.status_sensors(sensor_id, consum_gas, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Бойлер'::text), '" + str(
            s[k]) + "'::text, '" + str(_date[k]) + "'::text);"
        line1 += "INSERT INTO public.status_sensors(sensor_id, twister_gas, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'ЗадвижкаБойлера'::text), '" + str(
            1.0/(s[k]*1.1) if s[k] > 1 else s[k]*1.1) + "'::text, '" + str(_date[k]) + "'::text);"

#Отправка post - запросом данных в базу.
postData = "ins_db=" + line1
request = u2.Request(address + answer, postData)
response = u2.urlopen(request)

'''for line in s1:
    temp = line.split(';')
    t = float(temp[5].replace(',', '.'))
    air.append(t)
    power.append(float(temp[6].replace(',', '.'))/2000.0)
    cold.append(0.01 * t if t > 20 else 0)
    date.append(temp[13])
'''



# (sensor_id, consum_gas, twister_gas, celsium, twister_cold, twister_radiator, energy, date)

