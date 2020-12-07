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


ips = ["1.1.1", "8.8.8.8", "8.8.4.4", "8.8.7.1"]


def ping_ip_addresses(addr_list):
    import subprocess
    available = []
    not_available = []
    for ip in addr_list:
        try:
            out = subprocess.run(f'ping {ip}')
            if out.returncode == 0:
                available.append(ip)
            else:
                not_available.append(ip)
        except:
            pass
    result = (available, not_available,)
    return result





if __name__ == "__main__":
    print(ping_ip_addresses(ips))

