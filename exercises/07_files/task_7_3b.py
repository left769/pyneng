# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
value = False

while value == False:
    vlan = input('Enter VID: ')
    try:
        vlan = int(vlan)
        value = True
    except ValueError:
        print('VID is incorrect')
        value = False

list = []
template = "{:<4}  {:>15}  {:>6}"

with open('CAM_table.txt') as src:
    for line in src:
        counter = line.count('.')
        if counter > 0:
            plug = line.split()
            plug[0] = int(plug[0])
            plug.pop(2)
            values_tuple = tuple(plug)
            list.append(values_tuple)

list.sort()

for i in list:
    if i[0] == vlan:
        print((template.format(i[0], i[1], i[2])))

