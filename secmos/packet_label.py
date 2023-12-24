def parse_service_line(line):
    parts = line.split()
    if len(parts) >= 2:
        name = parts[0].replace('-', '_')
        # Prepend underscore if name starts with a digit
        if name[0].isdigit():
            name = 'p_' + name
        port_protocol = parts[1].split('/')
        if len(port_protocol) == 2:
            port, protocol = port_protocol
            return name, port, protocol
    return None, None, None

def write_secmark_commands(file, name, port, protocol):
    file.write(f'iptables -t mangle -A INPUT -p {protocol} --dport {port} -j SECMARK --selctx system_u:object_r:{name}_packet_t:s0\n')
    file.write(f'iptables -t mangle -A OUTPUT -p {protocol} --dport {port} -j SECMARK --selctx system_u:object_r:{name}_packet_t:s0\n')

def write_attributes(file, protocols):
    for name in protocols:
        file.write(f'attribute {name}_packet_type;\n')

def write_types(file, protocols):
    for name in protocols:
        file.write(f'type {name}_packet_t, packet_type, {name}_packet_type;\n')

def process_services_file():
    protocols = set()

    with open('/etc/services', 'r') as services_file:
        for line in services_file:
            if line.strip() and not line.startswith('#'):
                name, port, protocol = parse_service_line(line)
                if name and port and protocol:
                    protocols.add(name)

        with open('secmark.sh', 'w') as secmark_file, open('type_attr.txt', 'w') as type_attr_file:
            # Write attributes
            write_attributes(type_attr_file, protocols)
            # Separate attributes and types with a newline
            type_attr_file.write('\n')
            # Write types
            write_types(type_attr_file, protocols)

            # Reset file pointer to beginning for secmark commands
            services_file.seek(0)

            for line in services_file:
                if line.strip() and not line.startswith('#'):
                    name, port, protocol = parse_service_line(line)
                    if name and port and protocol:
                        write_secmark_commands(secmark_file, name, port, protocol)

process_services_file()
