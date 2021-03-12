# -*- coding: utf-8 -*-

"""
Задание 22.2a

Скопировать класс CiscoTelnet из задания 22.2 и изменить метод send_show_command добавив три параметра:

* parse - контролирует то, будет возвращаться обычный вывод команды или список словарей, полученные после обработки с помощью TextFSM. При parse=True должен возвращаться список словарей, а parse=False обычный вывод. Значение по умолчанию - True.
* templates - путь к каталогу с шаблонами. Значение по умолчанию - "templates"
* index - имя файла, где хранится соответствие между командами и шаблонами. Значение по умолчанию - "index"


Пример создания экземпляра класса:

In [1]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [2]: from task_22_2a import CiscoTelnet

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_show_command:
In [4]: r1.send_show_command("sh ip int br", parse=True)
Out[4]:
[{'intf': 'Ethernet0/0',
  'address': '192.168.100.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/1',
  'address': '192.168.200.1',
  'status': 'up',
  'protocol': 'up'},
 {'intf': 'Ethernet0/2',
  'address': '192.168.130.1',
  'status': 'up',
  'protocol': 'up'}]

In [5]: r1.send_show_command("sh ip int br", parse=False)
Out[5]: 'sh ip int br | exclude unassigned\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                192.168.130.1   YES NVRAM  up                    up      \r\n\r\nR1#'


"""
import telnetlib
import time
from useful_scripts import parse_command_dynamic


class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.username = username
        self.password = password
        self. secret = secret

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


if __name__ == '__main__':
    r1_params = {
        'ip': '192.168.100.1',
        'username': 'cisco',
        'password': 'cisco',
        'secret': 'cisco'}
    test = CiscoTelnet(**r1_params)
    print(test.send_show_command('sh ip int br'))
