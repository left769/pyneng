# -*- coding: utf-8 -*-
import sqlite3
from tabulate import tabulate


def get_info(parameter=None, value=None):
    connection = sqlite3.connect('dhcp_snooping.db')
    cursor = connection.cursor()
    if parameter and value:
        query = f'SELECT * FROM dhcp WHERE {parameter} = ?'
        result = cursor.execute(query, (value,))
        return result.fetchall()
    elif not parameter and not value:
        query = 'SELECT * FROM dhcp'
        result = cursor.execute(query)
        return result.fetchall()
    else:
        return 'Пожалуйста, введите два или ноль аргументов'


if __name__ == '__main__':
    keys = ['MAC', 'IP', 'VLAN', 'INTERFACE', 'SWITCH']
    local_result = get_info()
    print(tabulate(local_result, headers=keys, tablefmt="grid", stralign='center'))
