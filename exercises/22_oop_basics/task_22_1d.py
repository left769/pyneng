# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще нет в топологии
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение "Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


"""
from pprint import pprint

topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)

    def _normalize(self, topology_dict):
        formatted_topology = {}
        for local_device, rem_device in topology_dict.items():
            if rem_device not in formatted_topology.keys():
                formatted_topology[local_device] = rem_device
        return formatted_topology

    def delete_link(self, src_dev, dst_dev):
        result = self.topology
        direct_link = result.get(src_dev)
        reverse_link = result.get(dst_dev)
        if direct_link == dst_dev:
            del result[src_dev]
        elif reverse_link == src_dev:
            del result[dst_dev]
        else:
            print('Такого соединения нет')

    def delete_node(self, device_name):
        result = self.topology.copy()
        for link in result.items():
            for peer in link:
                if peer[0] == device_name:
                    del self.topology[link[0]]
        if result == self.topology:
            print('Такого устройства нет')

    def add_link(self, src_dev, dst_dev):
        for link in self.topology.items():
            if link == (src_dev, dst_dev):
                print('Такое соединение существует')
                return None
        if src_dev in self.topology.keys() or src_dev in self.topology.values():
            print('Cоединение с одним из портов существует')
        elif dst_dev in self.topology.keys() or dst_dev in self.topology.values():
            print('Cоединение с одним из портов существует')
        else:
            self.topology[src_dev] = dst_dev


if __name__ == '__main__':
    top = Topology(topology_example)
    pprint(top.add_link(("R1", "Eth0/0"), ("SW1", "Eth0/1")))
    pprint(top.topology)
