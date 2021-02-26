# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show с помощью netmiko,
а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br и устройствах из devices.yaml.
"""
from task_21_3 import parse_command_dynamic
from netmiko import ConnectHandler


def send_and_parse_show_command(device_dict, command, templates_path, index='index'):
    attributes = {'Command': command, 'Vendor': device_dict['device_type']}
    ssh = ConnectHandler(**device_dict)
    ssh.enable()
    output = ssh.send_command(command)
    result = parse_command_dynamic(output, attributes, index_file=index, templ_path=templates_path)
    return result


if __name__ == '__main__':
    cisco_router = {
        'device_type': 'cisco_ios',
        'host': '192.168.100.93',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'
    }
    print(send_and_parse_show_command(cisco_router, 'sh ip int br', 'templates'))
