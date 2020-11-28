# -*- coding: utf-8 -*-
"""
Задание 6.2

1. Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
2. В зависимости от типа адреса (описаны ниже), вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

input_ip = (input('Enter IP-address: ')).split(sep='.')
ip = [int(input_ip[0]), int(input_ip[1]), int(input_ip[2]), int(input_ip[3])]

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
