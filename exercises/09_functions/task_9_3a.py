# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию:
    - добавить поддержку конфигурации, когда настройка access-порта выглядит так:
            interface FastEthernet0/20
                switchport mode access
                duplex auto
      То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
      Пример словаря: {'FastEthernet0/12': 10,
                       'FastEthernet0/14': 11,
                       'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""



def get_int_vlan_map(config_filename):
    access_ports = {}
    trunk_ports = {}
    with open(config_filename) as f:
        for line in f:
            if 'Ethernet' in line:
                interface = line.split()[1]
                access_ports[interface] = 1
            elif 'access vlan' in line:
                vid = line.split()[-1]
                #access_ports[interface] = {}
                access_ports[interface] = int(vid)
            elif 'trunk allowed vlan' in line:
                vid = (line.split()[-1]).split(sep=',')
                test = [int(item) for item in vid if item.isdigit()]
                trunk_ports[interface] = test
                del access_ports[interface]
    result = (access_ports,trunk_ports)
    return result


