# -*- coding: utf-8 -*-
"""
Задание 15.1a

Скопировать функцию get_ip_from_cfg из задания 15.1 и переделать ее таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

В словарь добавлять только те интерфейсы, на которых настроены IP-адреса.

Например (взяты произвольные адреса):
{'FastEthernet0/1': ('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2': ('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

"""
import re


def get_ip_from_cfg(filename):
    regex = (r'interface (?P<interface>\S+)\n'
             r'( .+\n){0,2}'
             r' ip address (?P<ip_addr>\d+.\d+.\d+.\d+) (?P<mask>\d+.\d+.\d+.\d+)')

    result = {}

    with open(filename) as f:
        match_group = re.finditer(regex, f.read())
        for match in match_group:
            interface = match.group('interface')
            ip_addr = match.group('ip_addr')
            mask = match.group('mask')
            result[interface] = (ip_addr, mask,)
    return result


if __name__ == "__main__":
    print(get_ip_from_cfg('config_r1.txt'))
