# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет
одну и ту же команду show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате (перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""
import yaml
from itertools import repeat
from netmiko import ConnectHandler
from concurrent.futures import ThreadPoolExecutor


def send_show_command_to_devices(devices, command, filename, limit=3):
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(send_show_command, devices, repeat(command))
    file = open(filename, 'w')
    for element in result:
        file.write(element)
    file.close()


def send_show_command(device, command):
    ssh = ConnectHandler(**device)
    ssh.enable()
    prompt = ssh.find_prompt()
    output = ssh.send_command(command)
    return f'{prompt}{command}\n{output}\n'


if __name__ == '__main__':
    with open('devices.yaml') as f:
        dev_list = yaml.safe_load(f)
    show_command = 'show ip int br'
    dst_file = 'destination.txt'
    print(send_show_command_to_devices(dev_list, show_command, dst_file))
