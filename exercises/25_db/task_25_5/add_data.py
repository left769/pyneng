# -*- coding: utf-8 -*-
import sqlite3
import yaml
import os
import re
from datetime import timedelta, datetime




def update_db(db_name, sw_src_file=None, dhcp_src_file=None):
    if not os.path.exists(db_name):
        print('База данных не существует. Перед добавлением данных, ее надо создать')
        return None
    else:
        connection = sqlite3.connect(db_name)
        del_old_lines(connection)
        if sw_src_file:
            update_switches_table(sw_src_file, connection)
        if dhcp_src_file:
            update_dhcp_table(dhcp_src_file, connection)


def del_old_lines(connection):
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    connection.execute(f"DELETE FROM dhcp WHERE last_active < '{week_ago}'")


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
    switch_name = re.match(r'\S*(?P<host>sw\d+)_dhcp_snooping.txt', src_file)
    src_data = open(src_file, 'r').read()
    connection.execute(f"UPDATE dhcp SET active = 0 WHERE switch = '{switch_name[1]}'")
    matches = re.findall(r'(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<intf>\S+)', src_data)

    query = "INSERT INTO dhcp VALUES (?, ?, ?, ?, ?, ?, datetime('now'))"
    for match in matches:
        list_to_append = list(match)
        list_to_append.extend([switch_name[1], 1])
        try:
            connection.execute(query, list_to_append)
        except sqlite3.IntegrityError:
            connection.execute(f"UPDATE dhcp SET ip = '{list_to_append[1]}',"
                               f" vlan = '{list_to_append[2]}',"
                               f" interface = '{list_to_append[3]}',"
                               f" active = '{list_to_append[5]}',"
                               f" last_active = datetime('now')"
                               f" WHERE mac = '{list_to_append[0]}' and switch = '{list_to_append[4]}'")

    connection.commit()


if __name__ == '__main__':
    update_db('dhcp_snooping.db', dhcp_src_file='new_data/sw2_dhcp_snooping.txt')
