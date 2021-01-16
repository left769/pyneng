# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re
import glob


def parse_sh_cdp_neighbors(sh_cdp_n):
    result = {}
    neighbors = {}
    match_dev = re.search(r'(?P<dev_name>\S+)>sh\w+ c\w+ n\w+\n', sh_cdp_n)
    match_neigh = re.finditer(r'(?P<rem_dev>\S+) +(?P<local_int>\S+ \S+) +\d+ +.+ +(?P<port_id>\S+ \S+)\n', sh_cdp_n)
    for match in match_neigh:
        neighbors[match.group('local_int')] = {match.group('rem_dev'): (match.group('port_id'))}
    result[match_dev.group(1)] = neighbors
    return result


if __name__ == '__main__':
    files = glob.glob('sh_cdp_n*')
    for file in files:
        with open(file) as f:
            print(parse_sh_cdp_neighbors(f.read()))
