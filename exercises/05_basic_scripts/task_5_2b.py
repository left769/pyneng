# -*- coding: utf-8 -*-
"""
Задание 5.2b

Преобразовать скрипт из задания 5.2a таким образом,
чтобы сеть/маска не запрашивались у пользователя,
а передавались как аргумент скрипту.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

from sys import argv

network = ''.join(argv[1])
ip = (network.split('/')[0]).split('.')
mask = int(network.split('/')[1])

mask_bin = '1' * mask + '0' * (32 - mask)
mask_bin_separated = [int(mask_bin[0:8], 2), int(mask_bin[8:16], 2), int(mask_bin[16:24], 2), int(mask_bin[24:32], 2)]

mask_bin_separated_dict = """
Mask:
/{1}
{0[0]:<8}  {0[1]:<8}  {0[2]:<8}  {0[3]:<8}
{0[0]:08b}  {0[1]:08b}  {0[2]:08b}  {0[3]:08b}
"""

ip = list(map(int, ip))
ip_bin = "{0[0]:08b}  {0[1]:08b}  {0[2]:08b}  {0[3]:08b}"
ip_bin_list = ''.join(((ip_bin.format(ip)).split())[0::])

ip_bits = ip_bin_list[0:(mask)] + '0' * (32 - mask)
ip_bits = [int(ip_bits[0:8], 2), int(ip_bits[8:16], 2), int(ip_bits[16:24], 2), int(ip_bits[24:32], 2)]

ip_final = """
Network:
{0[0]:<8}  {0[1]:<8}  {0[2]:<8}  {0[3]:<8}
{0[0]:08b}  {0[1]:08b}  {0[2]:08b}  {0[3]:08b}
"""

print(ip_final.format(ip_bits))
print(mask_bin_separated_dict.format(mask_bin_separated, mask))