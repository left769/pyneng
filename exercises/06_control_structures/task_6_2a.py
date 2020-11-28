# -*- coding: utf-8 -*-
"""
Задание 6.2a

Сделать копию скрипта задания 6.2.

Добавить проверку введенного IP-адреса. Адрес считается корректно заданным, если он:
   - состоит из 4 чисел (а не букв или других символов)
   - числа разделенны точкой
   - каждое число в диапазоне от 0 до 255

Если адрес задан неправильно, выводить сообщение:
'Неправильный IP-адрес'

Сообщение должно выводиться только один раз.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

value = True

input_ip = (input('Enter IP-address: ')).split(sep='.')
try:
    ip = [int(input_ip[0]), int(input_ip[1]), int(input_ip[2]), int(input_ip[3])]
except ValueError:
    value = False


if value == True and len(input_ip) == 4:
    for octet in ip:
        if octet not in range(256):
            value = False
else:
    value = False

if value == True:
    if ip[0] >= 1 and ip[0] <=223:
        print('unicast')
    elif ip[0] >= 224 and ip[0] <= 239:
        print('multicast')
    elif ip[0] == 255 and ip[1] == 255 and ip[2] == 255 and ip[3] == 255:
        print('local broadcast')
    elif ip[0] == 0 and ip[0] == 0 and ip[0] == 0 and ip[0] == 0:
        print('unassigned')
    else:
        print('unused')
else:
    print('Invalid IP')