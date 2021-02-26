# -*- coding: utf-8 -*-
"""
Задание 21.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в параллельных потоках функцию send_and_parse_show_command из задания 21.4.

В этом задании надо самостоятельно решить:
* какие параметры будут у функции
* что она будет возвращать


Теста для этого задания нет.
"""
from itertools import repeat
from task_21_4 import send_and_parse_show_command
from concurrent.futures import ThreadPoolExecutor
import yaml


def send_and_parse_command_parallel(devices, command, templates_path, index='index'):
    with ThreadPoolExecutor(max_workers=3) as executor:
        result = executor.map(send_and_parse_show_command, devices, repeat(command), repeat(templates_path), repeat(index))
    for row in result:
        print(row)
    return result


if __name__ == "__main__":
    with open('devices.yaml') as f:
        dev_list = yaml.safe_load(f)
    show_command = 'sh ip int br'
    print(send_and_parse_command_parallel(dev_list, show_command, 'templates'))
