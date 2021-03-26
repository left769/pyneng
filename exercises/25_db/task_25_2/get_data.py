# -*- coding: utf-8 -*-
import sqlite3
from tabulate import tabulate
from sys import argv


def get_info(parameter=None, value=None):
    connection = sqlite3.connect('dhcp_snooping.db')
    cursor = connection.cursor()
    if parameter and value:
        try:
            query = f'SELECT * FROM dhcp WHERE {parameter} = ?'
            result = cursor.execute(query, (value,))
            return result.fetchall()
        except sqlite3.OperationalError:
            return 'Данный параметр не поддерживается.\n' \
                   'Допустимые значения параметров: mac, ip, vlan, interface, switch'
    elif not parameter and not value:
        query = 'SELECT * FROM dhcp'
        result = cursor.execute(query)
        return result.fetchall()
    else:
        return 'Пожалуйста, введите два или ноль аргументов'


if __name__ == '__main__':
    local_result = get_info(argv[1], argv[2])
    if isinstance(local_result, list):
        keys = ['MAC', 'IP', 'VLAN', 'INTERFACE', 'SWITCH']
        print(tabulate(local_result, headers=keys, tablefmt="grid", stralign='center'))
    else:
        print(local_result)
