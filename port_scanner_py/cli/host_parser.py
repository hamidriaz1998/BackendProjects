import argparse
import ipaddress
import socket


def parse_host(value: str) -> list[str]:
    # CIDR block
    if "/" in value:
        try:
            net = ipaddress.ip_network(value, strict=False)
            return [str(ip) for ip in net.hosts()]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid CIDR value: {value}")

    # IP Range
    elif "-" in value:
        base, end = value.split("-")
        parts = base.split(".")
        if len(parts) != 4:
            raise argparse.ArgumentTypeError(f"Invalid IP range: {value}")
        try:
            start, end = int(parts[3]), int(end)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid IP range format: {value}")
        if end < start:
            raise argparse.ArgumentTypeError(f"Invalid range end: {value}")
        return [f"{parts[0]}.{parts[1]}.{parts[2]}.{i}" for i in range(start, end + 1)]

    # Single IP
    else:
        try:
            # Check if it's a valid IP address
            ipaddress.ip_address(value)
            return [value]
        except ValueError:
            # Not an IP, try to resolve as hostname
            try:
                ip = socket.gethostbyname(value)
                return [ip]
            except socket.gaierror:
                raise argparse.ArgumentTypeError(
                    f"Invalid IP address or hostname: {value}"
                )


def parse_hosts(hosts: list[str]) -> list[str]:
    result = []
    for host in hosts:
        result.extend(parse_host(host))
    return result
