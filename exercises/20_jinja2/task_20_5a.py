# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует шаблоны из задания 20.5 для настройки VPN на маршрутизаторах на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству
* dst_device_params - словарь с параметрами подключения к устройству
* src_template - имя файла с шаблоном, который создает конфигурацию для одной строны туннеля
* dst_template - имя файла с шаблоном, который создает конфигурацию для второй строны туннеля
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов и данных на каждом устройстве с помощью netmiko.
Функция возвращает вывод с набором команд с двух марушртизаторов (вывод, которые возвращает метод netmiko send_config_set).

При этом, в словаре data не указан номер интерфейса Tunnel, который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel, взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 9.
И надо будет настроить интерфейс Tunnel 9.

Для этого задания нет теста!
"""
from netmiko import ConnectHandler
from task_20_1 import generate_config
import yaml
import re


data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}


def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    src_data = generate_config(src_template, vpn_data_dict)
    dst_data = generate_config(dst_template, vpn_data_dict)
    # send_commands(src_device_params, src_data)
    # send_commands(dst_device_params, dst_data)
    intf = set(send_show_command(src_device_params) + send_show_command(dst_device_params))
    return intf






def send_show_command(device):
    ssh = ConnectHandler(**device)
    ssh.enable()
    match = re.findall(r'Tunnel(\d+)', ssh.send_command('sh ip int br'))
    return match


def send_commands(dev_param, commands):
    ssh = ConnectHandler(**dev_param)
    ssh.enable()
    ssh.send_config_set(commands)


if __name__ == '__main__':
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    print(configure_vpn(devices[0], devices[1], 'templates/gre_ipsec_vpn_1.txt', 'templates/gre_ipsec_vpn_2.txt', data))
