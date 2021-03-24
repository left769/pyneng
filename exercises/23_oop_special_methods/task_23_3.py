# -*- coding: utf-8 -*-

"""
Задание 23.3

Скопировать и изменить класс Topology из задания 22.1x.

Добавить метод, который позволит выполнять сложение двух экземпляров класса Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
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

topology_example2 = {
    ("R1", "Eth0/4"): ("R7", "Eth0/0"),
    ("R1", "Eth0/6"): ("R9", "Eth0/0"),
}


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        self._index = 0

    def __str__(self):
        return f'Topology {self.topology}'

    def __repr__(self):
        return f"Topology('{self.topology}')"

    def __getitem__(self, item):
        return self.topology[item]

    def __iter__(self):
        return iter(self.topology)

    def __next__(self):
        if self._index < len(self.topology):
            current_item = self.topology[self._index]
            self._index += 1
            return current_item
        else:
            raise StopIteration

    def __add__(self, other):
        updateing = self.topology.copy()
        updateing.update(other.topology)
        return Topology(updateing)

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
    t1 = Topology(topology_example)
    t2 = Topology(topology_example2)
    t3 = t1 + t2
    pprint(t3.topology)
    pprint(t2.topology)
    pprint(t1.topology)
