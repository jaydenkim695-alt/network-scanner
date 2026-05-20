import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

COMMON_PORTS = [22, 80, 443, 21, 3389, 8080]

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((str(ip), port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ip(ip):
    open_ports = []

    for port in COMMON_PORTS:
        if scan_port(ip, port):
            open_ports.append(port)

    if open_ports:
        print(f"[+] {ip} -> Open ports: {open_ports}")

def scan_network(network):
    print(f"\nScanning network: {network}\n")

    net = ipaddress.ip_network(network, strict=False)

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(scan_ip, net.hosts())

if __name__ == "__main__":
    target_network = input("Enter network (e.g. 192.168.1.0/24): ")
    scan_network(target_network)
