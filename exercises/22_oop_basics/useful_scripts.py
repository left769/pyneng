# -*- coding: utf-8 -*-

from textfsm import clitable


def parse_command_dynamic(command_output, attributes_dict, index_file='index', templ_path='templates'):
    result = []
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    headers = cli_table.header
    for d_values in cli_table:
        result.append(dict(zip(headers, d_values)))
    return result
