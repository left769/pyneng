# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
import ipaddress


class IPAddress:
    def __init__(self, ip_mask):
        self.intf = self._check_ip(ip_mask)
        self.ip_mask = ip_mask

    def __getattr__(self, item):
        if item == 'ip':
            return self.intf[0]
        elif item == 'mask':
            return self.intf[1]
    def __str__(self):
        return f'IP address {self.ip_mask}'

    def __repr__(self):
        return f"IPAddress('{self.ip_mask}')"

    def _check_ip(self, ip_intf):
        ip, mask = ip_intf.split('/')
        if int(mask) > 8 and int(mask) <= 32:
            try:
                ipaddress.ip_address(ip)
                return [ip, int(mask)]
            except ValueError:
                raise ValueError('Incorrect IPv4 address')
        else:
            raise ValueError('Incorrect mask')


if __name__ == '__main__':
    ip1 = IPAddress('10.1.1.1/24')
    print(ip1)
    print([ip1])
    print(str(ip1))
