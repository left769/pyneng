# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный файл коммутатора
и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов, а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов, а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""



def get_int_vlan_map(config_filename):
    access_ports = {}
    trunk_ports = {}
    with open(config_filename) as f:
        for line in f:
            if 'Ethernet' in line:
                interface = line.split()[1]
            elif 'access vlan' in line:
                vid = line.split()[-1]
                access_ports[interface] = {}
                access_ports[interface] = int(vid)
    with open(config_filename) as f:
        for line in f:
            if 'Ethernet' in line:
                interface = line.split()[1]
            elif 'trunk allowed vlan' in line:
                vid = (line.split()[-1]).split(sep=',')
                test = [int(item) for item in vid if item.isdigit()]
                trunk_ports[interface] = {}
                trunk_ports[interface] = test
    result = (access_ports,trunk_ports)
    return result
