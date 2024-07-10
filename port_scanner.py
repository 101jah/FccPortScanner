import socket
from common_ports import ports_and_services

def get_open_ports(target, port_range, verbose=False):
    try:
        ip_address = socket.gethostbyname(target)  # Resolve DNS if 'target' is a URL
    except socket.gaierror:
        return "Error: Invalid hostname"

    # Validate if the IP address is valid
    try:
        socket.inet_aton(ip_address)
    except socket.error:
        return "Error: Invalid IP address"

    open_ports = []

    # Iterate through the range of ports
    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout for connection attempt

        try:
            result = sock.connect_ex((ip_address, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        except socket.error:
            pass

    if verbose:
        verbose_output = f"Open ports for {target} ({ip_address})\n"
        verbose_output += "PORT     SERVICE\n"
        for port in open_ports:
            service = ports_and_services.get(port, 'Unknown')
            verbose_output += f"{str(port):<9}{service}\n"
        return verbose_output
    else:
        return open_ports
