# -*- coding: utf-8 -*-
"""
Задание 7.2a

Сделать копию скрипта задания 7.2.

Дополнить скрипт:
  Скрипт не должен выводить команды, в которых содержатся слова,
  которые указаны в списке ignore.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv

ignore = ["duplex", "alias", "Current configuration"]

config = argv[1]

with open(config) as src:
    for line in src:
        for stimulant in ignore:
            counter = line.count('!') + line.count(stimulant)
            if counter != 0:
                break
        else:
            print(line.rstrip())

