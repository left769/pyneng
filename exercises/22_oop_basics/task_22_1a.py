# -*- coding: utf-8 -*-

"""
Задание 22.1a

Скопировать класс Topology из задания 22.1 и изменить его.

Перенести функциональность удаления дублей в метод _normalize.
При этом метод __init__ должен выглядеть таким образом:
"""
from pprint import pprint


class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
    def _normalize(self, topology_dict):
        formatted_topology = {}
        for local_device, rem_device in topology_dict.items():
            if rem_device not in formatted_topology.keys():
                formatted_topology[local_device] = rem_device
        return formatted_topology


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


if __name__ == '__main__':
    top = Topology(topology_example)
    pprint(top.topology)