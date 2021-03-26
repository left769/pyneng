# -*- coding: utf-8 -*-
import sqlite3
from tabulate import tabulate
from get_data import get_active_lines_info
from get_data import get_inactive_lines_info
from add_data import update_dhcp_table
from add_data import update_switches_table


def create_db(name, schema):
    print('Called function create_db')
    try:
        connection = sqlite3.connect(name)
        with open(schema, 'r') as f:
            schema = f.read()
            connection.executescript(schema)
        print('Создаю базу данных...')
    except sqlite3.OperationalError:
        print('База данных существует')


def add_data_switches(db_file, files):
    print('Called function add_data_switches')
    connection = sqlite3.connect(db_file)
    for file in files:
        update_switches_table(file, connection)


def add_data(db_file, files):
    connection = sqlite3.connect(db_file)
    for file in files:
        update_dhcp_table(file, connection)



def get_data(db_file, key, value):
    result = list(get_active_lines_info(db_file, key, value))
    decorator(result, 1)
    result = list(get_inactive_lines_info(db_file, key, value))
    decorator(result, 0)


def get_all_data(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    decorator(list(cursor.execute('SELECT * FROM dhcp WHERE active = 1')), 1)

    decorator(list(cursor.execute('SELECT * FROM dhcp WHERE active = 0')), 0)


def decorator(data, act):
    keys = ['MAC', 'IP', 'VLAN', 'INTERFACE', 'SWITCH', 'ACTIVE', 'LAST ACTIVE']
    if act and len(data):
        print('\nАктивные записи:\n')
        print(tabulate(data, headers=keys, tablefmt="grid", stralign='center'))
    elif not act and len(data):
        print('\nНеактивные записи:\n')
        print(tabulate(data, headers=keys, tablefmt="grid", stralign='center'))
