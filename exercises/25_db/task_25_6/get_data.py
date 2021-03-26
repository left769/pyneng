# -*- coding: utf-8 -*-
import sqlite3
from tabulate import tabulate
from sys import argv


class ErrorInQuery(Exception):
    pass


def get_info(db_name, parameter=None, value=None):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    if parameter and value:
        return [list(get_active_lines_info(parameter, value)),
                list(get_inactive_lines_info(parameter, value))]
    elif not parameter and not value:
        query = 'SELECT * FROM dhcp'
        result = cursor.execute(query)
        return result.fetchall()
    else:
        return 'Пожалуйста, введите два или ноль аргументов'


def get_active_lines_info(db_name, parameter, value):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    try:
        query_act = f'SELECT * FROM dhcp WHERE {parameter} = ? AND active = 1'
        result = cursor.execute(query_act, (value,))
        return result
    except sqlite3.OperationalError:
        raise ErrorInQuery('Данный параметр не поддерживается. '
                           'Допустимые значения параметров: mac, ip, vlan, interface, switch')


def get_inactive_lines_info(db_name, parameter, value):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    query_in = f'SELECT * FROM dhcp WHERE {parameter} = ? AND active = 0'
    result = cursor.execute(query_in, (value,))
    return result


if __name__ == '__main__':
    local_result = get_info('dhcp_snooping.db', argv[1], argv[2])
    keys = ['MAC', 'IP', 'VLAN', 'INTERFACE', 'SWITCH', 'ACTIVE']
    print('Активные записи:')
    print(tabulate(local_result[0], headers=keys, tablefmt="grid", stralign='center'))
    if len(local_result[1]) > 0:
        print('Неактивные записи:')
        print(tabulate(local_result[1], headers=keys, tablefmt="grid", stralign='center'))
