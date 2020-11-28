# -*- coding: utf-8 -*-
"""
Задание 7.2c

Переделать скрипт из задания 7.2b:
* передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации,
в которых содержатся слова из списка ignore.
И записать остальные строки в итоговый файл.

Проверить работу скрипта на примере файла config_sw1.txt.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
from sys import argv

ignore = ["duplex", "alias", "Current configuration"]

config = argv[1]

dst_file = argv[2]

with open(config) as src:
    for line in src:
        for stimulant in ignore:
            counter = line.count(stimulant)
            if counter != 0:
                break
        else:
            dst = open(dst_file, 'a+')
            dst.write(line)

dst.close()


