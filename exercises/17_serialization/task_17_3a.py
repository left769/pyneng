# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод команды show cdp neighbor из нескольких файлов и записывает итоговую топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами, независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь в файл topology.yaml.

"""
import re
import glob
import yaml


def generate_topology_from_cdp(list_of_files, save_to_filename=None):
    result = {}
    for file in list_of_files:
        neighbors = {}
        with open(file) as f:
            src = f.read()
            match_dev = re.search(r'(?P<dev_name>\S+)>sh\w+ c\w+ n\w+\n', src)
            match_neigh = re.finditer(r'(?P<rem_dev>\S+) +(?P<local_int>\S+ \S+) +\d+ +.+ +(?P<port_id>\S+ \S+)\n', src)
            for match in match_neigh:
                neighbors[match.group('local_int')] = {match.group('rem_dev'): (match.group('port_id'))}
            result[match_dev.group(1)] = neighbors
    if type(save_to_filename) == str:
        with open(save_to_filename, 'w') as f:
            yaml.dump(result, f)
    return result


if __name__ == '__main__':
    print(generate_topology_from_cdp(glob.glob('sh_cdp_n*'), 'topology.yaml'))
