# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).
Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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

    def _write_line(self, word):
        self.telnet.write((word + '\n').encode('utf-8'))

    def send_show_command(self, show_command, parse=True, index='index', templates='templates'):
        with telnetlib.Telnet(self.ip) as telnet:
            telnet.read_until(b"Username")
            telnet.write(self._write_line(self.username))
            telnet.read_until(b"Password")
            telnet.write(self._write_line(self.password))
            index, m, output = telnet.expect([b">", b"#"])
            if index == 0:
                telnet.write(b"enable\n")
                telnet.read_until(b"Password")
                telnet.write(self._write_line(self.secret))
                telnet.read_until(b"#", timeout=5)
                time.sleep(3)
                telnet.read_very_eager()

            telnet.write(self._write_line(show_command))
            out = telnet.read_until(b"#", timeout=5).decode("utf-8")
        if parse:
            connection_info = {'Command': show_command, 'Vendor': 'cisco_ios'}
            return parse_command_dynamic(out, connection_info, 'index', templates)
        else:
            return out

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
            elif error_check and strict == False:
                print(f'При выполнении команды "{command}" на устройстве {self.ip} '
                      f'возникла ошибка -> {error_check.group(1)}')
            result = result + out

        self._write_line("end")
        time.sleep(1)
        out = self.telnet.read_very_eager().decode("utf-8")
        result = result + out
        return result


if __name__ == '__main__':
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands = commands_with_errors + correct_commands
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
    test = CiscoTelnet(**r1_params)
    print(test.send_config_commands(commands, strict=False))
