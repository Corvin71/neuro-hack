# -*- coding: utf-8 -*-
import date
import random

'''
with open('131521850387409128.log', 'r') as f:
    s = [i for i in f]

s1 = [s[i] for i in range(0, len(s), 1200)]
'''

def generate(day, startCelsius, nameFile):
    _air1 = []
    _power1 = []
    _cold1 = []
    _move1 = []
    _date = date.get_hours(day)

    # Генерация для одного датчика
    # Cтартовая температура
    startCelsiumSensor1 = startCelsius
    # До скольких градусов греем
    endCelsiumSensor1 = startCelsiumSensor1 + int(random.randint(5, 20))
    airTime = random.randint(50, 150)
    # На протяжении какого времени нужно греть температуру
    amountHour = random.randint(10, 50)
    # Время стационарного режима
    amountStableHour = random.randint(20, 30)
    _deltaTemperature = float(endCelsiumSensor1 - startCelsiumSensor1) / float(amountHour)

    for i in range(len(_date)):
        # Держим температуру...
        if (i < airTime):
            _air1.append(str(startCelsiumSensor1 + random.uniform(-0.4, 0.4)))
            _move1.append('0')
            _cold1.append('0')
            _power1.append('0')
        # Греем ...
        elif (i >= airTime) and (i < airTime + amountHour):
            _move1.append('1')
            _power1.append(str(0.9 + random.uniform(-0.1, 0.1)))
            _cold1.append(str(0.5 + random.uniform(-0.1, 0.1)))

            startCelsiumSensor1 += _deltaTemperature + random.uniform(-0.2, 0.2)
            _air1.append(str(startCelsiumSensor1))
        # Держим стационарный режым...
        elif (i >= airTime + amountHour) and (i < airTime + amountHour + amountStableHour):
            _move1.append('1')
            _power1.append(str(0.3 + random.uniform(-0.1, 0.1)))
            _cold1.append(str(0.4 + random.uniform(-0.1, 0.1)))

            _air1.append(str(startCelsiumSensor1 + random.uniform(-1, 0.2)))
        # Человек уходит
        else:
            _move1.append('0')
            _cold1.append('0')
            _power1.append('0')

            if (startCelsiumSensor1 >= startCelsius):
                startCelsiumSensor1 += random.uniform(-0.8, 0)
                _air1.append(str(startCelsiumSensor1))
            else:
                _air1.append(str(startCelsiumSensor1 + random.uniform(-0.2, 0.2)))

    '''for i in range(len(_date)):
        print(_date[i] + ' - ' + _air1[i] + ' - ' + _power1[i] + ' - ' + _cold1[i] + ' - ' + _move1[i])
'''

    with open(str(nameFile + '.sql'), 'w') as f:
        for i in range(len(_air1)):
            line1 = "INSERT INTO public.weather(sensor_id, celsium, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Температура1'::text), '" + str(
                _air1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            line2 = "INSERT INTO public.status_sensors(sensor, statec, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Радиатор1'::text), '" + str(
                _power1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            line3 = "INSERT INTO public.status_sensors(sensor, statec, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Кондиционер1'::text), '" + str(
                _cold1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            line4 = "INSERT INTO public.status_sensors(sensor, statec, date) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Движение1'::text), '" + str(
                _move1[i]) + "'::text, '" + str(_date[i]) + "'::text);"
            f.write(line1 + '\n')
            f.write(line2 + '\n')
            f.write(line3 + '\n')
            f.write(line4 + '\n')


generate(25, 14.08, "tiichki")


'''for line in s1:
    temp = line.split(';')
    t = float(temp[5].replace(',', '.'))
    air.append(t)
    power.append(float(temp[6].replace(',', '.'))/2000.0)
    cold.append(0.01 * t if t > 20 else 0)
    date.append(temp[13])
'''



