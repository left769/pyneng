# -*- coding: utf-8 -*-

"""
Задание 24.2b

Скопировать класс MyNetmiko из задания 24.2a.

Дополнить функционал метода send_config_set netmiko и добавить в него проверку на ошибки с помощью метода _check_error_in_command.

Метод send_config_set должен отправлять команды по одной и проверять каждую на ошибки.
Если при выполнении команд не обнаружены ошибки, метод send_config_set возвращает вывод команд.

In [2]: from task_24_2b import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_config_set('lo')
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-2-8e491f78b235> in <module>()
----> 1 r1.send_config_set('lo')

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."

"""
from netmiko.cisco.cisco_ios import CiscoIosSSH
import re

device_params = {
    "device_type": "cisco_ios",
    "ip": "192.168.100.1",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}


class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании, возникла ошибка.
    """


class MyNetmiko(CiscoIosSSH):
    def __init__(self, **device_params):
        super(MyNetmiko, self).__init__(**device_params)
        self.enable()

    def _check_error_in_command(self, command, out):
        error_check = re.search(r'% (?P<error>.+)', out)
        if error_check:
            raise ErrorInCommand(f"При выполнении команды '{command}' возникла ошибка '{error_check.group(1)}'{out}")

    def send_command(self, command_string, *args, **kwargs):
        result = super().send_command(command_string, *args, **kwargs)
        self._check_error_in_command(command_string, result)
        return result

    def send_config_set(self, commands_list):
        result = ''
        if isinstance(commands_list, str):
            commands_list = [commands_list]
        for command in commands_list:
            result += super().send_config_set(command, exit_config_mode=False)
            self._check_error_in_command(command, result)
        result += super().send_config_set('end')
        return result


if __name__ == '__main__':
    r1 = MyNetmiko(**device_params)
    print(r1.send_command('sh ip int br', strip_command=False))
