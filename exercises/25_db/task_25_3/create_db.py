# -*- coding: utf-8 -*-
import sqlite3


def create_db(db_name):
    try:
        connection = sqlite3.connect(db_name)
        with open('dhcp_snooping_schema.sql', 'r') as f:
            schema = f.read()
            connection.executescript(schema)
        print('Создаю базу данных...')
    except sqlite3.OperationalError:
        print('База данных существует')


if __name__ == '__main__':
    create_db('dhcp_snooping.db')
