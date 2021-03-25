# -*- coding: utf-8 -*-
import sqlite3
import yaml
import os
import re


def update_db(sw_src_file, dhcp_src_file, db_name):
    if not os.path.exists(db_name):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return None
    else:
        connection = sqlite3.connect(db_name)
        update_switches_table(sw_src_file, connection)
        update_dhcp_table(dhcp_src_file, connection)


def update_switches_table(src_file, connection):
    with open(src_file) as f:
        data = yaml.safe_load(f)
    query = 'INSERT into switches values (?, ?)'
    for line in data['switches'].items():
        try:
            connection.execute(query, line)
        except sqlite3.IntegrityError as error:
            print(f'При добавлении данных: {line} Возникла ошибка: {error}')
    connection.commit()


def update_dhcp_table(src_file, connection):
    switch_name = src_file.split('_')[0]
    query = 'INSERT into dhcp values (?, ?, ?, ?, ?)'
    src_data = open(src_file, 'r').read()
    matches = re.findall(r'(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<intf>\S+)', src_data)
    for match in matches:
        list_to_append = list(match)
        list_to_append.append(switch_name)
        try:
            connection.execute(query, list_to_append)
        except sqlite3.IntegrityError as error:
            print(f'При добавлении данных: {list_to_append} Возникла ошибка: {error}')
    connection.commit()


if __name__ == '__main__':
    update_db('switches.yml', 'sw1_dhcp_snooping.txt', 'dhcp_snooping.db')
