with open('131521850387409128.log', 'r') as f:
    s = [i for i in f]

s1 = [s[i] for i in range(0, len(s), 60)]

air = []
power = []
cold = []
for line in s1:
    temp = line.split(';')
    t = float(temp[5].replace(',', '.'))
    air.append(t)
    power.append(float(temp[6].replace(',', '.'))/2000.0)
    cold.append(0.01 * t if t > 20 else 0)

with open('script.sql', 'w') as f:
   for i in range(len(air)):
       line1 = "INSERT INTO public.weather(sensor_id, celsium) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Температура1'::text), '" + str(air[i]) + "'::text);"
       line2 = "INSERT INTO public.status_sensors(sensor, statec) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Радиатор1'::text), '" + str(power[i]) + "'::text);"
       line3 = "INSERT INTO public.status_sensors(sensor, statec) VALUES((SELECT id_sensor FROM public.sensors WHERE name = 'Кондиционер1'::text), '" + str(cold[i]) + "'::text);"
       f.write(line1 + '\n')
       f.write(line2 + '\n')
       f.write(line3 + '\n')

