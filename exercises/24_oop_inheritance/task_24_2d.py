# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен работать точно так же как метод
                                                                                            send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\n
                                                            R1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\n
                                                            R1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."
"""
from netmiko.cisco.cisco_ios import CiscoIosSSH
import re

r1_params = {
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
            raise ErrorInCommand(f"При выполнении команды '{command}' возникла ошибка '{error_check.group(1)}'")

    def send_command(self, command_string, *args, **kwargs):
        result = super().send_command(command_string, *args, **kwargs)
        self._check_error_in_command(command_string, result)
        return result

    def send_config_set(self, config_commands=None, ignore_errors=True, *args, **kwargs):
        result = ''
        if ignore_errors:
            return super(MyNetmiko, self).send_config_set(config_commands, *args, **kwargs)
        else:
            if isinstance(config_commands, str):
                config_commands = [config_commands]
            for command in config_commands:
                result += super().send_config_set(command, exit_config_mode=False, *args, **kwargs)
                self._check_error_in_command(command, result)
            result += super().send_config_set('end')
            return result


if __name__ == '__main__':
    r1 = MyNetmiko(**r1_params)
    print(r1.send_config_set('int loopback 0', ignore_errors=False))
