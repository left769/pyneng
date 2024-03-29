# -*- coding: utf-8 -*-
"""
Задание 19.3a

Создать функцию send_command_to_devices, которая отправляет
список указанных команды show на разные устройства в параллельных потоках,
а затем записывает вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять какие команды. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом каждой команды надо написать имя хоста и саму команду):

R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          87   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R1#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  10.30.0.1               -   aabb.cc00.6530  ARPA   Ethernet0/3.300
Internet  10.100.0.1              -   aabb.cc00.6530  ARPA   Ethernet0/3.100
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down
R3#sh ip route | ex -

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
O        10.1.1.1/32 [110/11] via 192.168.100.1, 07:12:03, Ethernet0/0
O        10.30.0.0/24 [110/20] via 192.168.100.1, 07:12:03, Ethernet0/0


Порядок команд в файле может быть любым.

Для выполнения задания можно создавать любые дополнительные функции, а также использовать функции созданные в предыдущих заданиях.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""
import yaml
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
commands = {
    "192.168.100.93": ["sh ip int br", "sh ip route | ex -"],
    "192.168.100.94": ["sh ip int br", "sh int desc"],
    "192.168.100.92": ["sh int desc"],
}


def send_command_to_devices(devices, commands_dict, filename, limit=3):
    sorted_commands = []
    for device in devices:
        for ip_host in commands_dict.keys():
            if device['host'] == ip_host:
                sorted_commands.append(commands_dict[ip_host])
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(send_command, devices, sorted_commands)
    file = open(filename, 'w')
    for element in result:
        file.write(element)
    file.close()


def send_command(device, commands_list):
    result = ''
    ssh = ConnectHandler(**device)
    ssh.enable()
    prompt = ssh.find_prompt()
    for command in commands_list:
        output = ssh.send_command(command)
        result = result + f'{prompt}{command}{output}\n'
    return result


if __name__ == '__main__':
    with open('devices.yaml') as f:
        dev_list = yaml.safe_load(f)
    print(send_command_to_devices(dev_list, commands, 'destinatiion.txt'))
