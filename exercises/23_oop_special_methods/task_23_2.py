# -*- coding: utf-8 -*-

"""
Задание 23.2

Добавить к классу CiscoTelnet из задания 25.2x поддержку работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
"""
import telnetlib
import time
import re
from useful_scripts import parse_command_dynamic


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b"Username")
        self._write_line(username)
        self.telnet.read_until(b"Password")
        self._write_line(password)
        self._write_line('enable')
        self.telnet.read_until(b"Password:")
        self._write_line(secret)
        self._write_line("terminal length 0")
        time.sleep(1)
        self.telnet.read_very_eager()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.telnet.close()

    def _write_line(self, word):
        self.telnet.write((word + '\n').encode('utf-8'))

    def send_show_command(self, show_command, parse=False, templates='templates'):
        self._write_line(show_command)
        result = self.telnet.read_until(b"#").decode("utf-8")
        time.sleep(1)
        if parse:
            connection_info = {'Command': show_command, 'Vendor': 'cisco_ios'}
            return parse_command_dynamic(result, connection_info, 'index', templates)
        else:
            return result

    def send_config_commands(self, config_command, strict=True):
        result = ''
        if type(config_command) == str:
            config_command = [config_command]

        self._write_line('conf t')
        for command in config_command:
            self._write_line(command)
            time.sleep(1)
            out = self.telnet.read_very_eager().decode("utf-8")
            error_check = re.search(r'% (?P<error>.+)', out)
            if error_check and strict:
                raise ValueError(f'При выполнении команды "{command}" на устройстве {self.ip} '
                                 f'возникла ошибка -> {error_check.group(1)}')
            elif error_check and not strict:
                print(f'При выполнении команды "{command}" на устройстве {self.ip} '
                      f'возникла ошибка -> {error_check.group(1)}')
            result = result + out

        self._write_line("end")
        time.sleep(1)
        out = self.telnet.read_very_eager().decode("utf-8")
        result = result + out
        return result


if __name__ == '__main__':
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
    with CiscoTelnet(**r1_params) as r1:
        print(r1.send_show_command('sh clock'))
        raise ValueError('Возникла ошибка')
