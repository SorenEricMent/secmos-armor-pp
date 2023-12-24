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

def write_nftables_config(file, protocols):
    # Write table header
    file.write('table inet secmark_rule_demo {\n\n')

    # Write secmark definitions and chain rules
    for name, port in protocols:
        file.write(f'    secmark {name}tag {{ "system_u:object_r:{name}_packet_t:s0" }}\n')
    
    file.write('\n    chain IN {\n')
    file.write('        type filter hook input priority filter;\n\n')

    for name, port in protocols:
        file.write(f'        tcp dport {port} meta secmark set "{name}tag"\n')

    file.write('    }\n')
    file.write('}\n')

def process_services_file():
    protocols = set()

    with open('/etc/services', 'r') as services_file:
        for line in services_file:
            if line.strip() and not line.startswith('#'):
                name, port, protocol = parse_service_line(line)
                if name and port and protocol == 'tcp':  # Only consider TCP for this example
                    protocols.add((name, port))

    with open('nftables.conf', 'w') as nftables_file:
        write_nftables_config(nftables_file, protocols)

process_services_file()

