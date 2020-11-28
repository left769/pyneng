# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт:
Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""




value = False

while value == False:
    input_ip = (input('Enter IP-address: ')).split(sep='.')
    try:
        ip = [int(input_ip[0]), int(input_ip[1]), int(input_ip[2]), int(input_ip[3])]
        value = True
    except ValueError:
        value = False
        continue
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
