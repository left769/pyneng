# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko (пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""
import telnetlib
import time
from useful_scripts import parse_command_dynamic


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self.secret = secret

    def _write_line(self, word):
        return (word + '\n').encode('utf-8')

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

    def send_config_commands(self, config_command):
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
            if type(config_command) == str:
                telnet.write(self._write_line('conf t'))
                conf_t = telnet.read_until(b"(config)#")
                telnet.write(self._write_line(config_command))
                out = telnet.read_until(b"(config)#")
                telnet.write(self._write_line('end'))
                the_end = telnet.read_until(b"#")
                result = conf_t.decode('utf-8') + out.decode('utf-8') + the_end.decode('utf-8')
            else:
                telnet.write(self._write_line('conf t'))
                result = telnet.read_until(b"(config)#").decode('utf-8')
                for command in config_command:
                    telnet.write(self._write_line(command))
                    out = telnet.read_until(b"#")
                    result = result + out.decode('utf-8')
                telnet.write(self._write_line('end'))
                result = result + telnet.read_until(b"#").decode('utf-8')
        return result


if __name__ == '__main__':
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
    test = CiscoTelnet(**r1_params)
    print(test.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255']))
