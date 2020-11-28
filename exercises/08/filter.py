
result = {}

with open('sh_ip_interface.txt') as f:
    for line in f:
        if 'line protocol' in line:
            intf = line.split()[0]
        elif 'MTU is' in line:
            mtu = line.split()[2]
            result[intf] = mtu

print(result)