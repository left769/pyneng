# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess

addresses = ['1.1.1.1', '192.168.1.1', '8.8.8.8', '5.5.5.5', '127.0.0.1']


def ping_ip_addresses(addr_list):
    available = []
    not_available = []
    for ip in addr_list:
        result = subprocess.run('ping {}'.format(ip))
        if result.returncode == 0:
            available.append(ip)
        else:
            not_available.append(ip)
    test = (available, not_available,)
    return test





if __name__ == "__main__":
    print(ping_ip_addresses(addresses))

