import socket
import concurrent.futures


def scan_ports(hosts: list[str], ports: list[int], timeout: int = 1):
    for host in hosts:
        print("*" * 30)
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=8)
        print(f"[+] Scanning for host {host}")
        for port in ports:
            pool.submit(scan_port, host, port, timeout)
        pool.shutdown(wait=True)
        print("*" * 30)

    print("Scan complete")


def scan_port(host: str, port: int, timeout: int = 1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        if result == 0:
            print(f"[+] Port {port} is open")
