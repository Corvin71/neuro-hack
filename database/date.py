# -*- coding: utf-8 -*-

import random

#288 измерений в день

def get_hours(day):
    i = 1
    minute = 0
    minute_str = ''
    hour_str = ''
    second_str = ''
    hour = 0
    second = 0
    date = []
    while i < 288:
        second = random.randint(0, 59)
        if (minute < 10):
            minute_str = '0' + str(minute)
        else:
            minute_str = str(minute)
        if (hour < 10):
            hour_str = '0' + str(hour)
        else:
            hour_str = str(hour)
        if (int(second) < 10):
            second_str = '0' + str(second)
        else:
            second_str = str(second)
        date.append(str(day) + '.10.2017 ' + hour_str + ':' + minute_str + ':' + second_str)
        if (minute == 55):
            hour += 1
            minute = 0
        else:
            minute += 5
        i += 1

    return date

#10.10.2017 08:35:14
def newTime(date):
    time1 = str(date).split(' ')
    time = time1[1].split(':')
    if (int(time[1]) + 5 > 60):
        time[0] = str(int(time[0]) + 1)
        time[1] = str('00')
    else:
        time[1] = str(int(time[1]) + 5)

    return str(time1[0] + ' ' + time[0] + ':' + time[1] + ':' + time[2])

