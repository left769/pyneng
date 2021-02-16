# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM (templates/sh_ip_int_br.template)
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt и шаблоне templates/sh_ip_int_br.template.
"""
import textfsm


def parse_output_to_dict(template, command_output):
    result = []
    with open(template) as temp:
        fsm = textfsm.TextFSM(temp)
    with open(command_output) as f:
        command = f.read()
    output = fsm.ParseText(command)
    d_keys = fsm.header
    for d_values in output:
        result.append(dict(zip(d_keys, d_values)))
    return result


if __name__ == "__main__":
    print(parse_output_to_dict('templates/sh_ip_int_br.template', 'output/sh_ip_int_br.txt'))
